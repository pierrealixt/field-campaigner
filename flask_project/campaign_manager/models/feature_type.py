from sqlalchemy.orm import relationship

class FeatureType(Base):

    __tablename__ = 'featureType'

    featureTemplate = relationship(
        'FeatureTemplate',
        back_populates='featureType'
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
        back_populates='featureTypes'
        )
    attributes = relationship(
        'Attribute',
        secondary=featureTypeAssociations,
        lazy='subquery',
        back_populates='featureTypes'
        )

    def __init__(self, **kwargs):
        super(FeatureType, self).__init__(**kwargs)

