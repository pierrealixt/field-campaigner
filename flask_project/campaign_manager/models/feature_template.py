from sqlalchemy.orm import relationship

class FeatureTemplate(Base):

    __tablename__ = 'featureTemplate'

    featureType = relationship(
        'FeatureType',
        back_populates='featureTemplate'
        )

    def __init__(self, **kwargs):
        super(FeatureTemplate, self).__init__(**kwargs)

