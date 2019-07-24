#!/usr/bin/python3

from flask import Flask, render_template, request

import search

application = app = Flask(__name__)
app.debug = True

@app.route('/search', methods=["GET"])
def dosearch():
    query = request.args['query']
    qtype = request.args['query_type']
    itemnum = request.args['page']
    move = request.args['move']


    itemnum = int(itemnum)
    if move == "previous":
        itemnum -= 20

    if move == "next":
        itemnum += 20

    if move == "start":
        itemnum = 0

    if itemnum < 0:
        itemnum = 0



    """
    TODO:
    Use request.args to extract other information
    you may need for pagination.
    """

    search_results = search.search(query, qtype,itemnum)




    if len(search_results) == 21:
        display = search_results[:-1]
    else:
        display = search_results



    return render_template('results.html',
            query=query,
            qtype = qtype,
            results=len(search_results),
            search_results=display,
            display_results = len(display),
            item = itemnum)

@app.route("/", methods=["GET"])
def index():
    if request.method == "GET":
        pass
    return render_template('index.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0')
