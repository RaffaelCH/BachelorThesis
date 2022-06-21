import sys
import json


if len(sys.argv) < 2:
    print("Usage: py json-combiner file_path_1.json [file_path_2.json [file_path_3.json [...]]]")
    exit()



combined_json = {'links': [], 'nodes': []}


for file in sys.argv[1:]:
    with open(file) as json_file:
        file_content = json_file.read()
        json_content = json.loads(file_content)

        for link in json_content['links']:
            combined_json['links'].append(link)
        
        for node in json_content['nodes']:
            combined_json['nodes'].append(node)


print(json.dumps(combined_json))