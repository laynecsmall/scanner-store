from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os, datetime

class Result(declarative_base()):
    __tablename__ = 'results'

    id = Column(Integer, primary_key=True)
    device_name = Column(String)
    time = Column(DateTime)
    raw_results = Column(String)

    def __repr__(self):
        return "Result(id='%s', device_name='%s', time='%s', raw_results:\n%s)" % (
                self.id, self.device_name, self.time, self.raw_results )

class Device(declarative_base()):
    __tablename__ = 'devices'

    device_id = Column(String, primary_key=True)
    device_type = Column(String)
    sensor_x = Column(Integer)
    sensor_y = Column(Integer)
    create_time = Column(DateTime)
    last_update = Column(DateTime)

    def __repr__(self):
        return "Device(id='%s', device_type='%s', x:y=%d:%d, created='%s', last_updated='%s" % (
                self.device_id,
                self.device_type,
                self.sensor_x,
                self.sensor_y,
                self.create_time.isoformat(),
                self.last_update.isoformat())

def setup_db(path):
    if check_db_exist(path):
        db = create_engine("sqlite:///%s" % (path))
    else:
        db = create_engine("sqlite:///%s" % (path))
        create_db(db)
    Session = sessionmaker(bind=db)
    return Session()


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
    r = Result(device_name=result['device_name'],
               time=result['time'],
               raw_results=result['raw_results'])
    db_session.add(r)

    #update last_updated time in devices table
    db_session.query(Device).filter_by(device_id=result['device_name']).update({"last_update":datetime.datetime.now()})

    db_session.commit()


def insert_new_device(db_session, device):
    #result = 
    d = Device(device_id=device['device_name'],
               device_type=device['device_type'],
               sensor_x=device['sensor_x'],
               sensor_y=device['sensor_y'],
               create_time=datetime.datetime.now(),
               last_update=datetime.datetime.now())
    db_session.add(d)
    db_session.commit()

def get_latest_result_for_device(db_session, device_id):
    result = db_session.query(Result).filter(Result.device_name==device_id).order_by(Result.id.desc()).first()
    return result

def get_latest_n_results_for_device(db_session, device_id, n):
    result = db_session.query(Result).filter(Result.device_name==device_id).order_by(Result.id.desc()).limit(count).all()
    return result

def get_latest_result(db_session):
    result = db_session.query(Result).order_by(Result.id.desc()).first()
    return result

def get_latest_n_results(db_session, n):
    result = db_session.query(Result).order_by(Result.id.desc()).limit(n).all()
    return result

def get_device_details(db_session, device):
    result = db_session.query(Device).filter(device).first()
    return result

def get_all_devices(db_session):
    return db_session.query(Device).all()

