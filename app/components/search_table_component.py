import PySimpleGUI as sg

SEARCH_TABLE = '-SEARCH-TABLE-'


def search_table_component(table_data, table_headers):
    return [sg.Table(values=table_data, headings=table_headers,
                     auto_size_columns=True,
                     vertical_scroll_only=False,
                     justification='right',
                     num_rows=7,
                     alternating_row_color='lightyellow',
                     key=SEARCH_TABLE,
                     row_height=35,
                     tooltip='Search Results',
                     enable_events=True)]
