#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
	:author: Muneeb Ali | http://muneebali.com
	:license: MIT, see LICENSE for more details.
"""

from flask import Flask, make_response, render_template, jsonify
from scanner_store_db import *
from config import DEFAULT_DB_FILE

app = Flask(__name__)

db = setup_db(DEFAULT_DB_FILE)

from commontools import log

#-----------------------------------
@app.route('/')
def index():
	return render_template('index.html')

#-----------------------------------
#-----------------------------------
@app.route('/new/result', method=['POST'])
def new_result():
    if request.method == 'POST':
        if sorted(request.form.keys) == sorted(['device_name','time','raw_results']):
            insert_new_result(db, {"device_name": request.form['device_name'],
                "time":request.form['time'],
                "raw_results": request.form['raw_results']})
            return make_response(jsonify( { 'success': 'result stored' } ), 200)
        else:
            return make_response(jsonify( { 'failure': 'bad request' } ), 400)
    else:
            return make_response(jsonify( { 'failure': 'unsupported method' } ), 400)


#-----------------------------------
#-----------------------------------
@app.route('/new/device', method=['POST'])
def index():
	return render_template('index.html')

#-----------------------------------
#-----------------------------------
@app.route('/results/latest_for_device/<device_name>')
def index():
	return render_template('index.html')

#-----------------------------------
#-----------------------------------
@app.route('/latest_n_for_device/<n>/<device_name>')
def index():
	return render_template('index.html')

#-----------------------------------
#-----------------------------------
@app.route('/get/device/details/<device>')
def index():
	return render_template('index.html')

#-----------------------------------
#-----------------------------------
@app.route('/get/device/all')
def index():
	return render_template('index.html')

#-----------------------------------
@app.errorhandler(500)
def internal_error(error):

	reply = []
	return jsonify(reply)

#-----------------------------------
@app.errorhandler(404)
def not_found(error):
	return make_response(jsonify( { 'error': 'Not found' } ), 404)
