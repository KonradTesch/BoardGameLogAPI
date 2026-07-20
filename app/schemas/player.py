from app.schemas.base import ResponseModel, RequestModel

class UpdatePlayerRequest(RequestModel):
    new_name: str

class PlayerResponse(ResponseModel):
    id: int
    name: str

class PlayerCreate(RequestModel):
    name: str
