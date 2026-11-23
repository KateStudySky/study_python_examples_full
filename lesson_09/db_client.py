from sqlalchemy import create_engine, text


class StudentTable:
    __scripts = {
        "select_all": text("SELECT * FROM student"),
        "select_by_id": text("SELECT * FROM student WHERE user_id = :user_id"),
        "insert": text("""
            INSERT INTO student (user_id, level, education_form, subject_id) 
            VALUES (:user_id, :level, :education_form, :subject_id)
        """),
        "update": text("""
            UPDATE student 
            SET level = :level, education_form = :education_form 
            WHERE user_id = :user_id
        """),
        "delete": text("DELETE FROM student WHERE user_id = :user_id")
    }

    def __init__(self, connection_string):
        self.__db = create_engine(connection_string)

    def get_all(self):
        with self.__db.connect() as conn:
            result = conn.execute(self.__scripts["select_all"])
            return result.mappings().all()

    def get_by_id(self, user_id):
        with self.__db.connect() as conn:
            result = conn.execute(self.__scripts["select_by_id"], {"user_id": user_id})
            return result.mappings().all()

    def create(self, user_id, level="Beginner", education_form="Full-time", subject_id=1):
        with self.__db.connect() as conn:
            conn.execute(self.__scripts["insert"], {
                "user_id": user_id,
                "level": level,
                "education_form": education_form,
                "subject_id": subject_id
            })
            conn.commit()

    def update(self, user_id, level, education_form):
        with self.__db.connect() as conn:
            conn.execute(self.__scripts["update"], {
                "user_id": user_id,
                "level": level,
                "education_form": education_form
            })
            conn.commit()

    def delete(self, user_id):
        with self.__db.connect() as conn:
            conn.execute(self.__scripts["delete"], {"user_id": user_id})
            conn.commit()
