import PySimpleGUI as sg

PRODUCTION_YEAR_CHECKBOX = 'production_year_checkbox'
PRODUCTION_YEARS_CHECKBOX_VAL = 'production_years_checkbox_val'


def production_years_filter_component(prod):
    return sg.Column([[sg.Checkbox('Production Years', key=PRODUCTION_YEAR_CHECKBOX),
                       sg.OptionMenu(prod, default_value=prod[0],
                                     key=PRODUCTION_YEARS_CHECKBOX_VAL)]])
