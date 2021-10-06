import PySimpleGUI as sg

FACTORY_CHECKBOX = 'factory_checkbox'
FACTORY_CHECKBOX_VAL = 'factory_checkbox_val'


def factories_filter_component(fac):
    return sg.Column([[sg.Checkbox('Factory', key=FACTORY_CHECKBOX),
                       sg.OptionMenu(fac, default_value=fac[0], key=FACTORY_CHECKBOX_VAL)]])
