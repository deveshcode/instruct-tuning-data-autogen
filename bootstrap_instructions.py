import os
import json
import random
import re
import string
import tqdm
import argparse
import numpy as np
import pandas as pd
from multiprocessing import Pool
from functools import partial
from rouge_score import rouge_scorer
from llama3_api import make_requests as make_llama3_requests  # Update import
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

random.seed(42)

def encode_prompt(prompt_instructions, classification=False):
    """Encode multiple prompt instructions into a single string."""
    if classification:
        prompt = "Come up with a series of classification tasks. Try to specify the possible output labels when possible.\n"
    else:
        prompt = "Come up with a series of tasks:\n"
    for idx, instruction in enumerate(prompt_instructions):
        instruction = re.sub(r"\s+", " ", instruction).strip().rstrip(":")
        prompt += f"{idx+1}. {instruction}\n"
    prompt += f"{len(prompt_instructions) + 1}."
    logging.debug(f"Encoded prompt: {prompt}")
    return prompt

def sample_machine_instructions(machine_instructions, similarities, n):
    """Sample n machine instructions from a list of machine instructions."""
    sampled_instructions = random.sample(machine_instructions, min(n, len(machine_instructions)))
    logging.debug(f"Sampled {n} machine instructions")
    return sampled_instructions

def find_word_in_string(w, s):
    return re.compile(r'\b({0})\b'.format(w), flags=re.IGNORECASE).search(s)

def post_process_llama3_response(response):
    if response is None:
        logging.warning("Response was None or cut off due to length.")
        return []
    raw_instructions = re.split(r"\n\d+\s?\. ", response["choices"][0]["text"])
    instructions = []
    for inst in raw_instructions:
        inst = re.sub(r"\s+", " ", inst).strip()
        inst = inst.strip().capitalize()
        if inst == "":
            continue
        # Filter out too short or too long instructions
        if len(inst.split()) <= 3 or len(inst.split()) > 150:
            continue
        # Filter based on keywords that are not suitable for language models.
        if any(find_word_in_string(word, inst) for word in ["image", "images", "graph", "graphs", "picture", "pictures", "file", "files", "map", "maps", "draw", "plot", "go to"]):
            continue
        # Filter out instructions starting with "Write a program"
        if inst.startswith("Write a program"):
            continue
        # Filter those starting with punctuation
        if inst[0] in string.punctuation:
            continue
        # Filter those starting with non-English character
        if not inst[0].isascii():
            continue
        instructions.append(inst)
    logging.info(f"Post-processed response: {instructions}")
    return instructions

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--batch_dir",
        type=str,
        required=True,
        default="data/llama3_generations/",
        help="The directory where the batch is stored.",
    )
    parser.add_argument(
        "--seed_tasks_path",
        type=str,
        required=True,
        default="data/seed_tasks.jsonl",
        help="The path to the human written data.",
    )
    parser.add_argument(
        "--num_instructions_to_generate",
        type=int,
        default=100,
        help="Number of instructions to generate.",
    )
    parser.add_argument(
        "--use_clf_seed_tasks_only",
        action="store_true",
        help="If specified, we will only use the classification seed tasks to prompt new instructions. This will lead to more classification instructions.",
    )
    parser.add_argument(
        "--num_prompt_instructions",
        type=int,
        default=8,
        help="The number of instructions to use in the prompt."
    )
    parser.add_argument(
        "--request_batch_size",
        type=int,
        default=5,
        help="The number of requests to send to Llama-3 at a time."
    )
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    logging.info(f"Arguments parsed: {args}")

    # Load seed tasks
    seed_tasks = [json.loads(l) for l in open(args.seed_tasks_path, "r")]
    if args.use_clf_seed_tasks_only:
        seed_tasks = [t for t in seed_tasks if t["is_classification"]]
    seed_instructions = [t["instruction"] for t in seed_tasks]
    logging.info(f"Loaded {len(seed_instructions)} human-written seed instructions")

    os.makedirs(args.batch_dir, exist_ok=True)
    logging.info(f"Batch directory {args.batch_dir} created/exists")

    request_idx = 0
    # Load the LM-generated instructions
    machine_instructions = []
    if os.path.exists(os.path.join(args.batch_dir, "machine_generated_instructions.jsonl")):
        with open(os.path.join(args.batch_dir, "machine_generated_instructions.jsonl"), "r") as fin:
            for line in fin:
                instruction_info = json.loads(line)
                machine_instructions.append(instruction_info["instruction"])
                request_idx = instruction_info["request_idx"] + 1
        logging.info(f"Loaded {len(machine_instructions)} machine-generated instructions")

    scorer = rouge_scorer.RougeScorer(["rougeL"], use_stemmer=False)
    logging.info("Initialized ROUGE scorer")

    # Now let's generate new instructions!
    progress_bar = tqdm.tqdm(total=args.num_instructions_to_generate)
    if machine_instructions:
        progress_bar.update(len(machine_instructions))

    with open(os.path.join(args.batch_dir, "machine_generated_instructions.jsonl"), "a") as fout:
        while len(machine_instructions) < args.num_instructions_to_generate:
            logging.info(f"Generating batch, currently have {len(machine_instructions)} instructions")
            batch_inputs = []
            for _ in range(args.request_batch_size):
                # Sample machine instructions from the pool
                prompt_instructions = sample_machine_instructions(
                    machine_instructions, 
                    similarities=None,
                    n=2)
                # Sample human instructions from the pool
                prompt_instructions += random.sample(seed_instructions, args.num_prompt_instructions - len(prompt_instructions))
                random.shuffle(prompt_instructions)
                prompt = encode_prompt(prompt_instructions, classification=args.use_clf_seed_tasks_only)
                batch_inputs.append(prompt)
            logging.info(f"Batch inputs prepared: {batch_inputs}")

            results = make_llama3_requests(batch_inputs)
            logging.info(f"Received results: {results}")

            instructions = []
            all_metadata = []
            for result in results:
                new_instructions = post_process_llama3_response(result["response"])
                instructions += new_instructions
                all_metadata += [result] * len(new_instructions)

            for inst, metadata in zip(instructions, all_metadata):
                with Pool(4) as p:
                    rouge_scores = p.map(partial(scorer.score, inst), seed_instructions + machine_instructions)
                rouge_scores = [score["rougeL"].fmeasure for score in rouge_scores]
                logging.info(f"ROUGE scores for '{inst}': {rouge_scores}")

                if max(rouge_scores) > 0.7:
                    logging.info(f"Instruction '{inst}' too similar to existing ones, skipping.")
                    continue

                all_instructions = seed_instructions + machine_instructions
                most_similar_instructions = {
                    all_instructions[i]: rouge_scores[i] for i in np.argsort(rouge_scores)[-10:][::-1]
                }
                machine_instructions.append(inst)
                fout.write(json.dumps({
                    "instruction": inst,
                    "most_similar": most_similar_instructions,
                    "avg_similarity_score": float(np.mean(rouge_scores)),
                    "metadata": metadata,
                    "request_idx": request_idx
                }) + "\n")
                logging.info(f"Instruction '{inst}' added to machine-generated instructions")
                progress_bar.update(1)
            request_idx += 1
