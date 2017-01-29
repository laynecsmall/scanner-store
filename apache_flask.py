#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
	:author: Muneeb Ali | http://muneebali.com
	:license: MIT, see LICENSE for more details.
"""

from flask import Flask, make_response, render_template, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData, create_engine, Table, Column, String, Integer, DateTime
from config import DEFAULT_DB_FILE


from commontools import log

import os, datetime, pdb

def setup_db(path, app):
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///%s" % (path)
    if check_db_exist(path):
        db = SQLAlchemy(app)
    else:
        db = create_engine("sqlite:///%s" % (path))
        create_db(db)
        db = SQLAlchemy(app)
    return db


def create_db(db_obj):
    devices = Table('devices', MetaData(bind=db_obj),
      Column('device_id', String(40), primary_key = True),
      Column('device_type', String(40)),
      Column('sensor_x', Integer),
      Column('sensor_y', Integer),
      Column('create_time', DateTime),
      Column('last_update', DateTime))

    devices.create()

    results = Table('results', MetaData(bind=db_obj),
      Column('id', Integer, primary_key=True, autoincrement=True),
      Column('device_name', String(40)),
      Column('time', DateTime),
      Column('raw_results', String))

    results.create()

def check_db_exist(path):
    return os.path.isfile(path)

def insert_new_result(db_session, result):
    #add result
    r = Result(result['device_name'],
               result['time'],
               result['raw_results'])
    db_session.session.add(r)

    #update last_updated time in devices table
    Device.query.filter_by(device_id=result['device_name']).update({"last_update":datetime.datetime.now()})

    db_session.session.commit()


def insert_new_device(db_session, device):
    #result = 
    d = Device(device['device_name'],
               device['device_type'],
               device['sensor_x'],
               device['sensor_y'],
               datetime.datetime.now(),
               datetime.datetime.now())
    db_session.session.add(d)
    db_session.session.commit()

def get_latest_result_for_device(db_session, device_id):
    result = Result.query.filter(Result.device_name==device_id).order_by(Result.id.desc()).first()
    return result

def get_latest_n_results_for_device(db_session, device_id, n):
    result = Result.query.filter(Result.device_name==device_id).order_by(Result.id.desc()).limit(n).all()
    return result

def get_latest_result(db_session):
    result = Result.query.order_by(Result.id.desc()).first()
    return result

def get_latest_n_results(db_session, n):
    result = Result.query.order_by(Result.id.desc()).limit(n).all()
    return result

def get_device_details(db_session, device):
    result = Device.query.filter_by(device_id = device).first()
    return result

def get_all_devices(db_session):
    return Device.query.all()

app = Flask(__name__)

db = setup_db(DEFAULT_DB_FILE, app)

class Result(db.Model):
    __tablename__ = 'results'

    id = db.Column(db.Integer, primary_key=True)
    device_name = db.Column(db.String)
    time = db.Column(db.DateTime)
    raw_results = db.Column(db.String)

    def __init__(self,  device_name, time, raw_results):
        self.device_name = device_name
        self.time = time
        self.raw_results = raw_results

    def __repr__(self):
        return "Result(id='%s', device_name='%s', time='%s', raw_results:\n%s)" % (
                self.id, self.device_name, self.time, self.raw_results )

    def to_dict(self):
        return {"id": self.id,
                "device_name": self.device_name,
                "time": self.time.isoformat(),
                "raw_results": self.raw_results}


class Device(db.Model):
    __tablename__ = 'devices'

    device_id = db.Column(db.String, primary_key=True)
    device_type = db.Column(db.String)
    sensor_x = db.Column(db.Integer)
    sensor_y = db.Column(db.Integer)
    create_time = db.Column(db.DateTime)
    last_update = db.Column(db.DateTime)

    def __init__(self, device_id, device_type, sensor_x, sensor_y, create_time, last_update):
        self.device_id = device_id
        self.device_type = device_type
        self.sensor_x = sensor_x
        self.sensor_y = sensor_y
        self.create_time = create_time
        self.last_update = last_update

    def __repr__(self):
        return "Device(id='%s', device_type='%s', x:y=%d:%d, created='%s', last_updated='%s" % (
                self.device_id,
                self.device_type,
                self.sensor_x,
                self.sensor_y,
                self.create_time.isoformat(),
                self.last_update.isoformat())

    def to_dict(self):
        return {"device_id": self.device_id,
                "device_type": self.device_type,
                "sensor_x": self.sensor_x,
                "sensor_y": self.sensor_y,
                "create_time": self.create_time.isoformat(),
                "last_update": self.last_update.isoformat()}

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

