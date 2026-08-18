import json, re

# Open the file and parse the JSON content
with open('data.json', 'r') as file:
    data = json.load(file)

items = set()
for o in data:
    for i in o["Requirements"]:
        i = re.sub(r" x\d+$", "", i)
        items.add(i)

with open('items.json', "w") as f:
    json.dump(list(items), f)