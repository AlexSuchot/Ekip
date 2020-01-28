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
                           node_address=CONNECTED_NODE_ADDRESS)


@app.route('/submit', methods=['POST'])
def submit_textarea():
    global i
    chain = []
    count = 0
    block = ''
    pdfFileObj = open('Livre_Maupassant.pdf', 'rb')
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj)

    # Submit a transaction
    global block, count

    # On parcours toutes les pages du livre et on affiche le texte :
    for x in range(pdfReader.numPages):
        # Affiche une page :
        pageObj = pdfReader.getPage(x)
        text = pageObj.extractText() + '\n'
        block += text
        count += 1
        if count == 5:
            chain.append(block)
            encodedBlock = block.encode('UTF-8')
            m = hashlib.sha256()
            m.update(encodedBlock)
            block = ''
            count = 0

    post_object = {
        'author': i,
        'content': chain[i],
    }

    i += 1
    new_tx_address = "{}/new_transaction".format(CONNECTED_NODE_ADDRESS)
    requests.post(new_tx_address,
                  json=post_object,
                  headers={'Content-type': 'application/json'})

    return redirect('/')
