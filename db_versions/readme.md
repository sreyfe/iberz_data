This is a folder containing database versions and scripts for [Iberz: a database of
translations into Yiddish](https://w3id.org/iberz). 
A more thorough description of the data will follow. For now, a few explanatory 
notes:

The data is primarily kept in two 
YAML documents: main and source. Main contains translations, source contains
source-texts. The main YAML references source texts by their id's. 

Entries in "main" each represent a single translation. Each translation can be printed
in multiple editions, which in turn can consist of multiple volumes.

The "year" field in the highest level of the entries in "main" is equivalent to 
the earliest year among individual editions. It is a convenient abstraction.

The JSON files
which begin with "combined" are an index used to more efficiently search the data.
These JSON's are produced using the combine_to_json.py script found in the scripts
folder.
