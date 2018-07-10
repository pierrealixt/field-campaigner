#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
from sqlalchemy import (
    create_engine
)
from sqlalchemy.ext.declarative import declarative_base

db_location = os.environ['DATABASE_URL']
engine = create_engine(db_location, echo=True)
Base = declarative_base()

import sys
print('create_tablres.py')
print(sys.path)

from flask_project.campaign_manager.models.models import *

Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)
