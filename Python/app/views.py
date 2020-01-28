import datetime
import hashlib
import json

import PyPDF2
import requests
from flask import render_template, redirect, request

from app import app

# The node with which our application interacts, there can be multiple
# such nodes as well.
CONNECTED_NODE_ADDRESS = "http://127.0.0.1:8000"

posts = []

count = 0
block = ''
i = 0

def fetch_posts():
    """
    Function to fetch the chain from a blockchain node, parse the
    data and store it locally.
    """
    get_chain_address = "{}/chain".format(CONNECTED_NODE_ADDRESS)
    response = requests.get(get_chain_address)
    if response.status_code == 200:
        content = []
        chain = json.loads(response.content)
        for block in chain["chain"]:
            for tx in block["transactions"]:
                tx["index"] = block["index"]
                tx["hash"] = block["previous_hash"]
                content.append(tx)

        global posts
        posts = sorted(content, key=lambda k: k['timestamp'],
                       reverse=True)


@app.route('/')
def index():
    fetch_posts()
    return render_template('index.html',
                           title='Guy de Maupassant - BlockChain',
                           posts=posts,
                           node_address=CONNECTED_NODE_ADDRESS,
                           readable_time=timestamp_to_string)


@app.route('/submit', methods=['POST'])
def submit_textarea():
    pdfFileObj = open('Livre_Maupassant.pdf', 'rb')
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj)

    # Submit a transaction
    global block, count
    new_tx_address = "{}/new_transaction".format(CONNECTED_NODE_ADDRESS)

    # On parcours toutes les pages du livre et on affiche le texte :
    for x in range(pdfReader.numPages):
        # Affiche une page :
        pageObj = pdfReader.getPage(x)
        text = pageObj.extractText() + '\n'
        block += text
        count += 1
        if count == 5:
            print(block)
            encodedBlock = block.encode('UTF-8')
            m = hashlib.sha256()
            m.update(encodedBlock)
            print(m.hexdigest())

            post_object = {
                'author': m.hexdigest(),
                'content': block,
            }
            requests.post(new_tx_address,
                          json=post_object,
                          headers={'Content-type': 'application/json'})
            block = ''
            count = 0

        elif x == 705:
            pageObj1 = pdfReader.getPage(705)
            pageObj2 = pdfReader.getPage(706)
            pageObj3 = pdfReader.getPage(707)
            text1 = pageObj1.extractText() + '\n'
            text2 = pageObj2.extractText() + '\n'
            text3 = pageObj3.extractText() + '\n'
            block = text1 + text2 + text3
            encodedBlock = block.encode('UTF-8')
            m = hashlib.sha256()
            m.update(encodedBlock)
            print(m.hexdigest())

            post_object = {
                'author': m.hexdigest(),
                'content': block,
            }
            requests.post(new_tx_address,
                          json=post_object,
                          headers={'Content-type': 'application/json'})

    return redirect('/')


def timestamp_to_string(epoch_time):
    return datetime.datetime.fromtimestamp(epoch_time).strftime('%H:%M')
