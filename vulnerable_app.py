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

    # INTENTIONALLY VULNERABLE SQL INJECTION
    query = f"SELECT * FROM users WHERE name = ?"

    print("SQL:", query)

    try:
        cursor.execute(query)
        users = cursor.fetchall()

    except sqlite3.Error as e:
        # Do not crash Flask when sqlmap sends broken payloads
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
        <p>{{ user }}</p>
    {% else %}
        <p>No users found</p>
    {% endfor %}

    """, users=users)


if __name__ == "__main__":
    app.run(debug=True)
