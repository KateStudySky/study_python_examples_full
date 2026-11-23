import allure
from sqlalchemy import create_engine, text

class CompanyTable:
    __scripts = {
        "select_all": text("SELECT * FROM company WHERE deleted_at IS NULL"),
        "select_active": text("SELECT * FROM company WHERE \"is_active\" = true AND deleted_at IS NULL"),
        "delete_by_id": text("DELETE FROM company WHERE id = :id_to_delete"),
        "insert_new": text("INSERT INTO company(\"name\", \"description\") VALUES (:new_name, :new_descr)"),
        "get_max_id": text("SELECT MAX(\"id\") FROM company WHERE deleted_at IS NULL"),
        "select_by_id": text("SELECT * FROM company WHERE id = :select_id AND deleted_at IS NULL")
    }

    def __init__(self, connection_string):
        self.__db = create_engine(connection_string)

    @allure.step("БД. Запросить список организаций")
    def get_companies(self):
        conn = self.__db.connect()
        query = conn.execute(self.__scripts["select_all"])
        # Добавляем вложение с SQL-запросом
        allure.attach(str(self.__scripts["select_all"]), 'SQL', allure.attachment_type.TEXT)
        rows = query.mappings().all()
        conn.close()
        return rows

    @allure.step("БД. Запросить список активных организаций")
    def get_active_companies(self):
        conn = self.__db.connect()
        query = conn.execute(self.__scripts["select_active"])
        allure.attach(str(self.__scripts["select_active"]), 'SQL', allure.attachment_type.TEXT)
        rows = query.mappings().all()
        conn.close()
        return rows

    @allure.step("БД. Получить компанию по {id}")
    def get_company_by_id(self, id):
        conn = self.__db.connect()
        query = conn.execute(self.__scripts["select_by_id"], {"select_id": id})
        allure.attach(str(self.__scripts["select_by_id"]), 'SQL', allure.attachment_type.TEXT)
        company = query.mappings().all()
        conn.close()
        return company

    @allure.step("БД. Удалить организацию по {id}")
    def delete(self, id):
        conn = self.__db.connect()
        conn.execute(self.__scripts["delete_by_id"], {"id_to_delete": id})
        # Добавляем вложение с SQL-запросом
        allure.attach(str(self.__scripts["delete_by_id"]), 'SQL', allure.attachment_type.TEXT)
        conn.commit()
        conn.close()

    @allure.step("БД. Создать организацию с названием {name}")
    def create(self, name, description=""):
        conn = self.__db.connect()
        conn.execute(
            self.__scripts["insert_new"],
            {"new_name": name, "new_descr": description}
        )
        # Добавляем вложение с SQL-запросом
        allure.attach(str(self.__scripts["insert_new"]), 'SQL', allure.attachment_type.TEXT)
        conn.commit()
        conn.close()

    @allure.step("БД. Получить максимальный id организации")
    def get_max_id(self):
        conn = self.__db.connect()
        query = conn.execute(self.__scripts["get_max_id"])
        allure.attach(str(self.__scripts["get_max_id"]), 'SQL', allure.attachment_type.TEXT)
        max_id = query.scalar()
        conn.close()
        return max_id
