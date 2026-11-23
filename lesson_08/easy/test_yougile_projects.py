import requests


BASE_URL = "https://ru.yougile.com"
TOKEN = "CkVx0aVE9lI0Tip8eMuzR9LEHstIt3h3t8PKxKh5RukodKa5sbe65OYNAaOJ6CUl"
ID_USER = "9cb5b2fc-ca2c-4a01-bafc-103ae55d2a57"
MY_HEADERS = {"Authorization": f"Bearer {TOKEN}",
              "Content-Type": "application/json"}
DATA = {"title": "New project", "users": {ID_USER: "admin"}}


def test_create_project():
    resp = requests.post(f"{BASE_URL}/api-v2/projects",
                         headers=MY_HEADERS,
                         json=DATA)

    assert resp.status_code == 201
    assert resp.json().get("id") is not None

    project_id = resp.json().get("id")
    requests.put(
        f"{BASE_URL}/api-v2/projects/{project_id}",
        headers=MY_HEADERS,
        json={"deleted": True},
    )


def test_update_project_title():
    resp = requests.post(f"{BASE_URL}/api-v2/projects",
                         headers=MY_HEADERS,
                         json=DATA)
    project_id = resp.json().get("id")

    new_data = {
        "title": "Updated title",
    }
    res_project = requests.put(
        f"{BASE_URL}/api-v2/projects/{project_id}",
        headers=MY_HEADERS,
        json=new_data
    )

    assert res_project.status_code == 200

    requests.put(
        f"{BASE_URL}/api-v2/projects/{project_id}",
        headers=MY_HEADERS,
        json={"deleted": True},
    )


def test_get_project():
    resp = requests.post(f"{BASE_URL}/api-v2/projects",
                         headers=MY_HEADERS,
                         json=DATA)
    project_id = resp.json().get("id")

    res_project = requests.get(
        f"{BASE_URL}/api-v2/projects/{project_id}",
        headers=MY_HEADERS
    )

    assert res_project.status_code == 200
    assert DATA.get("title") in res_project.json().get("title")

    requests.put(
        f"{BASE_URL}/api-v2/projects/{project_id}",
        headers=MY_HEADERS,
        json={"deleted": True},
    )


def test_create_project_no_title():
    resp = requests.post(
        f"{BASE_URL}/api-v2/projects",
        headers=MY_HEADERS,
        json={})

    assert resp.status_code == 400
    assert "title should not be empty" in resp.json()["message"]


def test_update_not_existing_project():
    new_data = {
        "title": "Updated title",
    }
    resp = requests.put(
        f"{BASE_URL}/api-v2/projects/99999999",
        headers=MY_HEADERS,
        json=new_data
    )

    assert resp.status_code == 404
    assert "Проект не найден" in resp.json()["message"]


def test_get_project_no_auth():
    resp = requests.post(
        f"{BASE_URL}/api-v2/projects",
        headers=MY_HEADERS,
        json=DATA)
    project_id = resp.json().get("id")

    res_project = requests.get(
        f"{BASE_URL}/api-v2/projects/{project_id}"
    )

    assert res_project.status_code == 401
    assert "Unauthorized" in res_project.json()["message"]
