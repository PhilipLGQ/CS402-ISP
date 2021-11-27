import populate
from flask import Flask
from flask import request, jsonify
import pymysql

app = Flask(__name__)
username = "root"
password = "root"
database = "hw5_ex2"


# This method returns a list of messages in a json format such as
# [
# { "name": <name>, "message": <message> },
# { "name": <name>, "message": <message> },
# ...
# ]
# If this is a POST request and there is a parameter "name" given, then only
# messages of the given name should be returned.
# If the POST parameter is invalid, then the response code must be 500.


@app.route("/messages", methods=["GET", "POST"])
def messages():
    try:
        with db.cursor() as cursor:
            if request.method == 'GET':
                sql_query = "SELECT name, message FROM messages"
                cursor.execute(sql_query)
                json = []

                for name, message in cursor.fetchall():
                    json.append({"name": name, "message": message})
                return jsonify(json), 200

            elif request.method == 'POST':
                form = request.form
                name_key = form.get("name", None)
                json = []
                if name_key is None:
                    return 'A name is required when POST', 500

                sql_query = "SELECT name, message FROM messages WHERE name LIKE %s"
                cursor.execute(sql_query)

                for name, message in cursor.fetchall():
                    json.append({"name": name, "message": message})
                return jsonify(json)

            else:
                return 'Well, what do you want?', 500

    except pymysql.err.ProgrammingError:
        print('Malicious input may included.')
        return "Don't you ever try to hack me :)", 500


# This method returns the list of users in a json format such as
# { "users": [ <user1>, <user2>, ... ] }
# This methods should limit the number of users if a GET URL parameter is given
# named limit. For example, /users?limit=4 should only return the first four
# users.
# If the paramer given is invalid, then the response code must be 500.
@app.route("/users", methods=["GET"])
def contact():
    try:
        with db.cursor() as cursor:
            sql_query = "SELECT name FROM users"
            args = request.args
            names = []
            limit = args.get("limit", None)

            if limit is not None:
                sql_query += "LIMIT 0, %s"
                cursor.execute(sql_query, int(limit))
            else:
                cursor.execute(sql_query)

            # name is of tuple size 1, use name[0] to unpack the value
            for name in cursor.fetchall():
                names.append(name[0])

            json = {"users": names}
            return jsonify(json), 200

    except (pymysql.err.ProgrammingError, ValueError):
        return "Don't you ever try to hack me :)", 500


if __name__ == "__main__":
    db = pymysql.connect("localhost",
                         username,
                         password,
                         database)
    with db.cursor() as cursor:
        populate.populate_db(cursor)
        db.commit()
    print("[+] database populated")

    app.run(host='0.0.0.0', port=80)
