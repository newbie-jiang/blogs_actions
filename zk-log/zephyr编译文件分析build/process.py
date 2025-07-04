import json

with open('compile_commands.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

with open('files.txt', 'w', encoding='utf-8') as f:
    for entry in data:
        f.write(entry['file'] + '\n')
