
# NOT YET IN ALEMBIC

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
