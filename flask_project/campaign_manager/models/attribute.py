class Attribute(Base):

    __tablename__ = 'attribute'

    featureTypes = relationship(
        'FeatureType',
        secondary=featureTypeAssociations,
        lazy='subquery',
        back_populates='attributes'
        )

    def __init__(self, **kwargs):
        super(Attribute, self).__init__(**kwargs)
