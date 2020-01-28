# Guy de Maupassant - BlockChain

## Instructions to run

Install the dependencies,

```sh
$ cd Python
$ pip install -r requirements.txt
```

Start a blockchain node server,

```sh
$ export FLASK_APP=node_server.py
$ flask run --port 8000
```

One instance of our blockchain node is now up and running at port 8000.


Run the application on a different terminal session,

```sh
$ python run_app.py
```

The application should be up and running at [http://localhost:5000](http://localhost:5000).

Here are a few screenshots

1. Post a block

2. Requesting the node to mine

3. Resyncing with the chain for updated data


To play around by spinning off multiple custom nodes, use the `register_with/` endpoint to register a new node. 

To run another application with a different port :

```sh
# already running
$ flask run --port 8000 &
# spinning up new nodes
$ flask run --port 8001 &
$ flask run --port 8002 &
```
