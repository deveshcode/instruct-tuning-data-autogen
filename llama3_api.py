import json
import os
import time
from datetime import datetime
import argparse
from groq import Groq
from dotenv import load_dotenv
import tqdm

load_dotenv()  # Load environment variables from .env.

# Configure Groq API
groq_api_key = os.getenv("GROQ_API_KEY")

client = Groq(api_key=groq_api_key)

def make_requests(prompts, stop_sequences, retries=3):
    response = None
    retry_cnt = 0
    backoff_time = 30
    results = []
    
    while retry_cnt <= retries:
        try:
            for prompt in prompts:
                chat_completion = client.chat.completions.create(
                    messages=[
                        {"role": "user", "content": prompt}
                    ],
                    model="llama3-8b-8192"
                )
                response = chat_completion.choices[0].message.content.strip()
                for stop_seq in stop_sequences:
                    if stop_seq in response:
                        print("\n\nOriginal response")
                        print(response)
                        print("\n\nFound stop sequence ", stop_seq)
                        print(response.split(stop_seq))
                        response = response.split(stop_seq)[0]
                        break
                results.append({
                    "prompt": prompt,
                    "response": {"choices": [{"text": response}]},
                    "created_at": str(datetime.now()),
                })
            break
        except Exception as e:
            print(f"Error: {e}. Retrying in {backoff_time} seconds...")
            time.sleep(backoff_time)
            backoff_time *= 1.5
            retry_cnt += 1

    return results

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input_file",
        type=str,
        help="The input file that contains the prompts to Llama-3.",
    )
    parser.add_argument(
        "--output_file",
        type=str,
        help="The output file to save the responses from Llama-3.",
    )
    parser.add_argument(
        "--use_existing_responses",
        action="store_true",
        help="Whether to use existing responses from the output file if it exists."
    )
    parser.add_argument(
        "--request_batch_size",
        default=20,
        type=int,
        help="The number of requests to send to Llama-3 at a time."
    )
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    os.makedirs(os.path.dirname(args.output_file), exist_ok=True)

    # Read existing file if it exists
    existing_responses = {}
    if os.path.exists(args.output_file) and args.use_existing_responses:
        with open(args.output_file, "r") as fin:
            for line in fin:
                data = json.loads(line)
                existing_responses[data["prompt"]] = data

    # Do new prompts
    with open(args.input_file, "r") as fin:
        if args.input_file.endswith(".jsonl"):
            all_prompts = [json.loads(line)["prompt"] for line in fin]
        else:
            all_prompts = [line.strip().replace("\\n", "\n") for line in fin]

    with open(args.output_file, "w") as fout:
        for i in tqdm.tqdm(range(0, len(all_prompts), args.request_batch_size)):
            batch_prompts = all_prompts[i: i + args.request_batch_size]
            if all(p in existing_responses for p in batch_prompts):
                for p in batch_prompts:
                    fout.write(json.dumps(existing_responses[p]) + "\n")
            else:
                results = make_requests(batch_prompts)
                for data in results:
                    fout.write(json.dumps(data) + "\n")
