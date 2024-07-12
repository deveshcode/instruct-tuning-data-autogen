# Self-Instruct Data Generation

This repository contains the code for generating data for fine-tuning a language model using the Self-Instruct method described in the paper Self-Instruct: Aligning Language Model with Self-Generated Instructions.

# Requirements
- Python 3.6 or higher
- Groq API key
- rouge-score library
- multiprocessing library
- functools library

# Usage

Clone the repository:

```bash
git clone https://github.com/your-username/self-instruct-data-generation.git
```

Install the required libraries:

```bash
pip install -r requirements.txt
```

Set up your Groq API key by replacing "GROQ" with your own API key in the make_requests function in main.py.

Run the code:
Self_Instruct_Full.ipynb 

The code will generate data for fine-tuning a language model using the Self-Instruct method. The generated data will be saved to a JSONL file.

# Code Overview

The code consists of the following main functions:

- make_requests: Makes requests to the Groq API and returns the response.
- generate_instructions: Generates new instructions based on the seed tasks using a language model.
- classify_instructions: Determines whether each instruction corresponds to a classification or non-classification task.
- generate_instances: Generates instances for each instruction using a suitable template.
- prepare_finetuning_data: Prepares the data for fine-tuning the language model.

The code also includes helper functions for extracting JSON from a response string and encoding instances in a suitable format for training.

# Data Format
The generated data is saved to a JSONL file, where each line contains a JSON object with the following keys:

- prompt: The instruction and input, formatted as a prompt string.
- completion: The expected output for the prompt.

The data is shuffled and saved to the output file in this format.