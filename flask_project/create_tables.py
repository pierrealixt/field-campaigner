#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
from sqlalchemy import (
    create_engine
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.schema import DropTable
from sqlalchemy.ext.compiler import compiles

from campaign_manager.models.models import *
from campaign_manager.sqlalchemy_session import engine, session, Base


@compiles(DropTable, "postgresql")
def _compile_drop_table(element, compiler, **kwargs):
    return compiler.visit_drop_table(element) + " CASCADE"


session.rollback()
session.commit()
session.close_all()
Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)
