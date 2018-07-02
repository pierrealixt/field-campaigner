from sqlalchemy.orm import relationship

class TaskBoundary(Base):

    __tablename__ = 'taskBoundary'

    team = relationship(
        'Team',
        back_populates='boundary',
        lazy=True,
        uselist=False
        )
    campaign = relationship(
        'Campaign',
        back_populates='taskBoundaries',
        lazy=True
        )

    def __init__(self, **kwargs):
        super(TaskBoundary, self).__init__(**kwargs)

    def create(self):
        """ Creates and saves the current model to DB """
        session.add(self)
        session.commit()
