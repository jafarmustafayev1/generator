import psycopg2
from contex_manager import DatabaseConnect

db_info = {
    'host': 'localhost',
    'database': 'nt',
    'user': 'postgres',
    'password': '1',
    'port': 5432
}

class Person:
    def __init__(self, full_name, age):
        self.full_name = full_name
        self.age = age

    def save(self):
        with DatabaseConnect(**db_info) as conn:
            with conn.cursor() as cur:
                insert_person_query = '''insert into person(full_name, age)
                values (%s, %s);
                '''
                data = (self.full_name, self.age)

                cur.execute(insert_person_query, data)
                conn.commit()
                print('Person successfully saved')

    @staticmethod
    def get_all_persons():
        with DatabaseConnect(**db_info) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT full_name, age FROM person;")
                result = cur.fetchall()
                persons = [Person(full_name=row[0], age=row[1]) for row in result]
                return persons

    @staticmethod
    def get_one_person(person_id):
        with DatabaseConnect(**db_info) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT full_name, age FROM person WHERE id = %s;", (person_id,))
                result = cur.fetchone()
                if result:
                    return Person(full_name=result[0], age=result[1])
                else:
                    return None

sherali = Person('Sherali Olimov', 25)
sherali.save()

persons = Person.get_all_persons()
for person in persons:
    print(f'Name: {person.full_name}, Age: {person.age}')

person = Person.get_one_person(1)
if person:
    print(f'Name: {person.full_name}, Age: {person.age}')
else:
    print("Person not found")
