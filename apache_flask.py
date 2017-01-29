#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
	:author: Muneeb Ali | http://muneebali.com
	:license: MIT, see LICENSE for more details.
"""

from flask import Flask, make_response, render_template, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from scanner_store_db import *
from config import DEFAULT_DB_FILE

app = Flask(__name__)

db = setup_db(DEFAULT_DB_FILE)

from commontools import log

import pdb

def setup_db(path, app):
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///%s" % (path)
    if check_db_exist(path):
        db = SQLAlchemy(app)
    else:
        db = SQLAlchemy(app)
        create_db(db)
    Session = sessionmaker(bind=db)
    return Session()


#-----------------------------------
@app.route('/')
def index():
	return render_template('index.html')

#-----------------------------------
#-----------------------------------
@app.route('/new/result',  methods=['POST'])
def new_result():
    if request.method == 'POST':
        if sorted(request.form.viewkeys()) == sorted(['device_name','time','raw_results']):
            insert_new_result(db, {"device_name": request.form['device_name'],
                                   "time":datetime.datetime.strptime(request.form['time'], "%Y-%m-%dT%H:%M:%S.%f"),
                                   "raw_results": request.form['raw_results']})
            return make_response(jsonify( { 'success': 'result stored' } ), 200)
        else:
            return make_response(jsonify( { 'failure': 'bad request' } ), 400)
    else:
            return make_response(jsonify( { 'failure': 'unsupported method' } ), 400)


#-----------------------------------
#-----------------------------------
@app.route('/new/device', methods=['POST'])
def new_device():
    if request.method == 'POST':
        if sorted(request.form.viewkeys()) == sorted(['device_name','device_type','sensor_x', 'sensor_y']):
            insert_new_device(db, {"device_name": request.form['device_name'],
                                   "device_type": request.form['device_type'],
                                   "sensor_x": request.form['sensor_x'],
                                   "sensor_y": request.form['sensor_y']})
            return make_response(jsonify( { 'success': 'device created' } ), 200)
        else:
            return make_response(jsonify( { 'failure': 'bad request' } ), 400)
    else:
            return make_response(jsonify( { 'failure': 'unsupported method' } ), 400)

#-----------------------------------
#-----------------------------------
@app.route('/results/latest_for_device/<device_name>')
def latest_for_device(device_name):
    result =  get_latest_result_for_device(db, device_name)  
    return make_response(jsonify(result.to_dict()), 200)

#-----------------------------------
#-----------------------------------
@app.route('/results/latest_n_for_device/<n>/<device_name>')
def latest_n_for_device(n, device_name):
    result =  get_latest_n_results_for_device(db, device_name,n)  
    out = {"responses":[x.to_dict() for x in result]}

    return make_response(jsonify(out), 200)

#-----------------------------------
#-----------------------------------
@app.route('/device/details/<device>')
def details_for_device(device):
    return make_response(jsonify(get_device_details(db, device).to_dict()), 200)

#-----------------------------------
#-----------------------------------
@app.route('/device/all')
def details_all_devices():
    result = get_all_devices(db)
    out = {"devices": [x.to_dict() for x in result]}
    return make_response(jsonify(out), 200)

#-----------------------------------
@app.errorhandler(500)
def internal_error(error):

	reply = []
	return jsonify(reply)

#-----------------------------------
@app.errorhandler(404)
def not_found(error):
	return make_response(jsonify( { 'error': 'Not found' } ), 404)
