import PySimpleGUI as sg

COLOR_CHECKBOX = 'color_checkbox'
COLOR_CHECKBOX_VAL = 'color_checkbox_val'


def colors_filter_component(col):
    return sg.Column([[sg.Checkbox('Color', key=COLOR_CHECKBOX),
                       sg.OptionMenu(col, default_value=col[0], key=COLOR_CHECKBOX_VAL)]])
