from flask import Flask, flash, redirect, render_template, request, session, abort
import os
import sqlite3
import database as db

# Initial database setup
conn = sqlite3.connect("my_database.db")
try:
    db.setup_database(conn)
except Exception as e:
    print(str(e))
    pass
conn.close()

# Instantiate the Flask Web App
app = Flask(__name__)
app.secret_key = "super secret key"

conn = sqlite3.connect("my_database.db")
admin = "admin"

cur = conn.cursor()
cur.execute("SELECT * FROM t_user WHERE c_username = ?", (admin,))
data = cur.fetchone()

if data is None:
    db.define_admin(conn)

conn.close()

currentUser = None

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/admin_home')
def admin_home():
    return render_template('admin_home.html')

@app.route('/user_home')
def user_home():
    return render_template('user_home.html')

@app.route('/index', methods=['POST'])
def do_admin_login():
 
    username_str = str(request.form['username'])
    password_str = request.form['password']

    conn = sqlite3.connect("my_database.db")

    if db.validate_user(conn, username_str)==True and db.validate_pass(conn, password_str)==True:
        if username_str=="admin" and password_str=="admin":
            session['logged_in_boss'] = True
            conn.close()
            return render_template('login_success_admin.html')
        else:
            session['logged_in'] = True
            global currentUser
            currentUser = username_str
            conn.close()
            return render_template('login_success_user.html')

    else:
        conn.close()
        return render_template('error_login.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/add_user')
def add_user():
    return render_template('add_user.html')

@app.route('/process_add_user_admin/', methods=['POST'])
def process_add_user_admin():
    username_str = request.form['username']
    password_str = request.form['password']
    name_str = request.form['name']
    address_str = request.form['address']
    credit_str = request.form['credit']

    conn = sqlite3.connect("my_database.db")

    cur = conn.cursor()
    cur.execute("SELECT * FROM t_user WHERE c_username = ?", (username_str,))
    data = cur.fetchone()

    if credit_str.isdigit() and data is None:

        conn=sqlite3.connect("my_database.db")

        db.add_user(conn, name_str, username_str, password_str, address_str, credit_str)
        db.show_user_default(conn)

        conn.close()

        return render_template('process_success_admin.html')

    else:
        return render_template('error_registration_admin.html')

@app.route('/process_add_user/', methods=['POST'])
def process_add_user():
    username_str = request.form['username']
    password_str = request.form['password']
    name_str = request.form['name']
    address_str = request.form['address']
    credit_str = request.form['credit']

    conn = sqlite3.connect("my_database.db")

    cur = conn.cursor()
    cur.execute("SELECT * FROM t_user WHERE c_username = ?", (username_str,))
    data = cur.fetchone()

    if credit_str.isdigit() and data is None:

        conn=sqlite3.connect("my_database.db")

        db.add_user(conn, name_str, username_str, password_str, address_str, credit_str)
        db.show_user_default(conn)

        conn.close()

        return render_template('success_registration.html')

    else:
        return render_template('error_registration.html')

@app.route('/view_user')
def view_user():
    conn = sqlite3.connect('my_database.db')

    aftermath = db.show_user_default(conn)
    jlist = []

    for record in aftermath:
        slimmy = {}

        slimmy['id'] = record[0]
        slimmy['name'] = record[1]
        slimmy['username'] = record[2]
        slimmy['address'] = record[3]
        slimmy['credit'] = record[4]
        slimmy['type'] = record[5]
        slimmy['status'] = record[6]

        jlist.append(slimmy)

    conn.close()

    return render_template('/view_user.html', jlist=jlist)

@app.route('/process_delete_suspend', methods=['POST'])
def process_delete_suspend():
    delete_str = request.form['delete']
    suspend_str = request.form['suspend']

    if delete_str.isdigit() and suspend_str.isdigit() and delete_str != suspend_str:

        conn = sqlite3.connect("my_database.db")

        db.delete_user(conn, delete_str)
        db.suspend_user(conn, suspend_str)
        db.show_user_default(conn)

        conn.commit()
        conn.close()

        return render_template('process_success_admin.html')

    else:
        return render_template('process_error_delsus.html')

@app.route('/add_product')
def add_product():
    return render_template('add_product.html')

@app.route('/process_add_product', methods=['POST'])
def process_add_product():
    name = request.form['name']
    brand = request.form['brand']
    quantity = request.form['quantity']
    price = request.form['price']
    type = request.form['type']
    desc = request.form['desc']

    if quantity.isdigit() and price.isdigit():
        conn = sqlite3.connect("my_database.db")

        db.add_product(conn, name, brand, quantity, price, type, desc)

        conn.close()

        return render_template('process_success_admin.html')
    else:
        return render_template('process_error_addprod.html')

@app.route('/view_product')
def view_product():
    conn = sqlite3.connect('my_database.db')
    type = "phone"
    aftermath = db.show_products(conn, type)
    jlist1 = []
    jlist2 = []
    jlist3 = []

    for record in aftermath:
        slimmy = {}

        slimmy['id'] = record[0]
        slimmy['name'] = record[1]
        slimmy['brand'] = record[2]
        slimmy['quantity'] = record[3]
        slimmy['price'] = record[4]
        slimmy['description'] = record[5]

        jlist1.append(slimmy)

    type="laptop"
    aftermath = db.show_products(conn, type)
    for record in aftermath:
        slimmy = {}

        slimmy['id'] = record[0]
        slimmy['name'] = record[1]
        slimmy['brand'] = record[2]
        slimmy['quantity'] = record[3]
        slimmy['price'] = record[4]
        slimmy['description'] = record[5]

        jlist2.append(slimmy)

    type="tablet"
    aftermath = db.show_products(conn, type)
    for record in aftermath:
        slimmy = {}

        slimmy['id'] = record[0]
        slimmy['name'] = record[1]
        slimmy['brand'] = record[2]
        slimmy['quantity'] = record[3]
        slimmy['price'] = record[4]
        slimmy['description'] = record[5]

        jlist3.append(slimmy)

    conn.close()

    return render_template('view_product.html', jlist1=jlist1, jlist2=jlist2, jlist3=jlist3)

@app.route('/del_up_product', methods=['POST'])
def del_up_product():
    delete = request.form['delete']
    id = request.form['id']
    quantity = request.form['quantity']

    if delete.isdigit() and id.isdigit() and quantity.isdigit() and delete!=id:
        conn = sqlite3.connect("my_database.db")
        db.update_product(conn, id, quantity)
        db.delete_product(conn, delete)
        conn.commit()
        conn.close()

        return render_template('process_success_admin.html')

    else:
        return render_template('process_error_delup.html')

@app.route('/users/')
def user_index():
    global currentUser
    user = currentUser

    conn = sqlite3.connect('my_database.db')

    #validate = db.validate_suspension(conn, user)

    #if validate==True:

    aftermath = db.show_user_profile(conn, user)
    jlist = []
    jlist1 = []
    jlist2 = []

    for record in aftermath:
        slimmy = {}

        slimmy['name'] = record[0]
        slimmy['address'] = record[1]
        slimmy['credit'] = record[2]

        jlist.append(slimmy)

    aftermath = db.show_cart(conn, user)

    for record in aftermath:
        slimmy = {}

        slimmy['name'] = record[0]
        slimmy['price'] = record[1]

        jlist1.append(slimmy)

    aftermath = db.select_sum(conn, user)

    for record in aftermath:
        slimmy = {}

        slimmy['price'] = record[0]

        jlist1.append(slimmy)

    conn.close()

    return render_template('user_home.html', jlist=jlist, jlist1=jlist1, jlist2=jlist2)

    #else:
        #return render_template('account_suspended.html')
	
@app.route('/process_confirm_cart')
def process_confirm_cart():
    return render_template('checkout_success.html')


@app.route('/user_view_product')
def user_view_product():
    conn = sqlite3.connect('my_database.db')
    type = "phone"
    aftermath = db.show_products(conn, type)
    jlist1 = []
    jlist2 = []
    jlist3 = []

    for record in aftermath:
        slimmy = {}

        slimmy['id'] = record[0]
        slimmy['name'] = record[1]
        slimmy['brand'] = record[2]
        slimmy['quantity'] = record[3]
        slimmy['price'] = record[4]
        slimmy['description'] = record[5]

        jlist1.append(slimmy)

    type="laptop"
    aftermath = db.show_products(conn, type)
    for record in aftermath:
        slimmy = {}

        slimmy['id'] = record[0]
        slimmy['name'] = record[1]
        slimmy['brand'] = record[2]
        slimmy['quantity'] = record[3]
        slimmy['price'] = record[4]
        slimmy['description'] = record[5]

        jlist2.append(slimmy)

    type="tablet"
    aftermath = db.show_products(conn, type)
    for record in aftermath:
        slimmy = {}

        slimmy['id'] = record[0]
        slimmy['name'] = record[1]
        slimmy['brand'] = record[2]
        slimmy['quantity'] = record[3]
        slimmy['price'] = record[4]
        slimmy['description'] = record[5]

        jlist3.append(slimmy)

    conn.close()

    return render_template('view_product_user.html', jlist1=jlist1, jlist2=jlist2, jlist3=jlist3)

@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    prod_id = request.form['prod_id']

    global currentUser
    user = currentUser

    if prod_id.isdigit():
        conn = sqlite3.connect('my_database.db')
        cur = conn.cursor()
        cur.execute('SELECT c_id FROM t_user WHERE c_username = "{}"'.format(user))
        data = cur.fetchone()

        db.add_to_cart(conn, data, prod_id)

        conn.close()
        return render_template('success_add_to_cart.html')

    else:
        return render_template('process_error_add_cart.html')

@app.route('/user_view_product_price')
def user_view_product_price():
    conn = sqlite3.connect('my_database.db')
    type = "phone"
    aftermath = db.sort_price(conn, type)
    jlist1 = []
    jlist2 = []
    jlist3 = []

    for record in aftermath:
        slimmy = {}

        slimmy['id'] = record[0]
        slimmy['name'] = record[1]
        slimmy['brand'] = record[2]
        slimmy['quantity'] = record[3]
        slimmy['price'] = record[4]
        slimmy['description'] = record[5]

        jlist1.append(slimmy)

    type="laptop"
    aftermath = db.sort_price(conn, type)
    for record in aftermath:
        slimmy = {}

        slimmy['id'] = record[0]
        slimmy['name'] = record[1]
        slimmy['brand'] = record[2]
        slimmy['quantity'] = record[3]
        slimmy['price'] = record[4]
        slimmy['description'] = record[5]

        jlist2.append(slimmy)

    type="tablet"
    aftermath = db.sort_price(conn, type)
    for record in aftermath:
        slimmy = {}

        slimmy['id'] = record[0]
        slimmy['name'] = record[1]
        slimmy['brand'] = record[2]
        slimmy['quantity'] = record[3]
        slimmy['price'] = record[4]
        slimmy['description'] = record[5]

        jlist3.append(slimmy)

    conn.close()

    return render_template('view_product_price.html', jlist1=jlist1, jlist2=jlist2, jlist3=jlist3)

@app.route('/process_limit', methods=['POST'])
def limit():
    left_limit_str = request.form['left_limit']
    right_limit_str = request.form['right_limit']

    if left_limit_str.isdigit() and right_limit_str.isdigit():

        conn = sqlite3.connect('my_database.db')
        type = "phone"
        aftermath = db.limit_price(conn, type, left_limit_str, right_limit_str)
        jlist1 = []
        jlist2 = []
        jlist3 = []

        for record in aftermath:
            slimmy = {}

            slimmy['id'] = record[0]
            slimmy['name'] = record[1]
            slimmy['brand'] = record[2]
            slimmy['quantity'] = record[3]
            slimmy['price'] = record[4]
            slimmy['description'] = record[5]

            jlist1.append(slimmy)

        type = "laptop"
        aftermath = db.limit_price(conn, type, left_limit_str, right_limit_str)
        for record in aftermath:
            slimmy = {}

            slimmy['id'] = record[0]
            slimmy['name'] = record[1]
            slimmy['brand'] = record[2]
            slimmy['quantity'] = record[3]
            slimmy['price'] = record[4]
            slimmy['description'] = record[5]

            jlist2.append(slimmy)

        type = "tablet"
        aftermath = db.limit_price(conn, type, left_limit_str, right_limit_str)
        for record in aftermath:
            slimmy = {}

            slimmy['id'] = record[0]
            slimmy['name'] = record[1]
            slimmy['brand'] = record[2]
            slimmy['quantity'] = record[3]
            slimmy['price'] = record[4]
            slimmy['description'] = record[5]

            jlist3.append(slimmy)

        conn.close()

        return render_template('view_product_limit.html', jlist1=jlist1, jlist2=jlist2, jlist3=jlist3)

    else:
        return render_template('process_error_add_cart.html')