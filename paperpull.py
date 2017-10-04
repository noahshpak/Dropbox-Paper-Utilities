from pprint import pprint
import requests
import json
import cPickle as pickle
from HTMLParser import HTMLParser

ACCESS_TOKEN = 'YOUR TOKEN HERE'

class PaperHTMLParser(HTMLParser):
    def __init__(self):
        # initialize the base class
        HTMLParser.__init__(self)
        self.doc = []

    def handle_starttag(self, tag, attrs):
        pass
    def handle_endtag(self, tag):
        pass
    def handle_data(self, data):
        self.doc.append(data)

def get_doc_ids():
    url = "https://api.dropboxapi.com/2/paper/docs/list"
    headers = {
        "Authorization": "Bearer {token}".format(token=ACCESS_TOKEN),
        "Content-Type": "application/json"
    }
    data = {}
    r = requests.post(url, headers=headers, data=json.dumps(data))
    response_data = r.json()

    return response_data['doc_ids']

    # NOTE: loop while more in list/continue
    while response_data['has_more']:
        url = "https://api.dropboxapi.com/2/paper/docs/list/continue"
        headers = {
            "Authorization": "Bearer {token}".format(token=ACCESS_TOKEN),
            "Content-Type": "application/json"
        }
        data = {
            "cursor": response_data['cursor']['value']
        }
        response_data = requests.post(url, headers=headers, data=json.dumps(data))
        paper_doc_ids.extend(response_data['doc_ids'])

    return paper_doc_ids


def get_folder_info(doc_id, i=None, n=None):
    # NOTE: i, n for printing progress
    if i and n:
        print 'Gathering {i} of {n}'.format(i=i,n=n)

    url = "https://api.dropboxapi.com/2/paper/docs/get_folder_info"

    headers = {
        "Authorization": "Bearer {token}".format(token=ACCESS_TOKEN),
        "Content-Type": "application/json"
    }

    data = {
        "doc_id": doc_id
    }

    r = requests.post(url, headers=headers, data=json.dumps(data))
    return r.json().get('folders', [None])[0]

def get_text(doc_id):
    url = "https://api.dropboxapi.com/2/paper/docs/download"

    data = {
        "doc_id": "{_id}".format(_id=doc_id),
        "export_format": {
            ".tag": "html"
        }
    }
    headers = {
        "Authorization": "Bearer {token}".format(token=ACCESS_TOKEN),
        "Dropbox-API-Arg": json.dumps(data)
    }

    doc_as_html = requests.post(url, headers=headers).text

    parser = PaperHTMLParser()
    parser.feed(doc_as_html)
    return " ".join(parser.doc)

def pull_and_save():
    doc_ids = get_doc_ids()
    n = len(doc_ids)
    docs = { _id: {'folder': get_folder_info(_id, i=i, n=n), 'text': get_text(_id)} for i, _id in enumerate(doc_ids)}
    pickle.dump(docs, open('paper_docs.p', "wb"))

pull_and_save()
