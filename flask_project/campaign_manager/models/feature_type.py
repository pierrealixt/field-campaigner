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

    def get_templates(self):
        """ Returns the templates feature types """
        return session.query(FeatureType).filter(
            FeatureType.is_template == true()
            ).all()

    def create(self):
        """ Creates and saves the current model to DB """
        session.add(self)
        session.commit()

