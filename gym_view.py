
from mysql import connector
from datetime import datetime


class Dbconnect:
    def get_connection(self):
        try:
            connection = connector.connect(
                host="localhost",
                user="root",
                password="JAITHRIm2005@7736",
                database="gym_db"
            )
            return connection

        except Exception as e:
            print(e)
            return None


class GymMemberManager(Dbconnect):

    def get(self):
        connection = None
        cursor = None

        try:
            connection = super().get_connection()
            if connection is None:
                return []

            cursor = connection.cursor()
            query = "SELECT * FROM member"
            cursor.execute(query)

            records = cursor.fetchall()
            print(records)
            return records

        except Exception as e:
            print(e)
            return []

        finally:
            if cursor:
                cursor.close()
            if connection and connection.is_connected():
                connection.close()

    def post(self, **kwargs):
        connection = None
        cursor = None

        try:
            connection = super().get_connection()
            if connection is None:
                return

            cursor = connection.cursor()

            query = """
                INSERT INTO member
                (name, place, plan, mobile, fee, joining_date)
                VALUES (%s, %s, %s, %s, %s, %s)
            """

            values = (
                kwargs["name"],
                kwargs["place"],
                kwargs["plan"],
                kwargs["mobile"],
                kwargs["fee"],
                kwargs["joining_date"]
            )

            cursor.execute(query, values)
            connection.commit()

            print("New member added successfully...!")

        except Exception as e:
            print(e)

        finally:
            if cursor:
                cursor.close()
            if connection and connection.is_connected():
                connection.close()

    def get_object(self, id=None):
        connection = None
        cursor = None

        try:
            connection = super().get_connection()
            if connection is None:
                return None

            cursor = connection.cursor()

            query = "SELECT * FROM member WHERE id = %s"
            values = (id,)

            cursor.execute(query, values)
            record = cursor.fetchone()

            return record

        except Exception as e:
            print(e)
            return None

        finally:
            if cursor:
                cursor.close()
            if connection and connection.is_connected():
                connection.close()

    def retrieve(self, id=None):
        record = self.get_object(id=id)

        if record is not None:
            print(record)
        else:
            print("Member not found...!")

    def delete(self, id=None):
        connection = None
        cursor = None

        try:
            connection = super().get_connection()
            if connection is None:
                return

            cursor = connection.cursor()

            query = "DELETE FROM member WHERE id = %s"
            values = (id,)

            cursor.execute(query, values)
            connection.commit()

            if cursor.rowcount > 0:
                print("Member deleted successfully...!")
            else:
                print("Member not found...!")

        except Exception as e:
            print(e)

        finally:
            if cursor:
                cursor.close()
            if connection and connection.is_connected():
                connection.close()

    def put(self, id=None, **kwargs):
        connection = None
        cursor = None

        try:
            allowed_fields = {
                "name", "place", "plan",
                "mobile", "fee", "joining_date"
            }

            if not kwargs or not set(kwargs).issubset(allowed_fields):
                print("Invalid or empty update data...!")
                return

            connection = super().get_connection()
            if connection is None:
                return

            cursor = connection.cursor()

            placeholder = ""

            for k in kwargs.keys():
                placeholder += k + " = %s, "

            placeholder = placeholder.rstrip(", ")

            query = f"UPDATE member SET {placeholder} WHERE id = %s"

            values = list(kwargs.values())
            values.append(id)

            cursor.execute(query, values)
            connection.commit()

            if cursor.rowcount > 0:
                print("Member updated successfully...!")
            else:
                print("Member not found or no changes made...!")

        except Exception as e:
            print(e)

        finally:
            if cursor:
                cursor.close()
            if connection and connection.is_connected():
                connection.close()


member_instance = GymMemberManager()

member_instance.get()

member_instance.post(name="Vishnu", place="Thrissur", plan="3 months", mobile="8113970680", fee=2000, joining_date=datetime.today().date())
member_instance.post(name="Mahesh", place="Kochi", plan="6 months", mobile="9876543210", fee=3500, joining_date=datetime.today().date())
member_instance.post(name="Arjun", place="Kottayam", plan="1 year", mobile="9123456780", fee=6000, joining_date=datetime.today().date())

print("____________")

member_instance.retrieve(3)

print("____________")

# member_instance.delete(1)

print("_____After deletion________")
member_instance.get()

print("_____Updation_____")

member_instance.put(2, name="Mahesh")

member_instance.retrieve(2)
