from psycopg2 import connect, OperationalError
from models import User, Message
from clcrypto import check_password
import argparse

HOST = 'localhost'
USER = 'postgres'
PASSWORD = 'coderslab'
DATABASE = 'test_db'


def main():
    try:
        cnx = connect(host=HOST, user=USER, password=PASSWORD, database=DATABASE)
        cnx.autocommit = True
        cursor = cnx.cursor()

        parser = argparse.ArgumentParser()
        parser.add_argument("-u", "--username", help="username")
        parser.add_argument("-p", "--password", help="password")
        parser.add_argument("-t", "--to", help="send message to:")
        parser.add_argument("-s", "--send", help="message text")
        parser.add_argument("-l", "--list", help="list all users", action='store_true')
        args = parser.parse_args()

        if args.username and args.password and args.list:
            list_messages(cursor, args.username, args.password)

        elif args.username and args.password and args.to and args.send:
            send_message(cursor, args.username, args.password, args.to, args.send)

        else:
            parser.print_help()

    except OperationalError:
        print('There was an error connecting to the server!')


def list_messages(cursor, username, password):
    if check_credentials(cursor, username, password):
        all_messages = Message.load_all_messages(cursor)
        for message in all_messages:
            print(message)

def send_message(cursor, username, password, addressee, text):

    if check_credentials(cursor, username, password):
        user_to = User.load_user_by_username(cursor, addressee)
        if user_to:
            if len(text) < 255:
                to_id = user_to.id
                user_from = User.load_user_by_username(cursor, username)
                from_id = user_from.id
                message = Message(from_id, to_id, text)
                message.save_to_db(cursor)
                print('Message was sent!')
            else:
                print('Message too long!')
        else:
            print('This addressee does not exist!')
def check_credentials(cursor, username, password):
    user = User.load_user_by_username(cursor, username)
    if not user:
        print('Wrong username!')
        return False
    elif not check_password(password, user.hashed_password):
        print('Wrong password!')
        return False
    else:
        return True

if __name__ == '__main__':
    main()
