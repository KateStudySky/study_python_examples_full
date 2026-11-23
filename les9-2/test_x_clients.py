from company_api import CompanyApi
from company_table import CompanyTable


base_url = "http://139.100.217.192:8000"
db_connection_string = "postgresql://qa:skyqa@139.100.217.192:5432/x_clients"

api = CompanyApi(base_url)
db = CompanyTable(db_connection_string)


def test_get_companies():
    api_result = api.get_company_list()
    db_result = db.get_companies()
    assert len(api_result) == len(db_result)


def test_get_active_companies():
    filtered_list = api.get_company_list(params_to_add={"active": "true"})
    db_list = db.get_active_companies()
    assert len(filtered_list) == len(db_list)


def test_add_new():
    body = api.get_company_list()
    len_before = len(body)

    name = "Autotest"
    descr = "Descr"
    result = api.create_company(name, descr)
    new_id = result["id"]

    body = api.get_company_list()
    len_after = len(body)

    db.delete(new_id)

    assert len_after - len_before == 1

    found = False
    for company in body:
        if company["id"] == new_id:
            found = True
            assert company["name"] == name
            assert company["description"] == descr
            break

    assert found


def test_get_one_company():
    name = "Skypro"
    description = "descr"
    db.create(name, description)
    max_id = db.get_max_id()

    new_company = api.get_company(max_id)

    db.delete(max_id)

    assert new_company["name"] == name
    assert new_company["description"] == description
    assert new_company["is_active"] is True


def test_edit():
    name = "Skypro"
    db.create(name)
    max_id = db.get_max_id()

    new_name = "Updated"
    new_descr = "_upd_"
    edited = api.edit_company(max_id, new_name, new_descr)

    db.delete(max_id)

    assert edited["name"] == new_name
    assert edited["description"] == new_descr


def test_delete():
    name = "Skypro"
    db.create(name)
    max_id = db.get_max_id()

    deleted = api.delete_company(max_id)

    assert deleted["company_id"] == max_id
    assert deleted["detail"] == "Компания успешно удалена"

    rows = db.get_company_by_id(max_id)
    assert len(rows) == 0


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
