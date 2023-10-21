import jsonschema
import allure
import json

from requests import sessions
from curlify import to_curl
from allure_commons.types import AttachmentType

from utils import load_schema

project = 'reqres'
def reqres_api(method, url, **kwargs):
    new_url = 'https://reqres.in' + url

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


def test_get_users_status_code_is_ok():
    response = reqres_api(
        'get',
        url='/api/users'
    )

    assert response.status_code == 200


def test_get_users_schema_validation():
    schema = load_schema(project, 'get_users.json')

    response = reqres_api(
        'get',
        url='/api/users'
    )

    jsonschema.validate(response.json(), schema)


def test_get_single_user_status_code_is_ok():
    response = reqres_api(
        'get',
        url='/api/users/2'
    )

    assert response.status_code == 200


def test_get_single_user_schema_validation():
    schema = load_schema(project, 'get_single_user.json')

    response = reqres_api(
        'get',
        url='/api/users/2'
    )

    jsonschema.validate(response.json(), schema)


def test_post_users_status_code_is_ok():
    response = reqres_api(
        'post',
        url='/api/users/2',
        json={
            'name': "morpheus",
            'job': 'leader'
        }
    )

    assert response.status_code == 201


def test_post_users_schema_validation():
    schema = load_schema(project, 'post_users.json')

    response = reqres_api(
        'post',
        url='/api/users/2',
        json={
            'name': "morpheus",
            'job': 'leader'
        }
    )

    jsonschema.validate(response.json(), schema)


def test_post_users_response_body_data():
    response = reqres_api(
        'post',
        url='/api/users/2',
        json={
            'name': "morpheus",
            'job': 'leader'
        }
    )

    assert response.json()['name'] == 'morpheus'
    assert response.json()['job'] == 'leader'


def test_put_users_status_code_is_ok():
    response = reqres_api(
        'put',
        url='/api/users/2',
        json={
            'name': "morpheus",
            'job': 'resident'
        }
    )

    assert response.status_code == 200


def test_put_users_schema_validation():
    schema = load_schema(project, 'put_users.json')

    response = reqres_api(
        'put',
        url='/api/users/2',
        json={
            'name': "morpheus",
            'job': 'resident'
        }
    )

    jsonschema.validate(response.json(), schema)


def test_put_users_response_body_data():
    response = reqres_api(
        'put',
        url='/api/users/2',
        json={
            'name': "morpheus",
            'job': 'resident'
        }
    )

    assert response.json()['job'] == 'resident'


def test_delete_user_status_code_is_ok():
    response = reqres_api(
        'delete',
        url='/api/users/2'
    )

    assert response.status_code == 204
