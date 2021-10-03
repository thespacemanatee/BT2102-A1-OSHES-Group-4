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
    filter_criteria = {}
    projection = ['Category', 'Model', 'Price ($)', 'Warranty (months)']
    if category:
        filter_criteria['Category'] = category
    elif model:
        filter_criteria['Model'] = model
    if color:
        filter_criteria['Color'] = color
    if factory:
        filter_criteria['Factory'] = factory
    if power_supply:
        filter_criteria['PowerSupply'] = power_supply
    if production_year:
        filter_criteria['ProductionYear'] = production_year

    res = list(Products.find(filter_criteria, projection))
    final = []
    for item in res:
        final.append(list(item.values())[1:])

    return final
