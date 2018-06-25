from sqlalchemy.orm import relationship

class Campaign(Base):

    __tablename__ = 'campaign'

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
    featureTypes = relationship(
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
    taskBoundaries = relationship(
        'TaskBoundary',
        back_populates='campaign',
        lazy=True
        )

    def __init__(self, **kwargs):
        super(Campaign, self).__init__(**kwargs)
