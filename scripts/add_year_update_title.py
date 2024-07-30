import yaml

def represent_none(self, _):
    return self.represent_scalar('tag:yaml.org,2002:null', '')

yaml.add_representer(type(None), represent_none)

filename = "main_2024_07_29.yaml"

with open(filename, 'r') as file:
  db = yaml.safe_load(file)

for entry in db:
  earliest_year = "unknown"
  earliest_title = ""
  earliest_title_translit = ""
  for edition in entry["editions"]:
    if edition["year"] == "unknown":
      if earliest_year == 0:
        earliest_year = "unknown"
        earliest_title = edition["title"]
        earliest_title_translit = edition["title_translit"]        
    elif earliest_year == "unknown" or edition["year"] < earliest_year:
      earliest_year = edition["year"]
      earliest_title = edition["title"]
      earliest_title_translit = edition["title_translit"]
  entry["year"] = earliest_year
  entry["title"] = earliest_title
  entry["title_translit"] = earliest_title_translit

print(yaml.dump(db, allow_unicode=True, sort_keys=False))
