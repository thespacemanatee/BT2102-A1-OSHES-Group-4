from app.database.setup import Products, Items


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


def get_filtered_results(category=None, model=None, color=None, factory=None, power_supply=None, production_year=None):
    filter_by = {}
    projection = ['Category', 'Model', 'Price ($)', 'Warranty (months)']
    if category:
        filter_by['Category'] = category
    elif model:
        filter_by['Model'] = model

    res = list(Products.find(filter_by, projection))
    final = []
    for product in res:
        filter_criteria = {}
        filter_criteria['Category'] = product['Category']
        filter_criteria['Model'] = product['Model']
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
        temp.append(len(filter_res))
        final.append(temp[1:])

    return final
