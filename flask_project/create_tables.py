#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
from sqlalchemy import (
    create_engine
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

if 'RDS_DB_NAME' in os.environ:
    db_location = 'postgres://{}:{}@{}/{}'.format(
        os.environ['RDS_USERNAME'],
        os.environ['RDS_PASSWORD'],
        os.environ['RDS_HOSTNAME'],
        os.environ['RDS_DB_NAME'])
else:
    db_location = os.environ['DATABASE_URL']

engine = create_engine(db_location, echo=True)
Base = declarative_base()
Session = sessionmaker(bind=engine)
Session.configure(bind=engine)
session = Session()


from campaign_manager.models.models import *
from sqlalchemy.schema import DropTable
from sqlalchemy.ext.compiler import compiles


@compiles(DropTable, "postgresql")
def _compile_drop_table(element, compiler, **kwargs):
    return compiler.visit_drop_table(element) + " CASCADE"


session.rollback()
session.commit()
session.close_all()
Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)
