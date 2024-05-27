import webbrowser

def open_url(url):
    """
    Open the specified URL in the default web browser.
    
    Parameters:
        url (str): The URL to open.
        
    Returns:
        None
    """
    webbrowser.open(url)

# open url
url = "https://cyperfx-landing-page.netlify.app"
open_url(url)
