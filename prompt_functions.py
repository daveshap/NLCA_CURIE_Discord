def make_prompt_default(filename, content):
    with open(filename, 'r') as infile:
        prompt = infile.read()
    prompt = prompt.replace('<<TEXT>>', content)
    return prompt