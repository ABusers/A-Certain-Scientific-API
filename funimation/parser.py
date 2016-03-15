import xmltodict


def collapse(dictionary):
    if 'watchlist' in dictionary.keys():
        if 'historyItem' in dictionary['watchlist']['items']:
            return dictionary['watchlist']['items']['historyItem']
        else:
            return dictionary['watchlist']['items']
    return dictionary

def parse(xml):
    parsed = xmltodict.parse(xml)
    return collapse(parsed)