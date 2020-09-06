import json
import sys
from datetime import datetime
import time

from fbchat import Client, ThreadType


def send(arguments):
    login_data = json.loads(arguments[1])
    content = arguments[2]
    recipient = arguments[3]
    group = arguments[4]
    action = arguments[5] if len(arguments) > 5 else datetime.now()

    try:
        action_time = action.split("T")[1].split(":")
        hour = int(action_time[0])
        minute = int(action_time[1])
        action_date = action.split("T")[0].split("-")
        year = int(action_date[0])
        month = int(action_date[1])
        day = int(action_date[2])

        execution_datetime = datetime(year=year, month=month, day=day, hour=hour, minute=minute)
        while execution_datetime > datetime.now():
            time.sleep(1)
    except IndexError:
        pass

    cookies = {}
    try:
        with open(f'session_{login_data["email"]}.json', 'r') as f:
            cookies = json.load(f)
    except:
        pass

    if group == "True":
        thread_type = ThreadType.GROUP
    else:
        thread_type = ThreadType.USER

    # Attempt a login with the session, and if it fails, just use the email & password
    client = Client(login_data["email"], login_data["password"], session_cookies=cookies, logging_level=50)
    client.sendMessage(content, thread_id=int(recipient), thread_type=thread_type)

    # Save the session again
    with open(f'session_{login_data["email"]}.json', 'w') as f:
        json.dump(client.getSession(), f)


if __name__ == "__main__":
    send(sys.argv)
