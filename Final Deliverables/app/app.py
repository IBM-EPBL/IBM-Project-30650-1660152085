import ibm_db
from flask import (Flask, make_response, redirect, render_template, request,
                   session, url_for)

try:
    dsn = ("DATABASE={0};"
           "HOSTNAME={1};"
           "PORT={2};"
           "SECURITY={3};"
           "UID={4};"
           "PWD={5};"
           ).format('bludb', "98538591-7217-4024-b027-8baa776ffad1.c3n41cmd0nqnrk39u98g.databases.appdomain.cloud", 30875, "SSL", "pxz37891", "uS8RsXGIjXNHbwHF")
    conn = ibm_db.connect(dsn, '', '')
    print("Connection Success")
except:
    print(ibm_db.conn_errormsg())

app = Flask(__name__)
app.secret_key = "PERSONALEXPENSETRACKERAPP"


@app.route('/')
def index():
    if session.get("email") != None:
        return redirect(url_for('dashboard'))
    return render_template("index.html")


def all_transactions():
    uid = get_user('uid')
    all_transactions = []
    result = ibm_db.exec_immediate(
        conn, "SELECT * FROM TRANSACTIONS WHERE UID='"+uid+"'")
    while ibm_db.fetch_assoc(result) != False:
        data = {
            'time': ibm_db.result(result, 1),
            'amount': ibm_db.result(result, 3),
            'note': ibm_db.result(result, 4),
            'category': ibm_db.result(result, 6),
            'type': ibm_db.result(result, 5)
        }
        all_transactions.append(data)
    return all_transactions


@app.route('/dashboard')
def dashboard():
    email = session.get('email')
    if email == None:
        return redirect(url_for('index'))
    alltransactions = all_transactions()
    income = 0 
    expense = 0
    limit = int(get_user('limit'))
    for transaction in alltransactions:
        if transaction['type'] == 'Income':
            income += transaction['amount']
        else:
            expense += transaction['amount']
    return render_template("dashboard.html", data={"username": get_user('name'), "transactions": alltransactions[0:5], "limit": limit, "income": income, "expense": expense, "transaction":alltransactions})


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == "POST":
        email = request.form['email']
        pwd = request.form['password']
        verifyEmailQuery = ibm_db.prepare(
            conn, "SELECT * FROM USERS WHERE email=?")
        ibm_db.bind_param(verifyEmailQuery, 1, email)
        ibm_db.execute(verifyEmailQuery)
        while ibm_db.fetch_row(verifyEmailQuery) != False:
            if pwd != ibm_db.result(verifyEmailQuery, 3):
                return render_template('login.html', data={'email': email, 'error': 'Incorrect Password'})
            session['email'] = ibm_db.result(verifyEmailQuery, 2)
            return redirect(url_for('dashboard'))
        return render_template('login.html', data={'error': "Email doesn't Exists"})
    else:
        return render_template('login.html', data=None)


@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == "POST":
        name = request.form['name']
        email = request.form['email']
        pwd = request.form['password']

        verifyEmailQuery = ibm_db.prepare(
            conn, "SELECT * FROM USERS WHERE email=?")
        ibm_db.bind_param(verifyEmailQuery, 1, email)
        ibm_db.execute(verifyEmailQuery)
        while ibm_db.fetch_row(verifyEmailQuery) != False:
            return render_template('register.html', data={'name': name, 'error': 'Email Already Exists'})

        query = ibm_db.prepare(
            conn, "INSERT INTO USERS(name,email,pass) VALUES (?,?,?)")
        ibm_db.bind_param(query, 1, name)
        ibm_db.bind_param(query, 2, email)
        ibm_db.bind_param(query, 3, pwd)
        ibm_db.execute(query)
        return redirect(url_for('login'))
    else:
        return render_template('register.html', data=None)


@app.route('/logout')
def logout():
    session.pop('email', None)
    response = make_response(redirect(url_for('index')))
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    return response



def get_user(data):
    email = session.get('email')

    result = ibm_db.exec_immediate(
        conn, "SELECT * FROM USERS WHERE EMAIL='"+email+"'")
    while ibm_db.fetch_row(result) != False:
        return str(ibm_db.result(result, 0 if data == 'uid' else (1 if data=="name" else 4)))
    return None


@app.route('/add', methods=['POST'])
def add():
    amount = request.form['amount']
    note = request.form['note']
    category = request.form['category']
    typeofTransaction = request.form['type']
    uid = get_user('uid')
    query = ibm_db.prepare(
        conn, "INSERT INTO TRANSACTIONS(UID,AMOUNT,NOTE,TYPE,CATEGORY) VALUES (?,?,?,?,?)")
    ibm_db.bind_param(query, 1, uid)
    ibm_db.bind_param(query, 2, amount)
    ibm_db.bind_param(query, 3, note)
    ibm_db.bind_param(query, 4, typeofTransaction)
    ibm_db.bind_param(query, 5, category)
    ibm_db.execute(query)
    return redirect(url_for('dashboard'))


@app.route('/add_limit', methods=['POST'])
def add_limit():
    amount = request.form['amount']
    email = session.get('email')
    ibm_db.exec_immediate(
        conn, "UPDATE USERS SET MONTHLIMIT="+amount+" WHERE EMAIL='"+email+"' ")
    return redirect(url_for('dashboard'))


@app.route('/transactions')
def transactions():
    return render_template('transactions.html', data={"transactions": all_transactions()[0:5]})


if (__name__ == "__main__"):
    app.run(host='0.0.0.0', port=5000, debug=True)
