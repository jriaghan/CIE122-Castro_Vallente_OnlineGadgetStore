import sqlite3

conn = sqlite3.connect("my_database.db")

def activate_foreign_key(conn):
    query = "PRAGMA foreign_keys = ON;"
    cur = conn.cursor()
    result = cur.execute(query)
    print("Result: " + str(result.fetchall()))
    conn.commit()

def setup_database(conn):
    table_name = "t_product"

    columns = "("
    columns += "c_id INTEGER PRIMARY KEY, "
    columns += "c_name VARCHAR(128),"
    columns += "c_brand VARCHAR (128),"
    columns += "c_quantity INTEGER, "
    columns += "c_price INTEGER, "
    columns += "c_type VARCHAR(8), "
    columns += "c_desc VARCHAR(512)"
    columns += ")"

    query = "CREATE TABLE {} {};".format(table_name, columns)
    print(query)

    cur = conn.cursor()
    result = cur.execute(query)
    print("Result: " + str(result.fetchall()))
    conn.commit()

    table_name = "t_user"

    columns = "("
    columns += "c_id INTEGER PRIMARY KEY, "
    columns += "c_name VARCHAR(128),"
    columns += "c_username VARCHAR (64), "
    columns += "c_password VARCHAR(128), "
    columns += "c_address VARCHAR (512), "
    columns += "c_credit VARCHAR(128), "
    columns += "c_type VARCHAR(10), "
    columns += "c_status VARCHAR (10)"
    columns += ")"

    query = "CREATE TABLE {} {};".format(table_name, columns)
    print(query)

    cur = conn.cursor()
    result = cur.execute(query)
    print("Result: " + str(result.fetchall()))
    conn.commit()

    table_name = "t_cart"

    columns = "("
    columns += "c_id INTEGER PRIMARY KEY, "
    columns += "c_user_id INTEGER, "
    columns += "c_prod_id INTEGER, "
    columns += "FOREIGN KEY (c_user_id) REFERENCES t_user (c_id), "
    columns += "FOREIGN KEY (c_prod_id) REFERENCES t_product (c_id)"
    columns += ")"

    query = "CREATE TABLE {} {};".format(table_name, columns)
    print(query)

    cur = conn.cursor()
    result = cur.execute(query)
    print("Result: " + str(result.fetchall()))
    conn.commit()

def add_product(conn, name, brand, quantity, price, type, desc):
    table_name = "t_product"
    columns = "( c_name, c_brand, c_quantity, c_price, c_type, c_desc )"

    values = ' ("{}", "{}","{}", "{}", "{}","{}" ) '.format(name, brand, quantity, price, type, desc)

    query = "INSERT INTO {} {} VALUES {}".format(table_name, columns, values)

    cur = conn.cursor()
    result = cur.execute(query)
    print("Result: " + str(result.fetchall()))
    conn.commit()
    return

def add_user(conn, name, username, password, address, credit):
    type = "USER"
    status = "ACTIVE"
    table_name = "t_user"
    columns = "( c_name, c_username, c_password, c_address, c_credit, c_type, c_status)"
    values = ' ( "{}", "{}", "{}", "{}", "{}", "{}", "{}" ) '.format(name, username, password, address, credit, type, status)

    query = "INSERT INTO {} {} VALUES {}".format(table_name, columns, values)

    cur = conn.cursor()
    result = cur.execute(query)
    print("Result: " + str(result.fetchall()))
    conn.commit()
    return

def add_to_cart(conn, user_id, prod_id):
    table_name = "t_cart"
    columns = "( c_user_id, c_prod_id )"
    values = ' ( "{}", "{}" ) '.format(user_id, prod_id)

    query = "INSERT INTO {} {} VALUES {}".format(table_name, columns, values)

    cur = conn.cursor()
    result = cur.execute(query)
    print("Result: " + str(result.fetchall()))
    conn.commit()
    return

def delete_product(conn, id):
    query = 'DELETE FROM t_product WHERE c_id =  "{}" '.format(id)

    cur = conn.cursor()
    cur.execute(query)
    result = cur.fetchall()
    print(cur.description)
    print(result)
    return result

def update_product(conn, id, quantity):
    cur = conn.cursor()
    cur.execute('UPDATE t_product SET c_quantity = {} WHERE c_id = {}'.format(quantity, id))
    result = cur.fetchall()
    print(cur.description)
    print(result)
    return result

def delete_user(conn, id):
    query = 'DELETE FROM t_user WHERE c_id = "{}" '.format(id)

    cur = conn.cursor()
    cur.execute(query)
    result = cur.fetchall()
    print(cur.description)
    print(result)
    return result

def suspend_user(conn, id):
    query = 'UPDATE t_user SET c_type = "SUSPENDED" WHERE c_id = "{}" '.format(id)

    cur = conn.cursor()
    cur.execute(query)
    result = cur.fetchall()
    print(cur.description)
    print(result)
    return result

def show_user_default(conn):
    query = "SELECT c_id, c_name, c_username, c_address, c_credit, c_type, c_status FROM t_user"

    cur = conn.cursor()
    cur.execute(query)
    result = cur.fetchall()
    print(cur.description)
    print(result)
    return result
	
def show_user_profile(conn, name):
    query = 'SELECT c_name, c_address, c_credit FROM t_user WHERE c_username = "{}" '.format(name)
	
    cur = conn.cursor()
    cur.execute(query)
    result = cur.fetchall()
    print(cur.description)
    print(result)
    return result
	
def show_cart(conn, name):
    query = 'SELECT c_id FROM t_user WHERE c_username = "{}" '.format(name)
    cur = conn.cursor()
    cur.execute(query)
    result = cur.fetchone()
	
    query = 'SELECT TP.c_name, TP.c_price FROM t_product AS TP, t_cart AS TC WHERE TC.c_user_id="{}" AND TC.c_prod_id=TP.c_id'.format(result)
    cur = conn.cursor()
    cur.execute(query)
    result = cur.fetchall()
	
    print(cur.description)
    print(result)
    return result

#default sort is by name
def show_products(conn, type):
    query = 'SELECT c_id, c_name, c_brand, c_quantity, c_price, c_desc FROM t_product WHERE c_type = "{}" ORDER BY c_name ASC'.format(type)
    
    cur = conn.cursor()
    cur.execute(query)
    result = cur.fetchall()
    print(cur.description)
    print(result)
    return result

def sort_price(conn, type):
    query = 'SELECT c_id, c_name, c_brand, c_quantity, c_price, c_desc FROM t_product WHERE c_type = "{}" ORDER BY c_price ASC'.format(type)
    
    cur = conn.cursor()
    cur.execute(query)
    result = cur.fetchall()
    print(cur.description)
    print(result)
    return result

def limit_price(conn, type, leftlimit, rightlimit):
    query = 'SELECT c_id, c_name, c_brand, c_quantity, c_price, c_desc FROM t_product WHERE c_type = "{}" AND c_price>="{}" AND c_price<="{}" ORDER BY c_price ASC'.format(type, leftlimit, rightlimit)
	
    cur = conn.cursor()
    cur.execute(query)
    result = cur.fetchall()
    print(cur.description)
    print(result)
    return result

def define_admin(conn):
    name = "Administrator"
    username = "admin"
    password = "admin"
    address = "ADMU"
    credit = "N/A"
    type = "ADMIN"
    status = "ACTIVE"

    table_name = "t_user"
    columns = "( c_name, c_username, c_password, c_address, c_credit, c_type, c_status)"
    values = ' ( "{}", "{}", "{}", "{}", "{}", "{}", "{}" ) '.format(name, username, password, address, credit, type, status)

    query = "INSERT INTO {} {} VALUES {}".format(table_name, columns, values)

    cur = conn.cursor()
    result = cur.execute(query)
    print("Result: " + str(result.fetchall()))
    conn.commit()
    return
	
def validate_user(conn, user):
    for name in (user):
        cur = conn.cursor()
        cur.execute("SELECT count(*) FROM t_user WHERE c_username = ?", (user,))
        data = cur.fetchone()[0]
        if data==0:
            return False
        else:
            return True
			
def validate_pass(conn, pw):
    for name in (pw):
        cur = conn.cursor()
        cur.execute("SELECT count(*) FROM t_user WHERE c_password = ?", (pw,))
        data = cur.fetchone()[0]
        if data==0:
            return False
        else:
            return True

def validate_register(conn, username):
    for name in (username):
        cur = conn.cursor()
        cur.execute("SELECT * FROM t_user WHERE c_username = ?", (username,))
        data = cur.fetchone()
        if data == username:
            return False
        else:
            return True

def validate_suspension(conn, username):
    cur = conn.cursor()
    cur.execute("SELECT c_status FROM t_user WHERE c_username = ?", (username,))
    data = cur.fetchone()
    sus = "SUSPENDED"
    act = "ACTIVE"
    if data == sus:
        return False
    elif data == act:
        return True

def select_sum(conn, username):
    query = 'SELECT c_id FROM t_user WHERE c_username = "{}" '.format(username)
    cur = conn.cursor()
    cur.execute(query)
    result = cur.fetchone()

    query = 'SELECT SUM(TP.c_price) FROM t_product AS TP, t_cart AS TC WHERE TC.c_user_id="{}" AND TC.c_prod_id=TP.c_id'.format(result)
    cur = conn.cursor()
    cur.execute(query)
    result = cur.fetchall()

    print(cur.description)
    print(result)
    return result