import json
import os

json_dir = 'data/podcasts'
content_dir = 'content/podcasts'

if not os.path.exists(content_dir):
    os.makedirs(content_dir)

for json_file in os.listdir(json_dir):
    if json_file.endswith('.json'):
        with open(os.path.join(json_dir, json_file), 'r') as f:
            data = json.load(f)
        
        content_file = os.path.join(content_dir, f"{os.path.splitext(json_file)[0]}.md")
        
        with open(content_file, 'w') as f:
            f.write('---\n')
            for key, value in data.items():
                if key != 'description':
                    f.write(f'{key}: {value}\n')
            f.write('---\n')
            f.write(f'# {data["name"]}\n\n')
            f.write(f'{data["description"]}\n')
