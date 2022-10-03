from email.policy import default
from sqlalchemy import (
    Boolean,
    Column,
    ForeignKey,
    Integer,
    String,
    Enum,
    UniqueConstraint
)
from sqlalchemy.orm import relationship

from database.database import Base


# task status enum
statuses = ('failed', 'running', 'success')
status_enum = Enum(*statuses, name='status_enum')
default_status = 'running'

# integration names enum
integrations = ('etherscan', 'selectel')
integration_enum = Enum(*integrations, name='integration_enum')


class IntegrationTask(Base):
    __tablename__ = 'integration_tasks'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=False)
    status = Column(status_enum, default=default_status)

    integration_statuses = relationship('Integration', back_populates='integration_task')


class Integration(Base):
    __tablename__ = 'integrations'

    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(Integer, ForeignKey('integration_tasks.id'), index=True)
    name = Column(integration_enum, nullable=False)
    retry_counter = Column(Integer, default=0)
    status = Column(status_enum, default=default_status)

    integration_task = relationship('IntegrationTask', back_populates='integration_statuses')

    __table_args__ = (
        UniqueConstraint('task_id', 'name', name='_task_name_uc'),
    )
