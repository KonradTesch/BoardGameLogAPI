from app.schemas.base import ResponseModel

class BoardGameResponse(ResponseModel):
    id: int
    title: str
    user_id: int