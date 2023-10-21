import os
import json
import allure
from requests import sessions
from curlify import to_curl
from allure_commons.types import AttachmentType


def load_json_schema(project: str, name: str):
    if project == 'catfact':
        schemas_dir = 'tests/catfact/schemas'
    elif project == 'reqres':
        schemas_dir = 'tests/reqres/schemas'
    else:
        raise ValueError('Invalid project')

    schema_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), schemas_dir, name)
    with open(schema_path) as schema:
        return json.loads(schema.read())


def api_request(project, url, method='GET', **kwargs):
    base_urls = {
        "catfact": "https://catfact.ninja",
        "reqres": "https://reqres.in/api"
        }
    new_url = base_urls[project] + url

    with allure.step(f"{method.upper()}{new_url}"):
        with sessions.Session() as session:
            response = session.request(method=method, url=new_url, **kwargs)
            #response = requests.request("POST", url, data=payload, allow_redirects=False)
            message = to_curl(response.request)
            allure.attach(
                body=message.encode("utf-8"),
                name="Curl",
                attachment_type=AttachmentType.TEXT,
                extension='txt'
            )
            if not response.content:
                allure.attach(
                    body='empty response',
                    name='Empty Response',
                    attachment_type=AttachmentType.TEXT,
                    extension='txt'
                )
            else:
                allure.attach(
                    body=json.dumps(response.json(), indent=4).encode("utf-8"),
                    name="Response Json",
                    attachment_type=AttachmentType.JSON,
                    extension='json'
                )
    return response

