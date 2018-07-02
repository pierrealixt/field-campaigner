#!/usr/bin/python
# -*- coding: utf-8 -*-
import os

from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    Table,
    Text,
    ForeignKey,
    Date,
    DateTime,
    BOOLEAN
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import and_, or_
from sqlalchemy.sql.expression import true
from geoalchemy2 import Geometry


db_location = os.environ['DATABASE_URL']
engine = create_engine(db_location, echo=True)


Base = declarative_base()

Session = sessionmaker(bind=engine)
Session.configure(bind=engine)
session = Session()


adminAssociations = Table(
    'adminAssociations',
    Base.metadata,
    Column(
        'user_id',
        Integer,
        ForeignKey('user.id'),
        primary_key=True
        ),
    Column(
        'campaign_id',
        Integer,
        ForeignKey('campaign.id'),
        primary_key=True
        )
    )

typeCampaignAssociations = Table(
    'typeCampaignAssociations',
    Base.metadata,
    Column(
        'campaign_id',
        Integer,
        ForeignKey('campaign.id'),
        primary_key=True
        ),
    Column(
        'type_id',
        Integer,
        ForeignKey('featureType.id'),
        primary_key=True
        )
    )

featureTypeAssociations = Table(
    'featureTypeAssociations',
    Base.metadata,
    Column(
        'feature_id',
        Integer,
        ForeignKey('attribute.id'),
        primary_key=True
        ),
    Column(
        'type_id',
        Integer,
        ForeignKey('featureType.id'),
        primary_key=True
        )
    )

teamUserAssociations = Table(
    'teamUserAssociations',
    Base.metadata,
    Column(
        'user_id',
        Integer,
        ForeignKey('user.id'),
        primary_key=True
        ),
    Column(
        'team_id',
        Integer,
        ForeignKey('team.id'),
        primary_key=True
        )
    )

functionCampaignAssociations = Table(
    'functionCampaignAssociations',
    Base.metadata,
    Column(
        'campaign_id',
        Integer,
        ForeignKey('campaign.id')
        ),
    Column(
        'function_id',
        Integer,
        ForeignKey('function.id')
        )
    )


class Campaign(Base):

    __tablename__ = 'campaign'

    id = Column(
        'id',
        Integer,
        primary_key=True,
        autoincrement=True
        )
    creator_id = Column(
        Integer,
        ForeignKey('user.id'),
        nullable=False
        )
    creator = relationship(
        'User',
        back_populates='campaign_creator'
        )
    users = relationship(
        'User',
        secondary=adminAssociations,
        lazy='subquery',
        back_populates='campaigns'
        )
    feature_types = relationship(
        'FeatureType',
        secondary=typeCampaignAssociations,
        lazy='subquery',
        back_populates='campaigns'
        )
    functions = relationship(
        'Function',
        secondary=functionCampaignAssociations,
        lazy='subquery',
        back_populates='campaigns'
        )
    chat = relationship(
        'Chat',
        back_populates='campaign',
        lazy=True
        )
    notification = relationship(
        'Notification',
        back_populates='campaign',
        lazy=True
        )
    geometry = Column(Geometry('POLYGON'))
    task_boundaries = relationship(
        'TaskBoundary',
        back_populates='campaign',
        lazy=True
        )
    name = Column(
        String(20),
        unique=True,
        nullable=False
        )
    description = Column(String(200))
    start_date = Column(
        Date(),
        nullable=False
        )
    end_date = Column(
        Date(),
        nullable=False
        )
    create_on = Column(
        DateTime(),
        nullable=False
        )
    link_to_OpenMapKit = Column(
        BOOLEAN(),
        default=False
        )
    version = Column(Integer)
    uuid = Column(String(100))
    remote_projects = Column(String(30))
    map_type = Column(String(20))
    thumbnail = Column(String(100))

    def __init__(self, **kwargs):
        super(Campaign, self).__init__(**kwargs)



class Chat(Base):

    __tablename__ = 'chat'

    id = Column(
        'id',
        Integer,
        primary_key=True,
        autoincrement=True
        )
    campaign_id = Column(
        Integer,
        ForeignKey('campaign.id'),
        nullable=False
        )
    campaign = relationship(
        'Campaign',
        back_populates='chat'
        )
    sender_id = Column(
        Integer,
        ForeignKey('user.id'),
        nullable=False
        )
    sender = relationship(
        'User',
        foreign_keys=[sender_id],
        back_populates='chat_sender'
        )
    receiver_id = Column(
        Integer,
        ForeignKey('user.id'),
        nullable=False
        )
    reciever = relationship(
        'User',
        foreign_keys=[receiver_id],
        back_populates='chat_receiver'
        )
    message = Column(String(200))
    send_time = Column(DateTime())
    delivered = Column(
        BOOLEAN(),
        default=False
        )

    def __init__(self, **kwargs):
        super(Chat, self).__init__(**kwargs)


class Notification(Base):

    __tablename__ = 'notification'

    id = Column(
        'id',
        Integer,
        primary_key=True,
        autoincrement=True
        )
    campaign_id = Column(
        Integer,
        ForeignKey('campaign.id'),
        nullable=False
        )
    campaign = relationship(
        'Campaign',
        back_populates='notification'
        )
    sender_id = Column(
        Integer,
        ForeignKey('user.id'),
        nullable=False
        )
    sender = relationship(
        'User',
        back_populates='notification_sender'
        )
    notification_message = Column(String(100))
    time = Column(DateTime())
    delivered = Column(
        BOOLEAN(),
        default=False
        )

    def __init__(self, **kwargs):
        super(Notification, self).__init__(**kwargs)


class FeatureTemplate(Base):

    __tablename__ = 'featureTemplate'

    id = Column(
        'id',
        Integer,
        primary_key=True,
        autoincrement=True
        )
    name = Column(
        String(20),
        nullable=False
        )
    description = Column(String(200))
    featureType_id = Column(
        Integer,
        ForeignKey('featureType.id')
        )
    feature_type = relationship(
        'FeatureType',
        back_populates='feature_template'
        )

    def __init__(self, **kwargs):
        super(FeatureTemplate, self).__init__(**kwargs)


class FeatureType(Base):

    __tablename__ = 'featureType'

    id = Column(
        'id',
        Integer,
        primary_key=True,
        autoincrement=True
        )
    feature = Column(
        String(20),
        nullable=False
        )
    name = Column(String(20))
    is_template = Column(
        BOOLEAN(),
        default=False
        )
    feature_template = relationship(
        'FeatureTemplate',
        back_populates='feature_type'
        )
    function = relationship(
        'Function',
        back_populates='types',
        lazy=True
        )
    campaigns = relationship(
        'Campaign',
        secondary=typeCampaignAssociations,
        lazy='subquery',
        back_populates='feature_types'
        )
    attributes = relationship(
        'Attribute',
        secondary=featureTypeAssociations,
        lazy='subquery',
        back_populates='feature_types'
        )

    def __init__(self, **kwargs):
        super(FeatureType, self).__init__(**kwargs)



class Attribute(Base):

    __tablename__ = 'attribute'

    id = Column(
        'id',
        Integer,
        primary_key=True,
        autoincrement=True
        )
    attribute_name = Column(String(20))
    feature_types = relationship(
        'FeatureType',
        secondary=featureTypeAssociations,
        lazy='subquery',
        back_populates='attributes'
        )

    def __init__(self, **kwargs):
        super(Attribute, self).__init__(**kwargs)



class TaskBoundary(Base):

    __tablename__ = 'taskBoundary'

    id = Column(
        'id',
        Integer,
        primary_key=True,
        autoincrement=True
        )
    coordinates = Column(Geometry('POLYGON'))
    name = Column(String(100))
    status = Column(String(100))
    type_boundary = Column(String(100))
    team = relationship(
        'Team',
        back_populates='boundary',
        lazy=True,
        uselist=False
        )
    campaign_id = Column(
        Integer,
        ForeignKey('campaign.id'),
        nullable=False
        )
    campaign = relationship(
        'Campaign',
        back_populates='task_boundaries',
        lazy=True
        )

    def __init__(self, **kwargs):
        super(TaskBoundary, self).__init__(**kwargs)



class Team(Base):

    __tablename__ = 'team'

    id = Column(
        'id',
        Integer,
        primary_key=True,
        autoincrement=True
        )
    name = Column(
        String(20),
        nullable=False
        )
    boundary_id = Column(
        Integer,
        ForeignKey('taskBoundary.id'),
        nullable=False
        )
    boundary = relationship(
        'TaskBoundary',
        back_populates='team'
        )
    users = relationship(
        'User',
        secondary=teamUserAssociations,
        lazy='subquery',
        back_populates='teams'
        )

    def __init__(self, **kwargs):
        super(Team, self).__init__(**kwargs)



class Function(Base):

    __tablename__ = 'function'

    id = Column(
        'id',
        Integer,
        primary_key=True,
        autoincrement=True
        )
    name = Column(
        String(100),
        nullable=False
        )
    feature = Column(String(100))
    type_id = Column(
        Integer,
        ForeignKey('featureType.id'),
        nullable=False
        )
    types = relationship(
        'FeatureType',
        back_populates='function'
        )
    campaigns = relationship(
        'Campaign',
        secondary=functionCampaignAssociations,
        lazy='subquery',
        back_populates='functions'
        )

    def __init__(self, **kwargs):
        super(Function, self).__init__(**kwargs)

