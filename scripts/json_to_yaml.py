import yaml
from internetarchive import get_item
import json

class Dumper(yaml.Dumper):
    def increase_indent(self, flow=False, *args, **kwargs):
        return super().increase_indent(flow=flow, indentless=False)

template_yaml = """
id:
title:
title_translit:
translator:
  -
editions:
  - type:
    title:
    publisher:
    place:
    year:
    volumes:
      - number:
        date:
        source:
        source_id:
        notes:
keywords:
  -
notes:
source:
  title:
  author:
    - 
  language:
    -
  links:
    -
  wikidata_id:
"""

title_raw = open("./nybc_id_yiddish_title.json")
title_json = json.load(title_raw)

json_location = "./db_versions/db_2024_07_11.json"
raw = open(json_location, "r")

entries = {}

id_number = 0

json_object = json.load(raw)
for item in json_object:
    template = yaml.safe_load(template_yaml)

    title = item["title"]
    author = item["author"]
    translator = item["translator"]
    o_title = item["o_title"]
    o_language = item["o_language"]
    wikidata = item["wikidata"]
    notes = item["notes"]
    links = item["links"]
    volume_number = item["volume"]
    nybc_id = item["nybc_id"]
    place = item["place"]
    publisher = item["publisher"]
    year = item["year"]
    keywords = item["keywords"]
    id = item["id"]
    yid_title = title_json[nybc_id]

    #do not include anthologies
    if "anthology" in notes or "Anthology" in notes:
      continue

    if type(translator) == list:
      translator_key = ''.join(translator)
    else:
      translator_key = translator

    if type(publisher) == list:
      publisher_key = ''.join(publisher)
    else:
      publisher_key = publisher

    if o_title == "unknown":
      o_title_key = o_title + nybc_id
    else:
      o_title_key = o_title

    key = o_title_key + translator_key + publisher_key

    if key in entries:
      years_listed = []
      new_volume = {'number': volume_number, 'date': None, 'source': "nybc", 'source_id': nybc_id, 'notes': notes}
      for edition in entries[key]["editions"]:
        years_listed.append(edition["year"])
      if year not in years_listed:
        entries[key]["editions"].append({'type': "book", 'title': title, 'publisher': publisher, 'place': place, 'year': year, 'volumes': [new_volume]})
      else:
        for edition in entries[key]["editions"]:
          if edition['year'] == year:
            edition['volumes'].append(new_volume)

    else:
      template["id"] = "ytd" + format(id_number, '06')
      template["title"] = yid_title
      template["title_translit"] = title
      if type(translator) == list:
          template["translator"] = translator
      else:
          template["translator"][0] = translator
      template["editions"][0]["type"] = "book"
      template["editions"][0]["title"] = title
      template["editions"][0]["publisher"] = publisher
      template["editions"][0]["place"] = place
      template["editions"][0]["year"] = year
      template["editions"][0]["volumes"][0]["number"] = volume_number
      template["editions"][0]["volumes"][0]["date"] = None
      template["editions"][0]["volumes"][0]["source"] = "nybc"
      template["editions"][0]["volumes"][0]["source_id"] = nybc_id
      template["editions"][0]["notes"] = None
      template["keywords"] = keywords
      template["notes"] = notes
      template["source"]["title"] = o_title
      template["source"]["author"] = author
      if type(template["source"]["language"]) == list:
          template["source"]["language"] = o_language
      else:
          template["source"]["language"][0] = o_language
      template["source"]["links"][0] = links
      template["source"]["wikidata_id"] = wikidata

      entries[key] = template
      id_number = id_number + 1


for key in entries:
    print("---")
    print(yaml.dump(entries[key], sort_keys=False, Dumper=Dumper, allow_unicode=True))
print("---")

