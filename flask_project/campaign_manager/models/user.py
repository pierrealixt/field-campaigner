from sqlalchemy.orm import relationship

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

