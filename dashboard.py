
from flask import Flask, jsonify
from threading import Thread
from fetcher import get_cetus_bounties

app=Flask(__name__)

@app.get("/")
def root():
    return {"status":"online","routes":["/cetus"]}

@app.get("/cetus")
def cetus():
    return jsonify(get_cetus_bounties())

def start():
    Thread(target=lambda: app.run(host="0.0.0.0", port=8080)).start()
