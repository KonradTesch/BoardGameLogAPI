from app.schemas.base import ResponseModel

class PlayerResponse(ResponseModel):
    id: int
    name: str