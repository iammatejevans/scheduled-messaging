import json
import subprocess

from fbchat import Client, FBchatUserError
from flask import Flask, request, render_template, jsonify

app = Flask(__name__, template_folder="templates")


@app.route("/message/", methods=["GET", "POST"])
def message():
    if request.method == "POST":
        data = request.get_json()

        if "email" not in data or "password" not in data:
            return jsonify("Missing credentials")

        email = data["email"]
        password = data["password"]

        try:
            cookies = {}
            try:
                with open(f'session_{email}.json', 'r') as f:
                    cookies = json.load(f)
            except:
                pass

            client = Client(email, password, session_cookies=cookies, logging_level=50)

            with open(f'session_{email}.json', 'w') as f:
                json.dump(client.getSession(), f)

        except FBchatUserError:
            return jsonify("Wrong credentials")

        if "content" not in data or "recipient" not in data:
            return jsonify("Missing content")

        content = data["content"]
        recipient = data["recipient"]

        result_user = ""

        try:
            group = data["group"]
            if group == True:
                group = "True"
            else:
                group = "False"
        except KeyError:
            group = "False"

        if group == "True":
            users = client.searchForGroups(recipient)
            for user in users:
                if client.uid in user.participants:
                    result_user = user.uid
                    break

        else:
            users = client.searchForUsers(recipient)
            for user in users:
                if user.is_friend:
                    result_user = user.uid
                    break

        if not result_user:
            return jsonify("Recipient not found")

        login_data = json.dumps({"email": email, "password": password})

        try:
            action_time = data["action_time"]
        except KeyError:
            action_time = None

        if client:
            subprocess.Popen([
                "python",
                "send_message.py",
                login_data,
                content,
                result_user,
                group,
                action_time
            ])
            return jsonify("Success")

    if request.method == "GET":
        return render_template("message.html")
