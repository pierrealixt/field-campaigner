from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

from somewhere import (
    Base, # Base = declarative_base()
    session
)


Session = sessionmaker(bind=engine)
Session.configure(bind=engine)
session = Session()

class User(Base):

    __tablename__ = 'user'

    campaign_creator = relationship(
        'Campaign',
        back_populates='creator',
        lazy=True,
        uselist=False
        )
    chat_sender = relationship(
        'Chat',
        foreign_keys='Chat.sender_id',
        back_populates='sender',
        lazy=True,
        uselist=False
        )
    chat_receiver = relationship(
        'Chat',
        foreign_keys='Chat.receiver_id',
        back_populates='reciever',
        lazy=True,
        uselist=False
        )
    notification_sender = relationship(
        'Notification',
        back_populates='sender',
        lazy=True,
        uselist=False
        )
    campaigns = relationship(
        'Campaign',
        secondary=adminAssociations,
        lazy='subquery',
        back_populates='users'
        )
    teams = relationship(
        'Team',
        secondary=teamUserAssociations,
        lazy='subquery',
        back_populates='users'
        )

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)

    def create(self):
        """ Creates and Saves the current model the DB """
        session.add(self)
        session.commit()

    def save(self):
        session.commit()

    def get_by_osm_id(self, osm_id):
        """ Returns the user with the specified osm user id """
        return session.query(User).filter(
            User.osm_user_id == osm_id
            ).first()

    def get_all(self):
        """ Returns all the users registered with field-campaigner """
        return session.query(User).all()

    def update(self, user_dto):
        """ Updates the user's details """
        if user_dto['osm_user_id']:
            self.osm_user_id = user_dto['osm_user_id']
        if user_dto['email']:
            self.email = user_dto['email']
        session.commit()
