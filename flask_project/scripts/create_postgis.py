#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
from sqlalchemy import (
    create_engine
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from campaign_manager.sqlalchemy_session import engine, session, Base

session.execute('drop extension if exists postgis CASCADE;')
session.commit()

session.execute('create extension postgis;')
session.commit()
