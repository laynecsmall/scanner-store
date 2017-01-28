from sqlalchemy import *
import os

class Result(Base):
    __tablename__ = 'results'

    id = Column(Integer, primary_key=True)
    device_name = Column(String)
    time = Column(DateTime)
    raw_results = Column(String)

    def __repr__(self):
        return "Result(id='%s', device_name='%s', time='%s', raw_results:\n%s)" % (
                self.id, self.device_name, self.time, self.raw_results )

class Device(Base):
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
        db = create_engine("sqllite:///%d" % (path))
        return sessionmaker(bind=db)

    else:
        db = create_engine("sqllite:///%d" % (path))

        db.echo = False

        devices = Table('devices', MetaData(bind=db),
          Column('device_id', String(40), primary_key = True),
          Column('device_type', String(40)),
          Column('sensor_x', Integer),
          Column('sensor_y', Integer),
          Column('create_time', DateTime),
          Column('last_update', DateTime))

        devices.create()

        results = Table('results', MetaData(bind=db),
          Column('id', Integer, primary_key=True, autoincrement=True),
          Column('device_name', String(40)),
          Column('time', DateTime),
          Column('raw_results', String))

        results.create()

        return sessionmaker(bind=db)

def check_db_exist(path):
    return os.path.isfile(path)

def insert_new_result(db_session, result):
    #result = 
    pass

def insert_new_device(db_session, device):
    pass

session = setup_db('scanner_store.db')
