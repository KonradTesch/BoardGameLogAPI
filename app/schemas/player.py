from app.schemas.base import ResponseModel, RequestModel


class PlayerResponse(ResponseModel):
    id: int
    name: str

class PlayerCreate(RequestModel):
    name: str

class PlayerRemove(RequestModel):
    id: int