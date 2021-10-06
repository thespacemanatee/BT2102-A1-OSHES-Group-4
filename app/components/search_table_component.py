import PySimpleGUI as sg


def search_table_component(table_data, table_headers):
    return [sg.Table(values=table_data, headings=table_headers,
                     auto_size_columns=False,
                     display_row_numbers=True,
                     justification='left',
                     num_rows=20,
                     alternating_row_color='lightyellow',
                     key='-TABLE-',
                     row_height=35,
                     col_widths=[19, 19, 19, 19, 19],
                     tooltip='Search Results',
                     enable_events=True)]
