output_first_template_for_clf = '''
Generate examples for the following classification task. Return the examples in JSON format with "task", "examples" keys. The "examples" key should contain an array of objects, each with "class_label", "input", and "output" keys. If the task doesn't require additional input, leave the "input" field empty. Include examples for all relevant class labels for the given task.

Here are some examples:

{
  "task": "Classify the sentiment of the sentence into positive, negative, or mixed.",
  "examples": [
    {
      "class_label": "mixed",
      "input": "I enjoy the flavor of the restaurant but their service is too slow.",
      "output": "mixed"
    },
    {
      "class_label": "positive",
      "input": "I had a great day today. The weather was beautiful and I spent time with friends and family.",
      "output": "positive"
    },
    {
      "class_label": "negative",
      "input": "I was really disappointed by the latest superhero movie. I would not recommend it to anyone.",
      "output": "negative"
    }
  ]
}

{
  "task": "Given a dialogue, classify whether the user is satisfied with the service. You should respond with 'Satisfied' or 'Unsatisfied'.",
  "examples": [
    {
      "class_label": "Satisfied",
      "input": "- Agent: Thank you for your feedback. We will work to improve our service in the future.\n- Customer: I am happy with the service you provided. Thank you for your help.",
      "output": "Satisfied"
    },
    {
      "class_label": "Unsatisfied",
      "input": "- Agent: I am sorry we will cancel that order for you, and you will get a refund within 7 business days.\n- Customer: oh that takes too long. I want you to take quicker action on this.",
      "output": "Unsatisfied"
    }
  ]
}

{
  "task": "Classify the given text as either a fact or an opinion.",
  "examples": [
    {
      "class_label": "Fact",
      "input": "The Earth revolves around the Sun.",
      "output": "Fact"
    },
    {
      "class_label": "Opinion",
      "input": "Summer is the best season of the year.",
      "output": "Opinion"
    }
  ]
}

{
  "task": "Determine whether the given statement is sarcastic or not.",
  "examples": [
    {
      "class_label": "Sarcastic",
      "input": "Oh great, another meeting. Just what I needed to make my day complete.",
      "output": "Sarcastic"
    },
    {
      "class_label": "Not Sarcastic",
      "input": "I'm really looking forward to our team-building event this weekend.",
      "output": "Not Sarcastic"
    }
  ]
}

{
  "task": "Classify the given movie review as either fresh or rotten.",
  "examples": [
    {
      "class_label": "Fresh",
      "input": "This film is a masterpiece of modern cinema, with stunning visuals and a gripping storyline that keeps you on the edge of your seat.",
      "output": "Fresh"
    },
    {
      "class_label": "Rotten",
      "input": "A complete waste of time and money. The plot is nonsensical, the acting is wooden, and the special effects look cheap.",
      "output": "Rotten"
    }
  ]
}

{
  "task": "Determine whether the given text is written in formal or informal language.",
  "examples": [
    {
      "class_label": "Formal",
      "input": "We regret to inform you that your application has been declined due to insufficient qualifications.",
      "output": "Formal"
    },
    {
      "class_label": "Informal",
      "input": "Hey there! Just wanted to give you a heads up that we can't take you on board right now. Maybe next time?",
      "output": "Informal"
    }
  ]
}

{
  "task": "Classify the given animal based on its characteristics as mammal, bird, reptile, or fish.",
  "examples": [
    {
      "class_label": "Mammal",
      "input": "Warm-blooded, gives birth to live young, has fur or hair, breathes air",
      "output": "Mammal"
    },
    {
      "class_label": "Bird",
      "input": "Warm-blooded, lays eggs, has feathers, can fly",
      "output": "Bird"
    },
    {
      "class_label": "Reptile",
      "input": "Cold-blooded, lays eggs, has scales, breathes air",
      "output": "Reptile"
    },
    {
      "class_label": "Fish",
      "input": "Cold-blooded, lays eggs, has scales, breathes underwater through gills",
      "output": "Fish"
    }
  ]
}

Explanation of the JSON structure:
- "task": The description of the classification task.
- "examples": An array of example objects, each containing:
  - "class_label": The expected class or category for the given input.
  - "input": The input data for classification. This can be a sentence, dialogue, characteristics, or any other relevant information.
  - "output": The expected output or classification result based on the input and class label.

Now, generate examples for the following task. Only the return the Final JSON and nothing else:

Task : 
'''

input_first_template_for_gen = '''

Generate examples for the following task. Return the examples in JSON format with "instruction", "input", and "output" keys. If the task doesn't require additional input, leave the "input" field empty. Generate multiple examples when possible.

Here are some examples of how to format your response:

{
  "examples": [
    {
      "instruction": "Which exercises are best for reducing belly fat at home?",
      "input": "",
      "output": "- Lying Leg Raises\n- Leg In And Out\n- Plank\n- Side Plank\n- Sit-ups"
    },
    {
      "instruction": "Extract all the country names in the paragraph, list them separated by commas.",
      "input": "Dr. No is the sixth novel by the English author Ian Fleming to feature his British Secret Service agent James Bond. Written at Fleming's Goldeneye estate in Jamaica, it was first published in the United Kingdom by Jonathan Cape in 1958. The character of Doctor No, the son of a German missionary and a Chinese woman, was influenced by Sax Rohmer's Fu Manchu stories. Dr. No was the first of Fleming's novels to face widespread negative reviews in Britain, but it was received more favourably in the United States.",
      "output": "English, British, Jamaica, the United Kingdom, German, Chinese, Britain, the United States"
    },
    {
      "instruction": "Convert 85 F to Celsius.",
      "input": "",
      "output": "85°F = 29.44°C"
    },
    {
      "instruction": "Sort the given list ascendingly.",
      "input": "[10, 92, 2, 5, -4, 92, 5, 101]",
      "output": "[-4, 2, 5, 5, 10, 92, 92, 101]"
    },
    {
      "instruction": "Suggest a better and more professional rephrasing of the following sentence.",
      "input": "This house is surprisingly not constructed very well, and you probably need more money to fix it after you buy it. If you ask me, I would suggest you to consider other candidates.",
      "output": "This house does not seem to be constructed well, so you may need to spend more money to fix it after you purchase it. I would suggest that you look at other properties."
    }
  ]
}

Now, generate an examples for the following task. Return the examples in JSON format with "instruction", "input", and "output" keys. Only return the JSON object and nothing else.:
'''