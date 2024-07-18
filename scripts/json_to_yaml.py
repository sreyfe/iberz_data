import yaml
from internetarchive import get_item
import json
from unidecode import unidecode
import re

class Dumper(yaml.Dumper):
    def increase_indent(self, flow=False, *args, **kwargs):
        return super().increase_indent(flow=flow, indentless=False)

main_file = open("main.yaml", "w")
source_file = open("source.yaml", "w")

main_template_yaml = """
id:
slug:
title:
title_translit:
translator:
  - name: 
    name_translit:
    wikidata:
editions:
  - type:
    title:
    title_translit:
    publisher:
    publisher_translit:
    place:
    year:
    volumes:
      - number:
        date:
        first_page:
        last_page:
        source_db:
        source_db_id:
        notes:
keywords:
  -
notes:
source:
  - 
"""

source_template_yaml = """
id:
slug:
title:
title_translit:
author:
  - 
language:
  -
links:
  -
wikidata_id:
"""

title_raw = open("../misc/nybc_id_yiddish_title.json")
title_json = json.load(title_raw)

json_location = "../db_versions/db_2024_07_17.json"
raw = open(json_location, "r")

main_entries = {}
source_entries = {}

id_number = 0
source_id_number = 0

json_object = json.load(raw)
for item in json_object:
    template = yaml.safe_load(main_template_yaml)
    source_template = yaml.safe_load(source_template_yaml)

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

    if type(author) == list:
      author_key = ''.join(author)
    else:
      author_key = author

    if o_title == "unknown":
      o_title_key = o_title + nybc_id
    else:
      o_title_key = o_title


    alpha_num_title = re.sub('[^0-9a-zA-Z_]+', '', '_'.join(unidecode(title).split()[:3]))

    main_slug = alpha_num_title + "_" + ''.join(unidecode(translator_key).replace(",", "").split()[:1])
    #print(main_slug)
    key = o_title_key + translator_key
    source_key = o_title_key + author_key



    if key in main_entries:
      years_listed = []
      new_volume = {'number': volume_number, 'date': None, 'first_page': None, 'last_page': None, 'source_db': "nybc", 'source_db_id': nybc_id, 'notes': notes}
      for edition in main_entries[key]["editions"]:
        years_listed.append(edition["year"])
      if year not in years_listed:
        main_entries[key]["editions"].append({'type': "book", 'title': yid_title, 'title_translit': title, 'publisher': None, 'publisher_translit': publisher, 'place': place, 'year': year, 'volumes': [new_volume]})
      else:
        for edition in main_entries[key]["editions"]:
          if edition['year'] == year:
            edition['volumes'].append(new_volume)

    else:
      template["id"] = "ytd" + format(id_number, '06')
      template["slug"] = main_slug
      template["title"] = yid_title
      template["title_translit"] = title
      if type(translator) == list:
        for n, tran in enumerate(translator):
          #sorry for this vvvv
          if n == 0:
            template["translator"][0]["name_translit"] = translator
          else:
            template["translator"].append({'name': None, 'name_translit': tran, 'wikidata': None})
      else:
        template["translator"][0]["name_translit"] = translator
      template["editions"][0]["type"] = "book"
      template["editions"][0]["title"] = yid_title
      template["editions"][0]["title_translit"] = title
      template["editions"][0]["publisher_translit"] = publisher
      template["editions"][0]["place"] = place
      template["editions"][0]["year"] = year
      template["editions"][0]["volumes"][0]["number"] = volume_number
      template["editions"][0]["volumes"][0]["date"] = None
      template["editions"][0]["volumes"][0]["source_db"] = "nybc"
      template["editions"][0]["volumes"][0]["source_db_id"] = nybc_id
      template["editions"][0]["notes"] = None
      template["keywords"] = keywords
      template["notes"] = notes
      source_template["title"] = o_title

      main_entries[key] = template
      id_number = id_number + 1

    if source_key in source_entries:
      template["source"][0] = source_entries[source_key]["id"]
    else:
      source_template["id"] = "ytds" + format(source_id_number, '06')
      source_template["title"] = o_title
      if type(o_language) == list:
          source_template["language"] = o_language
      else:
          source_template["language"][0] = o_language
      source_template["links"][0] = links

      source_template["wikidata_id"] = wikidata
      if type(author) == list:
          source_template["author"] = author
      else:
          source_template["author"][0] = author
      source_entries[source_key] = source_template
      template["source"][0] = source_entries[source_key]["id"]
      
      source_id_number = source_id_number + 1




for key in main_entries:
    main_file.write("---\n")
    main_file.write(yaml.dump(main_entries[key], sort_keys=False, Dumper=Dumper, allow_unicode=True))
main_file.write("---\n")

for key in source_entries:
    source_file.write("---\n")
    source_file.write(yaml.dump(source_entries[key], sort_keys=False, Dumper=Dumper, allow_unicode=True))
source_file.write("---\n")
