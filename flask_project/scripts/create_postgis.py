#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
from sqlalchemy import (
    create_engine
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

db_location = os.environ['DATABASE_URL']
engine = create_engine(db_location, echo=True)
Base = declarative_base()
Session = sessionmaker(bind=engine)
Session.configure(bind=engine)
session = Session()

session.execute('drop extension if exists postgis CASCADE;')
session.commit()

session.execute('create extension postgis;')
session.commit()