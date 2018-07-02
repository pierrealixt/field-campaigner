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

    def create(self):
        """ Creates and saves the current model to DB """
        session.add(self)
        session.commit()

    def save(self):
        session.commit()

    def get_by_uuid(self, uuid):
        """ Returns the campaign object based on the uuid """
        return session.query(Campaign).filter(Campaign.uuid == uuid).first()

    def get_all(self):
        """ Returns all the campaigns in the DB """
        return session.query(Campaign).all()

    def get_all_active(self):
        """ Returns all the active campaigns """
        from datetime import datetime
        date = datetime.now()
        return session.query(Campaign).filter(
            and_(
                Campaign.start_date <= date,
                date <= Campaign.end_date)
            ).all()

    def get_all_inactive(self):
        """ Returns all the inactive campaigns """
        from datetime import datetime
        date = datetime.now()
        return session.query(Campaign).filter(
            or_(Campaign.start_date >= date,
                date >= Campaign.end_date)
            ).all()

    def get_task_boundary(self):
        """ Returns the task_boundary of the campaign """
        return session.query(TaskBoundary).filter(
            TaskBoundary.campaign_id == self.id
            ).first()

    def get_task_boundary_as_geoJSON(self):
        """ Returns the task boundary in GeoJSON format """
        return session.query(
            TaskBoundary.coordinates.ST_AsGeoJSON()
            ).filter(
            TaskBoundary.campaign_id == self.id
            ).first()

    def update(self, campaign_dto):
        """ Updates and saves the model object """
        from datetime import datetime
        if campaign_dto['name']:
            self.name = campaign_dto['name']
        if campaign_dto['description']:
            self.description = campaign_dto['description']
        if campaign_dto['start_date']:
            self.start_date = campaign_dto['start_date']
        if campaign_dto['end_date']:
            self.end_date = campaign_dto['end_date']
        self.create_on = datetime.now()
        session.commit()

