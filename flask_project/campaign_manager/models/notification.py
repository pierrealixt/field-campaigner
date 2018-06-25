
# NOT YET IN ALEMBIC

class Notification(Base):

    __tablename__ = 'notification'

    # id = Column(
    #     'id',
    #     Integer,
    #     primary_key=True,
    #     autoincrement=True
    #     )
    # campaign_id = Column(
    #     Integer,
    #     ForeignKey('campaign.id'),
    #     nullable=False
    #     )

    # sender_id = Column(
    #     Integer,
    #     ForeignKey('user.id'),
    #     nullable=False
    #     )
    campaign = relationship(
        'Campaign',
        back_populates='notification'
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

