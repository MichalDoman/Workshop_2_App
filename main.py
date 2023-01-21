from psycopg2 import connect, OperationalError
from models import User, Message
from clcrypto import check_password
import argparse

HOST = 'localhost'
USER = 'postgres'
PASSWORD = 'coderslab'
DATABASE = 'test_db'

def delete_user(cursor, username, password):
    user = User.load_user_by_username(cursor, username)
    print(user)
    if check_password(password, user.hashed_password) and username == user.username:
        user.delete(cursor)
        print(user.delete(cursor))
def list_users(cursor):
    all_users = User.load_all_users(cursor)
    for user in all_users:
        print(user)

def main():
    try:
        cnx = connect(host=HOST, user=USER, password=PASSWORD, database=DATABASE)
        cnx.autocommit = True
        cursor = cnx.cursor()

        parser = argparse.ArgumentParser()
        parser.add_argument("-u", "--username", help="username")
        parser.add_argument("-p", "--password", help="password")
        parser.add_argument("-n", "--new_pass", help="new password")
        parser.add_argument("-l", "--list", help="list users", action='store_true')
        parser.add_argument("-d", "--delete", help="delete user", action='store_true')
        parser.add_argument("-e", "--edit", help="edit user info")
        args = parser.parse_args()

        # if args.username:
        #     pass
        # elif args.password:
        #     pass
        # elif args.new_pass:
        #     pass
        if args.list:
            list_users(cursor)
        elif args.username and args.password and args.delete:
            delete_user(cursor, args.username, args.password)
        # elif args.edit:
        #     pass
        else:
            parser.print_help()

    except OperationalError:
        print('There was an error connecting to the server!')


if __name__ == '__main__':
    main()
