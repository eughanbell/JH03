from urllib.request import urlopen
from urllib.error import HTTPError, URLError
from http.client import InvalidURL


def print_except(url, info, e):
    "Helper for get_from_url. prints out exception and url"
    print(f"ERROR: get_from_url error, returning blank file. url: {url} info: {info}" +
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
            print_except(url, "internet connection issue", e)
        except URLError as e:
            print_except(url, "url error", e)
        except InvalidURL as e:
            print_except(url, "invalid url string", e)
        except UnicodeEncodeError as e:
            print_except(url, "invalid character in url", e)
        except Exception as e:
            print_except(url, "unknown exeption", e)
    return bytearray()


def query_list_path(key, items, initial="?"):
    """
    Take a key string and items a list of strings.
    Return the query parameter of a url matching
    all items to the key. An example is
    ?key=item1&key=item2&key=item3

    This is useful for sending a list to a fastAPI enpoint
    """
    if len(items) == 0:
        return ""
    query = initial
    for x in items:
        query += key + "=" + x + "&"
    return query[0:-1]
