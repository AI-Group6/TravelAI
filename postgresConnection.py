import psycopg2
from psycopg2 import sql
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

#params
conn_params = {
    'dbname': 'postgres',
    'user': 'postgres',
    'password': 'postgres',
    'host': 'localhost',
    'port': 5432
}

# a function to get the chat history from the database
@app.route('/history', methods=['Get'])
def fetchHistory():
    try:
        username = request.args.get('username')
        #connect to db
        conn = psycopg2.connect(**conn_params)
        cursor = conn.cursor()

        #define sql query
        query = "SELECT * FROM chatHistory WHERE login = %s ORDER BY timestamp DESC"

        #execute query
        cursor.execute(query, (username,))

        #fetch all results
        chat_history = cursor.fetchall()

        #close cursor and connection
        cursor.close()
        conn.close()

        if chat_history:
            # Format the fetched data
            formatted_history = []
            for record in chat_history:
                login, title, response, timestamp = record

                # Format the timestamp
                formatted_timestamp = timestamp.strftime("%d/%m/%Y %H:%M")

                # Append formatted entry to list
                formatted_history.append({
                    'title': title,
                    'response': response,
                    'timestamp': formatted_timestamp
                })

            print("Chat history successfully fetched")
            return jsonify({'history': formatted_history})


        print("Chat history successfully fetched")
        return jsonify({'history': chat_history})

    except Exception as e:
        print(f"Error fetching chat history: {e}")
        return jsonify({'error': str(e)})

# a function to post AI response to the database
@app.route('/history', methods=['Post'])
def postHistory():
    try:
        data = request.json
        user_login = data.get('login')
        title_message = data.get('message')
        ai_response = data.get('response')
        #connect to db
        conn = psycopg2.connect(**conn_params)
        cursor = conn.cursor()

        #define sql query to insert data
        query = """
            INSERT INTO chatHistory (login, title, content, timestamp)
            VALUES (%s, %s, %s, NOW())
        """
        #execute query
        cursor.execute(query, (user_login, title_message, ai_response))

        #commit transaction 
        conn.commit()

        #close cursor & connection
        cursor.close()
        conn.close()

        print("AI response successfully posted to chatHistory")
        return jsonify({'success': True})

    except Exception as e:
        print(f"Error posting to chat history: {e}")
        return jsonify({'success': False})

#function to check if the given username and password are correct.
@app.route('/users', methods=['Get'])
def checkLogin():
    try:
        username = request.args.get('login')
        password = request.args.get('password')
        #connect to db
        conn = psycopg2.connect(**conn_params)
        cursor = conn.cursor()

        #define sql query
        query = "SELECT * FROM loginInfo WHERE login = %s AND password = %s"

        #execute query
        cursor.execute(query, (username, password))

        #fetch result
        result = cursor.fetchone()

        #close cursor and connection
        cursor.close()
        conn.close()

        if result:
            return jsonify({'exists': True})
        else: 
            raise Exception

    except Exception:
        print("Username or Password Incorrect")
        return jsonify({'exists': False})

#create login by posting user information
@app.route('/users', methods=['Post'])
def createUser():
    data = request.json
    username = data.get('login')
    print(username)
    password = data.get('password')
    print(password)
    try:

        #connect to db
        conn = psycopg2.connect(**conn_params)
        cursor = conn.cursor()

        #define sql query
        query = "SELECT * FROM loginInfo WHERE login = %s AND password = %s"

        #execute query
        cursor.execute(query, (username, password))

        #fetch result
        result = cursor.fetchone()

        #close cursor and connection
        cursor.close()
        conn.close()

        if result:
            raise Exception

    except Exception:
        print("User already Exists")
        return jsonify({'success': False})

    try:
        #connect to db
        conn = psycopg2.connect(**conn_params)
        cursor = conn.cursor()

        #define sql query to insert data
        query = """
            INSERT INTO loginInfo (login, password)
            VALUES (%s, %s)
        """
        #execute query
        cursor.execute(query, (username, password))

        #commit transaction 
        conn.commit()

        #close cursor & connection
        cursor.close()
        conn.close()

        print("New User Successfully Created")
        return jsonify({'success': True})

    except Exception as e:
        print(f"Error creating new user, please try again: {e}")
        return jsonify({'success': False})

if __name__ == '__main__':
    app.run(debug=True)