from app.database.setup import mysql_client, Products, Items


def initialise_mysql_database():
    cursor = mysql_client.cursor()
    with open('app/database/mysql_init.sql') as f:
        results = cursor.execute(f.read(), multi=True)
        for result in results:
            continue


def is_admin_username_taken(username):
    cursor = mysql_client.cursor()
    cursor.execute('USE `db.OSHES`;')
    cursor.execute('SELECT id FROM administrator WHERE id = %s', (username,))
    cursor.fetchone()

    return True if cursor.rowcount > 0 else False


def is_cust_username_taken(username):
    cursor = mysql_client.cursor()
    cursor.execute('USE `db.OSHES`;')
    cursor.execute('SELECT id FROM customer WHERE id = %s', (username,))
    cursor.fetchone()

    return True if cursor.rowcount > 0 else False


def insert_administrator(username, name, gender, phone, password):
    cursor = mysql_client.cursor()
    cursor.execute('USE `db.OSHES`;')
    cursor.execute('INSERT INTO administrator (id, name, gender, phone, password) VALUES (%s,%s, %s, %s, %s)',
                   (username, name, gender, phone, password))
    mysql_client.commit()

    return cursor.lastrowid


def insert_customer(username, name, gender, email, address, phone, password):
    cursor = mysql_client.cursor()
    cursor.execute('USE `db.OSHES`;')
    cursor.execute(
        'INSERT INTO customer (id, name, gender, email, address, phone, password) VALUES (%s,%s, %s, %s, %s, %s, %s)',
        (username, name, gender, email, address, phone, password))
    mysql_client.commit()

    return cursor.lastrowid


def validate_administrator_login(username, password):
    cursor = mysql_client.cursor()
    cursor.execute('USE `db.OSHES`;')
    cursor.execute('SELECT * FROM administrator WHERE id = %s AND password = %s', (username, password))
    results = cursor.fetchone()

    if results is None:
        return False, "", "", "", ""

    return True, results[0], results[1], results[2], results[3]


def validate_customer_login(username, password):
    cursor = mysql_client.cursor()
    cursor.execute('USE `db.OSHES`;')
    cursor.execute('SELECT * FROM customer WHERE id = %s AND password = %s', (username, password))
    results = cursor.fetchone()

    if results is None:
        return False, "", "", "", "", "", ""

    return True, results[0], results[1], results[2], results[3], results[4], results[5]


def get_categories():
    return list(Products.find().distinct('Category'))


def get_models():
    return list(Products.find().distinct('Model'))


def get_colors():
    return list(Items.find().distinct('Color'))


def get_factories():
    return list(Items.find().distinct('Factory'))


def get_power_supplies():
    return list(Items.find().distinct('PowerSupply'))


def get_production_years():
    return list(Items.find().distinct('ProductionYear'))


def get_filtered_results(admin=False, category=None, model=None,
                         color=None, factory=None, power_supply=None, production_year=None):
    filter_by = {}
    if admin:
        projection = ['ProductID', 'Category', 'Model', 'Price ($)', 'Warranty (months)', 'Cost ($)']
    else:
        projection = ['ProductID', 'Category', 'Model', 'Price ($)', 'Warranty (months)']
    if category:
        filter_by['Category'] = category
    elif model:
        filter_by['Model'] = model

    res = Products.find(filter_by, projection)
    final = []
    for product in list(res):
        product = {
            'IID': product['ProductID'],
            'Category': product['Category'],
            'Model': product['Model'],
            'Cost ($)': product['Cost ($)'],
            'Price ($)': product['Price ($)'],
            'Warranty (months)': product['Warranty (months)'],
        } if admin else {
            'IID': product['ProductID'],
            'Category': product['Category'],
            'Model': product['Model'],
            'Price ($)': product['Price ($)'],
            'Warranty (months)': product['Warranty (months)'],
        }
        filter_criteria = {'Category': product['Category'], 'Model': product['Model']}
        if color:
            filter_criteria['Color'] = color
        if factory:
            filter_criteria['Factory'] = factory
        if power_supply:
            filter_criteria['PowerSupply'] = power_supply
        if production_year:
            filter_criteria['ProductionYear'] = production_year
        filter_res = list(Items.find(filter_criteria))
        temp = list(product.values())
        temp.append(len(list(filter(lambda x: x['PurchaseStatus'] == 'Unsold', filter_res))))
        if admin:
            temp.append(len(list(filter(lambda x: x['PurchaseStatus'] == 'Sold', filter_res))))
        final.append(temp)

    return final


def find_product_by_category_and_model(category, model):
    return Products.find_one({'Category': category, 'Model': model})


def find_item_by_id(item_id):
    item = Items.find_one({'ItemID': item_id})
    product = find_product_by_category_and_model(item['Category'], item['Model'])
    return {**item, **product}
