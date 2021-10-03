import PySimpleGUI as sg

def setup_window(title: str, layout):
    '''
    Use this function to generate new windows
    @param title: Title to be set for new screen
    @param layout: A PySimpleGUI layout object
    '''
    
    return sg.Window(title, layout, resizable=True)