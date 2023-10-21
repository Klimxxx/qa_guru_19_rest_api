import jsonschema
import allure
import json

from requests import sessions
from curlify import to_curl
from allure_commons.types import AttachmentType

from utils import load_schema

project = 'azalia'
def azalia_api(method, url, **kwargs):
    new_url = 'https://staging.azalia-now.ru/api' + url

    with allure.step(f'{method.upper()} {url}'):
        with sessions.Session() as session:
            response = session.request(method=method, url=new_url, **kwargs)
            message = to_curl(response.request)

            allure.attach(body=message.encode('utf8'), name='Curl',
                          attachment_type=AttachmentType.TEXT, extension='txt')
            try:
                allure.attach(body=json.dumps(response.json(), indent=4).encode('utf8'), name='Response Json',
                              attachment_type=AttachmentType.JSON, extension='json')
            except:
                allure.attach(body=response.content, name='Response',
                              attachment_type=AttachmentType.TEXT, extension='txt')
    return response


def test_get_banners_status_code_is_ok():
    response = azalia_api('get', url='/banners')

    assert response.status_code == 200


def test_get_banners_schema_validation():
    schema = load_schema(project, 'get_banners.json')

    response = azalia_api(
        'get',
        url='/banners')
    jsonschema.validate(response.json(), schema)


def test_get_flower_instructions_status_code_is_ok():
    response = azalia_api(
        'get',
        url='/flower-instructions')
    assert response.status_code == 200


def test_get_flower_instructions_schema_validation():
    schema = load_schema(project, 'get_flower_instructions.json')

    response = azalia_api(
        'get',
        url='/flower-instructions')

    jsonschema.validate(response.json(), schema)

def test_get_me_unauthorized_status_code_is_ok():
    response = azalia_api(
        'get',
        url='/v2/me')
    assert response.status_code == 401

def test_get_me_unauthorized_schema_validation():
    schema = load_schema(project, 'get_me.json')

    response = azalia_api(
        'get',
        url='/v2/me')

    jsonschema.validate(response.json(), schema)

def test_get_cities_pagination_status_code_is_ok():
    response = azalia_api(
        'get',
        url='/cities?pagination=-1&populate=shops&sort=id')
    assert response.status_code == 200

def test_get_products_pagination_status_code_is_ok():
    response = azalia_api(
        'get',
        url='/products?pagination[limit]=1&fields=id')
    assert response.status_code == 200
