from flask import Flask, request, jsonify
import pymysql

app = Flask(__name__)
host = 'sql6.freesqldatabase.com'
user = 'sql6683632'
password = 'yaE9DX7wkS'
database = 'sql6683632'

try:
    connection = pymysql.connect(host=host, user=user, password=password, database=database)
    print('connection sucessfull')
except pymysql.Error as e:
    print(f"Error: {e}")

@app.route("/get-user", methods=['GET'])
def get_all_users():
    try:
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        select_all_query = "SELECT * FROM users"
        cursor.execute(select_all_query)
        users = cursor.fetchall()
        print(jsonify(users))
        return jsonify(users), 200

    except pymysql.Error as e:
        print('error while getting users as',e)
        return jsonify({"error": f"Database error: {e}"}), 500

    finally:
        if cursor:
            cursor.close()
    try:
        cursor = connection.cursor(pymysql.cursors.DictCursor)

        select_query = f"SELECT * FROM users WHERE user_id = '{user_id}'"
        cursor.execute(select_query)

        user = cursor.fetchone()
        if user:
            return jsonify(user), 200
        else:
            return jsonify({"error": "User not found"}), 404

    except pymysql.Error as e:
        return jsonify({"error": f"Database error: {e}"}), 500

    finally:
        if cursor:
            cursor.close()
@app.route("/create-user", methods=['POST'])
def create_user():
    try:
        data = request.get_json()

        cursor = connection.cursor()

        insert_query = "INSERT INTO users (user_id, name, Revenue, email) VALUES (%s, %s, %s, %s)"
        cursor.execute(insert_query, (data['user_id'], data['name'], data['Revenue'], data['email']))

        connection.commit()

        return jsonify({"message": "User created successfully"}), 201

    except pymysql.Error as e:
        return jsonify({"error": f"Database error: {e}"}), 500

    finally:
        if cursor:
            cursor.close()


if __name__ == "__main__":
    app.run(debug=True , host='0.0.0.0')
