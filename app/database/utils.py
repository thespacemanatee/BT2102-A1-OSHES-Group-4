import json

from app.database.setup import mysql_client, Products, Items


def initialise_mysql_database():
    Products.remove({})
    with open('data/products.json') as products:
        Products.insert_many(json.load(products))

    Items.remove({})
    with open('data/items.json') as items:
        Items.insert_many(json.load(items))

    cursor = mysql_client.cursor()
    with open('data/mysql_init.sql') as f:
        results = cursor.execute(f.read(), multi=True)
        for result in results:
            continue

    products = Products.find({}, {'_id': False})
    temp = []
    for product in products:
        temp.append(
            (product['ProductID'], product['Category'], product['Model'], product['Cost ($)'], product['Price ($)'],
             product['Warranty (months)']))
    cursor.executemany(
        'INSERT INTO product (id, category, model, cost, price, warranty) VALUES (%s, %s, %s, %s, %s, %s)', temp)

    mysql_client.commit()

    items = Items.find({}, {'_id': False})
    temp = []
    for item in items:
        product = find_product_by_category_and_model(item['Category'], item['Model'])
        temp.append(
            (item['ItemID'], item['Color'], item['PowerSupply'], item['Factory'], item['ProductionYear'],
             item['PurchaseStatus'], item['ServiceStatus'], product['ProductID']))
    cursor.executemany(
        'INSERT INTO item (id, colour, power_supply, factory, production_year, purchase_status, service_status,'
        ' product_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)',
        temp)

    mysql_client.commit()
    cursor.close()


def is_admin_username_taken(username):
    with mysql_client.cursor() as cursor:
        cursor.execute('USE `db.OSHES`;')
        cursor.execute('SELECT id FROM administrator WHERE id = %s', (username,))
        cursor.fetchone()
        result = True if cursor.rowcount > 0 else False
        cursor.close()

    return result


def is_cust_username_taken(username):
    with mysql_client.cursor() as cursor:
        cursor.execute('USE `db.OSHES`;')
        cursor.execute('SELECT id FROM customer WHERE id = %s', (username,))
        cursor.fetchone()
        result = True if cursor.rowcount > 0 else False
        cursor.close()

    return result


def insert_administrator(username, name, gender, phone, password):
    with mysql_client.cursor() as cursor:
        cursor.execute('USE `db.OSHES`;')
        cursor.execute('INSERT INTO administrator (id, name, gender, phone, password) '
                       'VALUES (%s,%s, %s, %s, %s)', (username, name, gender, phone, password))
        mysql_client.commit()
        cursor.close()


def insert_customer(username, name, gender, email, address, phone, password):
    with mysql_client.cursor() as cursor:
        cursor.execute('USE `db.OSHES`;')
        cursor.execute(
            'INSERT INTO customer (id, name, gender, email, address, phone, password) '
            'VALUES (%s,%s, %s, %s, %s, %s, %s)',
            (username, name, gender, email, address, phone, password))
        mysql_client.commit()
        cursor.close()


def validate_administrator_login(username, password):
    with mysql_client.cursor() as cursor:
        cursor.execute('USE `db.OSHES`;')
        cursor.execute('SELECT * FROM administrator WHERE id = %s AND password = %s', (username, password))
        results = cursor.fetchone()
        cursor.close()

    if results is None:
        return False, "", "", "", ""

    return True, results[0], results[1], results[2], results[3]


def validate_customer_login(username, password):
    with mysql_client.cursor() as cursor:
        cursor.execute('USE `db.OSHES`;')
        cursor.execute('SELECT * FROM customer WHERE id = %s AND password = %s', (username, password))
        results = cursor.fetchone()
        cursor.close()

    if results is None:
        return False, "", "", "", "", "", ""

    return True, results[0], results[1], results[2], results[3], results[4], results[5]


def purchase_item(customer_id, item, quantity: int):
    item['PurchaseStatus'] = 'Unsold'
    res = Items.find(item).limit(quantity)
    item_ids = []
    for db_item in res:
        item_ids.append(db_item['ItemID'])

    mysql_values = []
    for item_id in item_ids:
        mysql_values.append(('Sold', customer_id, item_id))

    cursor = mysql_client.cursor()
    cursor.execute('USE `db.OSHES`;')
    cursor.executemany(
        'UPDATE item SET purchase_status = %s, purchase_date = CURDATE(), customer_id = %s WHERE id = %s', mysql_values)

    mongo_ids = []
    for item_id in item_ids:
        mongo_ids.append({'ItemID': item_id})

    Items.update_many({
        '$or': mongo_ids
    }, {
        '$set': {
            'PurchaseStatus': 'Sold'
        }
    })

    mysql_client.commit()
    cursor.close()


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
    final_items = []
    final_values = []
    for product in list(res):
        product = {
            'ProductID': product['ProductID'],
            'Category': product['Category'],
            'Model': product['Model'],
            'Cost ($)': product['Cost ($)'],
            'Price ($)': product['Price ($)'],
            'Warranty (months)': product['Warranty (months)'],
        } if admin else {
            'ProductID': product['ProductID'],
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
        filtered_items = list(Items.find(filter_criteria))
        unsold_items = list(filter(lambda x: x['PurchaseStatus'] == 'Unsold', filtered_items))
        sold_items = list(filter(lambda x: x['PurchaseStatus'] == 'Sold', filtered_items))
        temp_items = []
        for item in unsold_items:
            item = {
                'Category': item['Category'],
                'Model': item['Model'],
                'Color': item['Color'],
                'Factory': item['Factory'],
                'PowerSupply': item['PowerSupply'],
                'ProductionYear': item['ProductionYear'],
            }
            temp_items.append(item)
        temp_items = [i for n, i in enumerate(temp_items) if i not in temp_items[n + 1:]]
        final_items.append(temp_items)
        temp = list(product.values())
        temp.append(len(unsold_items))
        if admin:
            temp.append(len(sold_items))
        final_values.append(temp)

    return final_values, final_items


def get_stock_levels(unsold_items):
    counts = []
    for item in unsold_items:
        temp_item = item.copy()
        temp_item['PurchaseStatus'] = 'Unsold'
        count = len(list(Items.find(temp_item)))
        counts.append(count)
    return counts


def find_product_by_category_and_model(category, model):
    return Products.find_one({'Category': category, 'Model': model})


def find_item_by_id(item_id):
    item = Items.find_one({'ItemID': item_id})
    product = find_product_by_category_and_model(item['Category'], item['Model'])
    return {**item, **product}


def find_product_by_id(product_id):
    with mysql_client.cursor(dictionary=True) as cursor:
        cursor.execute('USE `db.OSHES`;')
        cursor.execute('SELECT * FROM product WHERE id = %s', (product_id,))
        result = cursor.fetchone()
        cursor.close()

    return result


def get_purchase_history(customer_id):
    with mysql_client.cursor(dictionary=True) as cursor:
        cursor.execute('USE `db.OSHES`;')
        cursor.execute(
            'SELECT item.id, product.model, item.purchase_date, item.service_status FROM item '
            'INNER JOIN product ON item.product_id = product.id '
            'WHERE customer_id = %s',
            (customer_id,))
        result = cursor.fetchall()
        cursor.close()

    return result


def get_item_information(item_id):
    with mysql_client.cursor(dictionary=True) as cursor:
        cursor.execute('USE `db.OSHES`;')
        cursor.execute(
            'SELECT item.id, product.category, product.model, product.price, item.colour, item.power_supply, '
            'item.factory, item.production_year, product.warranty, item.service_status, administrator.name, '
            'item.purchase_date FROM item INNER JOIN product ON item.product_id = product.id '
            'LEFT JOIN administrator ON item.admin_id = administrator.id '
            'WHERE item.id = %s', (item_id,))
        result = cursor.fetchone()
        cursor.close()

    return result
