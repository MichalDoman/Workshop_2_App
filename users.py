from psycopg2 import connect, OperationalError
from main import HOST, USER, PASSWORD, DATABASE
from models import User
from clcrypto import check_password
import argparse


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
        parser.add_argument("-e", "--edit", help="edit user info", action='store_true')
        args = parser.parse_args()

        if args.username and args.password and not args.new_pass:
            create_user(cursor, args.username, args.password)

        elif args.username and args.password and args.new_pass and args.edit:
            edit_password(cursor, args.username, args.password, args.new_pass)

        elif args.username and args.password and args.delete:
            delete_user(cursor, args.username, args.password)

        elif args.list:
            list_users(cursor)

        else:
            parser.print_help()

    except OperationalError:
        print('There was an error connecting to the server!')


def create_user(cursor, username, password):
    user = User(username, password)
    all_users = User.load_all_users(cursor)
    usernames = []
    for user_object in all_users:
        usernames.append(user_object.username)

    if username in usernames:
        print('This username already exists!')
    else:
        if len(password) >= 8:
            user.save_to_db(cursor)
            print('Account created successfully!')
        else:
            print('Password is too short!')


def edit_password(cursor, username, password, new_pass):
    user = User.load_user_by_username(cursor, username)
    if not user:
        print('The user doesnt exist.')
    else:
        if check_password(password, user.hashed_password):
            if len(new_pass) >= 8:
                user.set_password(new_pass)
                user.save_to_db(cursor)
                print('Password changed successfully!')
            else:
                print('Password is too short!')


def delete_user(cursor, username, password):
    user = User.load_user_by_username(cursor, username)
    if not user:
        print('The user doesnt exist.')
    elif check_password(password, user.hashed_password) and username == user.username:
        user.delete(cursor)
        print('User deleted successfully!')


def list_users(cursor):
    all_users = User.load_all_users(cursor)
    for user in all_users:
        print(user)


if __name__ == '__main__':
    main()
