from sqlalchemy.orm import relationship

class Function(Base):

    __tablename__ = 'function'

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
