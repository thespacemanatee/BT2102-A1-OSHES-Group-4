import PySimpleGUI as sg

POWER_SUPPLY_CHECKBOX = 'power_supply_checkbox'
POWER_SUPPLY_CHECKBOX_VAL = 'power_supply_checkbox_val'


def power_supplies_filter_component(pow_sup):
    return sg.Column([[sg.Checkbox('Power Supply', key=POWER_SUPPLY_CHECKBOX),
                       sg.OptionMenu(pow_sup, default_value=pow_sup[0],
                                     key=POWER_SUPPLY_CHECKBOX_VAL)]])
