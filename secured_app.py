from flask import Flask, request, render_template_string
import sqlite3

app = Flask(__name__)

DATABASE = "data.db"


def get_db():
    return sqlite3.connect(DATABASE)


@app.route("/user")
def user():
    name = request.args.get("name", "")

    conn = get_db()
    cursor = conn.cursor()

    # SAFE: parameterized query
    query = "SELECT * FROM users WHERE name = ?"


    try:
        cursor.execute(query, (name,))
        users = cursor.fetchall()

    except sqlite3.Error as e:
        users = []
        error = str(e)

        conn.close()

        return render_template_string("""
        <h1>Database Error</h1>
        <p>{{ error }}</p>
        """, error=error), 500

    finally:
        conn.close()

    return render_template_string("""
    <h1>User Search</h1>

    <form>
        Name:
        <input name="name">
        <button>Search</button>
    </form>

    <h2>Results:</h2>

    {% for user in users %}
        <p>ID: {{ user[0] }}</p>
        <p>Name: {{ user[1] }}</p>
        <p>Email: {{ user[2] }}</p>
        <p>Age: {{ user[3] }}</p>
        <hr>
    {% else %}
        <p>No users found</p>
    {% endfor %}

    """, users=users)


if __name__ == "__main__":
    app.run(debug=True, port=5001)
