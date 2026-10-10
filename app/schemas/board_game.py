from app.schemas.base import ResponseModel, RequestModel


class BoardGameResponse(ResponseModel):
    id: int
    title: str

class AddBoardGameRequest(RequestModel):
    title: str

class EditBoardGameRequest(RequestModel):
    new_title: str
