from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup


def is_good_response(resp):
    """
    Returns True if the response seems to be HTML, False otherwise.
    """
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200 
            and content_type is not None 
            and content_type.find('html') > -1)


def simple_get(url):

    try:
        with closing(get(url, stream=True)) as resp:
            if is_good_response(resp):
                return resp.content
            else:
                return None

    except RequestException as e:
        print('Error during requests to {0} : {1}', format(url, str(e)))

bracket_html = simple_get('''https://smash.gg/tournament/smashing-legends-107/events/ultimate-singles/brackets/490150/852706''')

brackets = BeautifulSoup(bracket_html, 'html.parser')
print(brackets.prettyfy())
