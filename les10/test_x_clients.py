import allure
from company_api import CompanyApi
from company_table import CompanyTable


@allure.epic("Компании")
@allure.severity("blocker")
class TestCompany:

    # В реальном проекте URL и Connection String берутся из конфигов
    api = CompanyApi("http://139.100.217.192:8000")
    db = CompanyTable("postgresql://qa:skyqa@139.100.217.192:5432/x_clients")

    @allure.id("SKYPRO-3")
    @allure.story("Создание компаний")
    @allure.feature("CREATE")
    @allure.title("Создание организации")
    @allure.description("Проверка создания новой компании через API и её наличия в БД")
    def test_add_new(self):
        # Шаг 1: Получаем количество компаний ДО
        with allure.step("Получить количество организаций ДО через БД"):
            body_before = self.db.get_companies()
            len_before = len(body_before)

        # Шаг 2: Создаем компанию через API
        with allure.step("Создать организацию через API"):
            name = "Autotest_Company"
            descr = "Description for autotest"
            result = self.api.create_company(name, descr)
            new_id = result["id"]

        # Шаг 3: Проверяем поля в БД
        with allure.step("Проверить, что поля новой организации в БД заполнены корректно"):
            body_after = self.db.get_companies()
            found = False
            for company in body_after:
                if company["id"] == new_id:
                    assert company["name"] == name
                    assert company["description"] == descr
                    found = True
                    break
            assert found, "Созданная компания не найдена в базе данных"

        # Шаг 4: Проверяем счетчик
        with allure.step("Проверить, что список ДО меньше списка ПОСЛЕ на 1"):
            assert len(body_after) - len_before == 1

        # Шаг 5: Чистим за собой
        with allure.step("Удалить из БД новую организацию"):
            self.db.delete(new_id)
