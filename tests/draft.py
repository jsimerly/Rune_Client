import os
import sys


current_file = os.path.abspath(__file__)
current_dir = os.path.dirname(current_file)
parent_dir = os.path.dirname(current_dir)
grandparent_dir = os.path.dirname(parent_dir)
sys.path.insert(0, grandparent_dir)

from src.main import Client
from src.user.user import User

def connect_and_start_game(username: str):
    client = Client()
    client.network.send_message(user=None, type='login', serialized_message={'username': username})
    
    while not User.is_logged_in:
        client.network.run_one()
        messages = client.network.read_queue()
        for message in messages:
            message = client.network.decode_json(message)
            if message['type'] == 'login':
                user = User(user=message['data']['user'])
    
    message = {'start_looking': True}
    client.network.send_message(user=user.serialized, type='match_making', serialized_message=message)
    client.run()

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Please provide a username as a command line argument.")
        sys.exit(1)
    username = sys.argv[1]
    connect_and_start_game(username)