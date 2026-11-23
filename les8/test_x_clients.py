import requests

from company_api import CompanyApi


base_url = "http://139.100.217.192:8000"

api = CompanyApi(base_url)


def test_simple_req():
    resp = requests.get(base_url + '/company/list')
    response_body = resp.json()
    first_company = response_body[0]
    assert first_company["name"] == "QA Студия 'ТестировщикЪ'"
    assert resp.status_code == 200
    assert resp.headers["Content-Type"] == "application/json"


def test_get_companies():
    body = api.get_company_list()
    assert len(body) > 0


def test_get_active_companies():
    full_list = api.get_company_list()
    filtered_list = api.get_company_list(params_to_add={"active": "true"})
    assert len(full_list) > len(filtered_list)


def test_add_new():
    body = api.get_company_list()
    len_before = len(body)

    name = "Autotest"
    descr = "Descr"
    api.create_company(name, descr)

    body = api.get_company_list()
    len_after = len(body)

    assert len_after - len_before == 1
    assert body[-1]["name"] == name
    assert body[-1]["description"] == descr


def test_get_one_company():
    name = "VS Code"
    descr = "IDE"
    result = api.create_company(name, descr)
    new_id = result["id"]

    new_company = api.get_company(new_id)

    assert new_company["name"] == name
    assert new_company["description"] == descr
    assert new_company["is_active"] is True


def test_edit():
    name = "Company to be edited"
    descr = "Edit me"
    result = api.create_company(name, descr)
    new_id = result["id"]

    new_name = "Updated"
    new_descr = "_upd_"

    edited = api.edit_company(new_id, new_name, new_descr)

    assert edited["name"] == new_name
    assert edited["description"] == new_descr


def test_delete():
    name = "Company to be deleted"
    descr = "Delete me"
    result = api.create_company(name, descr)
    new_id = result["id"]

    new_company = api.get_company(new_id)
    assert new_company["name"] == name
    assert new_company["description"] == descr
    assert new_company["is_active"] is True

    body = api.get_company_list()
    len_before = len(body)

    api.delete_company(new_id)

    body = api.get_company_list()
    len_after = len(body)
    assert len_before - len_after == 1

    deleted = api.get_company(new_id)
    assert deleted['detail'] == 'Компания не найдена'


def test_deactivate():
    name = "Company to be deactivated"
    result = api.create_company(name)
    new_id = result["id"]

    body = api.set_active_state(new_id, False)

    assert body["is_active"] is False


def test_deactivate_and_activate_back():
    name = "Company to be deactivated"
    result = api.create_company(name)
    new_id = result["id"]

    body_d = api.set_active_state(new_id, False)
    assert body_d["is_active"] is False

    body_a = api.set_active_state(new_id, True)
    assert body_a["is_active"] is True
