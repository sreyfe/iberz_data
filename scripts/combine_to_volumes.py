### The purpose of this particular script is to unravel the .yaml format
### I have currently in order to get a list of volumes

import yaml
import json

def represent_none(self, _):
    return self.represent_scalar('tag:yaml.org,2002:null', '')

yaml.add_representer(type(None), represent_none)

translations = "../db_versions/2025_03_07/main_2025_03_07.yaml"
sources = "../db_versions/2025_03_07/source_2025_03_07.yaml"

with open(translations, 'r') as file:
    tra_db = yaml.safe_load(file)

with open(sources, 'r') as file:
    sou_db = yaml.safe_load(file)

to_dump = []

for n, entry in enumerate(tra_db):
    trans_id = entry["id"]

    translators = []
    for translator in entry["translator"]:
        translators.append(translator["name_translit"])

    source_data = {}
    for source_entry in sou_db:
        if source_entry["id"] == entry["source"][0]:
            source_data = source_entry

    source_id = source_data["id"]
    source_title = source_data["title"]
    author = source_data["author"]
    language = source_data["language"]
    wikidata_id = source_data["wikidata_id"]

    for edition in entry['editions']:
        title = edition["title_translit"]
        publisher = edition["publisher_translit"]
        place = edition["place"]
        year = edition["year"]

        for volume in edition['volumes']:
            number = volume['number']
            to_dump.append({"title": title,
                            "source_title": source_title,
                            "translator": translators,
                            "author": author,
                            "publisher": publisher,
                            "place": place,
                            "year": year,
                            "language": language,
                            "source_id": source_id,
                            "trans_id": trans_id,
                            })

dump = json.dumps(to_dump, ensure_ascii=False)
print(dump)
