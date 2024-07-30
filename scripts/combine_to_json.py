import yaml
import json

def represent_none(self, _):
    return self.represent_scalar('tag:yaml.org,2002:null', '')

yaml.add_representer(type(None), represent_none)

translations = "main_2024_07_30.yaml"
sources = "source_2024_07_30.yaml"

with open(translations, 'r') as file:
  tra_db = yaml.safe_load(file)

with open(sources, 'r') as file:
  sou_db = yaml.safe_load(file)

to_dump = []

for n, entry in enumerate(tra_db):
  source_data = {}
  for source_entry in sou_db:
    if source_entry["id"] == entry["source"][0]:
      source_data = source_entry
  to_dump.append({"trans_data": entry, "source_data": source_data})

dump = json.dumps(to_dump, ensure_ascii=False)
print(dump)