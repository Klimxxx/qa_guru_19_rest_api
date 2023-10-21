import allure
from allure_commons._allure import step
from allure_commons.types import Severity
import jsonschema
import requests

from utils import load_schema

@allure.title('GET users statuscode is ok')
@allure.label('owner', 'Klim')
@allure.tag('smoke tests')
@allure.severity(Severity.CRITICAL)
def test_get_users_statuscode_is_ok():
    with step("Get request"):
        response = requests.get(url='https://reqres.in/api/users')
    with step("Check status code == 200"):
        assert response.status_code == 200

@allure.title('GET users per page')
@allure.label('owner', 'Klim')
@allure.tag('smoke tests')
@allure.severity(Severity.CRITICAL)
def test_get_users_per_page():
    with step("Get request"):
        response = requests.get(url='https://reqres.in/api/users', params={"per_page": 1})
    with step("Load schema from directory"):
        schema = load_schema("get_users.json")
    with step("Check status code"):
        assert response.status_code == 200
    with step("Check len data == 1"):
        assert len(response.json()["data"]) == 1
    with step("Check per page == 1"):
        assert response.json()["per_page"] == 1
    with step("Check validation schema"):
        jsonschema.validate(response.json(), schema)

@allure.title('GET headers')
@allure.label('owner', 'Klim')
@allure.tag('smoke tests')
@allure.severity(Severity.CRITICAL)
def test_headers():
    with step("Get request"):
        response = requests.get(url='https://reqres.in/api/users', headers={"Accept": "*/*"})
    with step("Check status code == 200"):
        assert response.status_code == 200

@allure.title('GET single user')
@allure.label('owner', 'Klim')
@allure.tag('smoke tests')
@allure.severity(Severity.CRITICAL)
def test_single_user():
    with step("Get request"):
        response = requests.get(url='https://reqres.in/api/users/2')
    with step("Check status code == 200"):
        assert response.status_code == 200

@allure.title('GET no single user')
@allure.label('owner', 'Klim')
@allure.tag('smoke tests')
@allure.severity(Severity.CRITICAL)
def test_no_single_user():
    with step("Get request"):
        response = requests.get(url='https://reqres.in/api/users/23')
    with step("Check status code == 404"):
        assert response.status_code == 404

@allure.title('POST users users schema validation')
@allure.label('owner', 'Klim')
@allure.tag('smoke tests')
@allure.severity(Severity.CRITICAL)
def test_post_users_schema_validation():
    with step("Load schema from directory"):
        schema = load_schema("post_users.json")
    with step("Post request"):
        response = requests.post(
            url='https://reqres.in/api/users',
            json={
                "name": "morpheus",
                "job": "leader"
            }
        )
    with step("Check status code == 201"):
        assert response.status_code == 201
    with step("Check validation schema"):
        jsonschema.validate(response.json(), schema)
    with step("Check json name == morpheus"):
        assert response.json()['name'] == 'morpheus'

@allure.title('POST register_unsuccessful')
@allure.label('owner', 'Klim')
@allure.tag('smoke tests')
@allure.severity(Severity.CRITICAL)
def test_register_unsuccessful():
    with step("Post request"):
        response = requests.post(
            url='https://reqres.in/api/register',
            json={
                "email": "sydney@fife"
            }
        )
    with step("Check status code == 400"):
        assert response.status_code == 400
    with step("Check json == {'error': 'Missing password'}"):
        assert response.json() == {'error': 'Missing password'}

@allure.title('DELETE user')
@allure.label('owner', 'Klim')
@allure.tag('smoke tests')
@allure.severity(Severity.CRITICAL)
def test_delete_user():
    with step("Delete request"):
        response = requests.delete(url='https://reqres.in/api/users/2')
    with step("Check status code == 204"):
        assert response.status_code == 204

@allure.title('POST register user')
@allure.label('owner', 'Klim')
@allure.tag('smoke tests')
@allure.severity(Severity.CRITICAL)
def test_register_user():
    with step("Post request"):
        response = requests.post(url='https://reqres.in/api/register', data={
            "email": "eve.holt@reqres.in",
            "password": "pistol"
        })
    with step("Check status code == 200"):
        assert response.status_code == 200
    with step("Check json id == 4"):
        assert response.json()["id"] == 4
    with step("Check json token not empty"):
        assert response.json()["token"] is not None

@allure.title('PATCH update user')
@allure.label('owner', 'Klim')
@allure.tag('smoke tests')
@allure.severity(Severity.CRITICAL)
def test_update_user():
    with step("Patch request"):
        response = requests.patch(url='https://reqres.in/api/users/2', data={
            "name": "morpheus",
            "job": "zion resident"
        })
    with step("Check status code == 200"):
        assert response.status_code == 200
    with step("Check json job == zion resident"):
        assert response.json()["job"] == "zion resident"
