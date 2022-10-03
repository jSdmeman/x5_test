from pydantic import BaseModel


class IntegrationBase(BaseModel):
    pass


class IntegrationCreate(IntegrationBase):
    name: str


class Integration(IntegrationBase):
    name: str
    status: str
    retry_counter: int

    class Config:
        orm_mode = True


class IntegrationTaskBase(BaseModel):
    pass


class IntegrationTaskCreate(IntegrationTaskBase):
    name: str


class IntegrationTaskCreated(IntegrationTaskBase):
    task_id: int


class IntegrationTask(IntegrationTaskBase):
    id: int
    name: str
    status: str
    integration_statuses: list[Integration] = []

    class Config:
        orm_mode = True