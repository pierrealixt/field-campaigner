class Team(Base):

    __tablename__ = 'team'

    boundary = relationship(
        'TaskBoundary',
        back_populates='team'
        )
    users = relationship(
        'User',
        secondary=teamUserAssociations,
        lazy='subquery',
        back_populates='teams'
        )

    def __init__(self, **kwargs):
        super(Team, self).__init__(**kwargs)

    def create(self):
        """ Creates and saves the current model to DB """
        session.add(self)
        session.commit()

    def get_all(self):
        """ Returns all the teams registered in field campaigner """
        return session.query(Team).all()
