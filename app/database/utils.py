from app.database.setup import mysql_client, Products, Items


def initialise_mysql_database():
    cursor = mysql_client.cursor()
    with open('database/mysql_init.sql') as f:
        results = cursor.execute(f.read(), multi=True)
        for result in results:
            continue


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
