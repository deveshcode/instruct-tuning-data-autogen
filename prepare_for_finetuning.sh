batch_dir=data/llama3_generations/

python self_instruct/prepare_for_finetuning.py \
    --instance_files ${batch_dir}/machine_generated_instances.jsonl \
    --classification_type_files ${batch_dir}/is_clf_or_not_llama3_template_1.jsonl \
    --output_dir ${batch_dir}/finetuning_data \
    --include_seed_tasks \
    --seed_tasks_path data/seed_tasks.jsonl
