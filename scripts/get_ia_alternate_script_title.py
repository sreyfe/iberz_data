from internetarchive import get_item
import json

id_title_dict = {}

json_location = "./db_versions/db_2024_07_11.json"
raw = open(json_location, "r")

json_object = json.load(raw)

for item in json_object:
    yiddish_title = None
    id = item["nybc_id"]
    ia_item = get_item(id)

    if 'title-alt-script' in ia_item.metadata:
        yiddish_title = ia_item.metadata['title-alt-script']
    id_title_dict[id] = yiddish_title
    print(id, yiddish_title)

dump = json.dumps(id_title_dict, ensure_ascii=False)
f = open("out.json", "a")
f.write(dump)
#item = get_item('<unique_item_identifier>')
#for k,v in item.metadata.items():
#    print(print(k,":",v))
