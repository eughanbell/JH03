from urllib.request import urlopen
from urllib.error import HTTPError, URLError
from http.client import InvalidURL

def print_except(url, e):
    "Helper for get_from_url. prints out exception and url"
    print("get_from_url error, returning None. url: " + url +
          " --- Exception: ", e)

def get_from_url(url):
    "Tries to request data from a url, return None on failure"
    if not isinstance(url, str):
        print("the supplied url was not a string")
    else:
        try:
            f = urlopen(url)
            if f.getcode() != 200:
                print(f"http status code: {f.getcode()}, uniprot id"
                      " was invalid, id: {uniprot_id}")
            else:
                return f.read()
        except HTTPError as e:
            print_except(url, e)
        except URLError as e:
            print_except(url, e)
        except InvalidURL as e:
            print_except(url, e)
    return None
