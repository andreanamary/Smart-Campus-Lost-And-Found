from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

DATABASE = "database.db"

def get_connection():
    return sqlite3.connect(DATABASE)


@app.route('/')
def home():
    return render_template("home.html")


@app.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == "POST":

        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            "INSERT INTO users(fullname,email,password) VALUES(?,?,?)",
            (
                request.form['fullname'],
                request.form['email'],
                request.form['password']
            )
        )

        connection.commit()
        connection.close()

        return redirect('/login')

    return render_template("register.html")


@app.route('/login', methods=['GET','POST'])
def login():

    if request.method=="POST":

        connection=get_connection()
        cursor=connection.cursor()

        cursor.execute(
            "SELECT * FROM users WHERE email=? AND password=?",
            (
                request.form['email'],
                request.form['password']
            )
        )

        user=cursor.fetchone()

        connection.close()

        if user:
            return redirect('/dashboard')

        return "<h2>Invalid Email or Password</h2>"

    return render_template("login.html")


@app.route('/dashboard')
def dashboard():

    connection=get_connection()
    cursor=connection.cursor()

    cursor.execute("SELECT COUNT(*) FROM users")
    total_users=cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM lost_items")
    total_lost=cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM found_items")
    total_found=cursor.fetchone()[0]

    connection.close()

    return render_template(
        "dashboard.html",
        total_users=total_users,
        total_lost=total_lost,
        total_found=total_found
    )


@app.route('/report_lost', methods=['GET','POST'])
def report_lost():

    if request.method=="POST":

        connection=get_connection()
        cursor=connection.cursor()

        cursor.execute("""
        INSERT INTO lost_items
        (item_name,category,location,lost_date,description)
        VALUES(?,?,?,?,?)
        """,
        (
            request.form['item_name'],
            request.form['category'],
            request.form['location'],
            request.form['lost_date'],
            request.form['description']
        ))

        connection.commit()
        connection.close()

        return redirect('/dashboard')

    return render_template("report_lost.html")


@app.route('/report_found', methods=['GET','POST'])
def report_found():

    if request.method=="POST":

        connection=get_connection()
        cursor=connection.cursor()

        cursor.execute("""
        INSERT INTO found_items
        (item_name,category,location,found_date,description)
        VALUES(?,?,?,?,?)
        """,
        (
            request.form['item_name'],
            request.form['category'],
            request.form['location'],
            request.form['found_date'],
            request.form['description']
        ))

        connection.commit()
        connection.close()

        return redirect('/dashboard')

    return render_template("report_found.html")
@app.route('/logout')
def logout():
    return redirect('/')

@app.route('/search')
def search():

    connection=get_connection()
    cursor=connection.cursor()

    cursor.execute("""
    SELECT item_name,
           category,
           location,
           lost_date,
           description
    FROM lost_items
    ORDER BY id DESC
    """)

    items=cursor.fetchall()

    connection.close()

    return render_template(
        "search.html",
        items=items
    )


if __name__=="__main__":
    app.run(debug=True)