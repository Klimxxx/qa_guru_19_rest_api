import json
import os





def load_schema(project, name):
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), f'json_schemas/{project}', name)
    with open(path) as file:
        json_schema = json.loads(file.read())
    return json_schema
