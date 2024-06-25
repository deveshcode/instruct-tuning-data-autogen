batch_dir=data/llama3_generations/

python bootstrap_instructions.py \
    --batch_dir ${batch_dir} \
    --num_instructions_to_generate 30 \
    --seed_tasks_path data/seed_tasks.jsonl \
    --num_prompt_instructions 5 \
    --request_batch_size 1
