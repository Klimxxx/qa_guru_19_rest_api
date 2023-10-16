import jsonschema
import requests

from tests.utils import load_schema


def test_get_users_statuscode_is_ok():
    response = requests.get(url='https://reqres.in/api/users')
    assert response.status_code == 200


def test_get_users_statuscode_per_page():
    response = requests.get(url='https://reqres.in/api/users', params={"per_page": 1})
    print(response.json())
    schema = load_schema("get_users.json")
    assert response.status_code == 200
    assert len(response.json()["data"]) == 1
    assert response.json()["per_page"] == 1
    jsonschema.validate(response.json(), schema)


def test_headers():
    response = requests.get(url='https://reqres.in/api/users', headers={"Accept": "*/*"})
    assert response.status_code == 200


def test_single_user():
    response = requests.get(url='https://reqres.in/api/users/2')
    print(response.text)
    assert response.status_code == 200


def test_single_user():
    response = requests.get(url='https://reqres.in/api/users/23')
    assert response.status_code == 404


def test_post_users_schema_validation():
    schema = load_schema("post_users.json")

    response = requests.post(
        url='https://reqres.in/api/users',
        json={
            "name": "morpheus",
            "job": "leader"
        }
    )

    assert response.status_code == 201
    jsonschema.validate(response.json(), schema)
    assert response.json()['name'] == 'morpheus'


def test_register_unsuccessful():
    response = requests.post(
        url='https://reqres.in/api/register',
        json={
            "email": "sydney@fife"
        }
    )
    print(response.json())
    assert response.status_code == 400
    assert response.json() == {'error': 'Missing password'}


def test_delete_user():
    response = requests.delete(url='https://reqres.in/api/users/2')
    assert response.status_code == 204


def test_register_user():
    response = requests.post(url='https://reqres.in/api/register', data={
        "email": "eve.holt@reqres.in",
        "password": "pistol"
    })
    assert response.status_code == 200
    assert response.json()["id"] == 4
    assert response.json()["token"] is not None


def test_update_user():
    response = requests.patch(url='https://reqres.in/api/users/2', data={
        "name": "morpheus",
        "job": "zion resident"
    })
    assert response.status_code == 200
    assert response.json()["job"] == "zion resident"
