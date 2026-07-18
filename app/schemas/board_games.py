from app.schemas.base import ResponseModel, RequestModel


class BoardGameResponse(ResponseModel):
    id: int
    title: str
    user_id: int

class AddBoardGameRequest(RequestModel):
    title: str

class RemoveBoardGameRequest(RequestModel):
    id: int