#before running this please install PySimpleGUI:
#for windows         python -m pip install PySimpleGUI
#for mac and linux   python3 -m pip install PySimpleGUI


import PySimpleGUI as pg

#TEST CASE before database is linked
CustomerID = 'id'
AdministratorID = 'id'
correctpassword = 'pass'
customername = 'Customer Name'
adminname = 'Admin Name'

# 0 - START HERE: intro window
intro_layout = [ [pg.Text("Welcome to OSHES.")],
                 [pg.Text("Are you a customer or an administrator?")],
                 [pg.Button('Customer'), pg.Button('Administrator')]
                  ]
intro_window = pg.Window('Welcome!', intro_layout)
intro_event, intro_values = intro_window.read()
intro_window.close()
#goes to 1 - open customer login window or admin login window


# 2A - customer main page
def customer():
    #all the different tabs
        #tab1 main and logout
    cust_main_layout = [ [pg.Text('Welcome, '+customername+'. '\
                                  'Please click on the tabs to access other functions.')],
                         [pg.Button('Log Out')]
                         ]
        #tab2 search & purchase
    #filters in the dropdown menu; filter by item attributes
    attributes = ["ItemID",
               "Category",
               "Color",
               "Factory",
               "PowerSupply",
               "PurchaseStatus",
               "ProductionYear",
               "Model",
               "ServiceStatus"]
    
    cust_search_layout = [ [pg.Text('Search for an item:')],
                           [pg.Input()],#match against any field? 
                           [pg.Text('guys which one should we use for filters???', text_color='orange')],
                           [pg.Text('NOTE: incomplete and currently only showing filter for "Category".')],
                           [pg.Text('Category'), pg.Combo(['Lights', 'Locks'])],
                           [pg.Text('Category'), pg.OptionMenu(['Lights', 'Locks'])],
                           [pg.Button('Apply filters and search')]
                           ]
        #tab3 request/service
    cust_request_layout = [ [pg.Text('request servicing for your purchased item here')]
                            #also show purchased items
                            ]
    #tab group
    cust_tabs = [ [pg.TabGroup([[pg.Tab('Logout', cust_main_layout)],
                                [pg.Tab('Search', cust_search_layout)],
                                [pg.Tab('Request',cust_request_layout)]
                                ]
                               )]
                  ]

    cust_main_window = pg.Window(customername+"'s session", cust_tabs)
    cust_main_event, cust_main_values = cust_main_window.read()
    if cust_main_event == 'Log Out':
        cust_main_window.close()
    
# 2B - administrator main page
def administrator():
    #all diff tabs
        #tab1 main and logout
    admin_main_layout = [ [pg.Text('Welcome, '+adminname+'. '\
                                   'Please click on the tabs to access other functions.')],
                          [pg.Button('Log Out')]
                          ]
        #tab2 database initialisation
    admin_database_layout = [ [pg.Text('database init here')]
                               ]
        #tab3 search + additional info + sold/unsold items
    admin_search_layout = [ [pg.Text('search here')]
                             ]
        #tab4 request/service
    admin_request_layout = [ [pg.Text('request here')]
                              ]
        #tab5 customers pending payment
    admin_payment_layout = [ [pg.Text('payment pending here')]
                              ]
    #tab group
    admin_tabs = [ [pg.TabGroup([[pg.Tab('Logout', admin_main_layout)],
                                 [pg.Tab('Database initialisation', admin_database_layout)],
                                 [pg.Tab('Search', admin_search_layout)],
                                 [pg.Tab('Request', admin_request_layout)],
                                 [pg.Tab('Payment pending', admin_payment_layout)]
                                 ]
                                 )]
                   ]
    admin_main_window = pg.Window(adminname+"'s session", admin_tabs)
    admin_main_event, admin_main_values = admin_main_window.read()


# open customer login window or admin login window
if intro_event == 'Customer':
    #customer login window
    cust_login_layout = [ [pg.Text("Customer ID:")],
                    [pg.Input(key='id')],
                    [pg.Text("Password:")],
                    [pg.Input(key='pass')],
                    [pg.Text(key='wrong_entry')],
                    [pg.Button('OK')]
                    ]
    cust_login_window = pg.Window('Customer Login',cust_login_layout)
    cust_login_event, cust_login_values = cust_login_window.read()
    #print(cust_login_values)
    #check customer ID and password against database
    if cust_login_values['id']==CustomerID and cust_login_values['pass']==correctpassword:
        cust_login_window.close()
        customer() #goes to 2A - customer main page
    else:
        cust_login_window['wrong_entry'].update('You have entered the wrong ID or password.')

else:
    #admin login window
    admin_login_layout = [ [pg.Text("Administrator ID:")],
                     [pg.Input(key='id')],
                     [pg.Text("Password:")],
                     [pg.Input(key='pass')],
                     [pg.Text(key='wrong_entry')],
                     [pg.Button('OK')]
                     ]
    
    admin_login_window = pg.Window('Customer Login',admin_login_layout)

    admin_login_event, admin_login_values = admin_login_window.read()
    #check admin ID and password against database
    if admin_login_values['id']==AdministratorID and admin_login_values['pass']==correctpassword:
        admin_login_window.close()
        administrator() #goes to 2B - administrator main page
    else:
        admin_login_window['wrong_entry'].update('You have entered the wrong ID or password.')


















