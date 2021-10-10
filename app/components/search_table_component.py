from app.components.base_table_component import base_table_component

SEARCH_TABLE = '-SEARCH-TABLE-'


def search_table_component(table_data, table_headers, padding):
    return [base_table_component(values=table_data, headings=table_headers,
                                 key=SEARCH_TABLE,
                                 col_widths=padding,
                                 tooltip='Search Results',
                                 )]
