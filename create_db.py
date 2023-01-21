from psycopg2 import connect, OperationalError, ProgrammingError

HOST = 'localhost'
USER = 'postgres'
PASSWORD = 'coderslab'


def execute_sql(sql_code, db=None):
    try:
        cnx = connect(host=HOST, user=USER, password=PASSWORD, database=db)
        cnx.autocommit = True
        cursor = cnx.cursor()
        cursor.execute(sql_code)

    except OperationalError:
        print('There was an error connecting to the server!')


def create_db(db_name):
    sql = f"CREATE DATABASE {db_name};"
    try:
        execute_sql(sql)
        print("Database created successfully!")
    except ProgrammingError:
        print("Database already exists!")


def create_table(sql_code, db):
    try:
        execute_sql(sql_code, db)
        print("Table created successfully!")
    except ProgrammingError:
        print("Table already exists!")


def main():
    create_db('test_db')

    sql_users = 'CREATE TABLE Users(' \
                'id SERIAL PRIMARY KEY,' \
                'username varchar(255),' \
                'hashed_password varchar(80));'
    create_table(sql_users, 'test_db')

    sql_messages = 'CREATE TABLE Messages(' \
                   'id SERIAL PRIMARY KEY,' \
                   'from_id INT NOT NULL,' \
                   'to_id INT NOT NULL,' \
                   'creation_date TIMESTAMP,' \
                   'text TEXT,' \
                   'FOREIGN KEY(from_id) REFERENCES Users(id),' \
                   'FOREIGN KEY(to_id) REFERENCES Users(id));'
    create_table(sql_messages, 'test_db')


if __name__ == '__main__':
    main()
