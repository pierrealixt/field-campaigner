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

