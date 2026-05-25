class NotFoundException(Exception):
    def __init__(self, detail):
        self.detail = detail
        super().__init__(self.detail)

class UnprocessableException(Exception):
    def __init__(self, detail):
        self.detail = detail
        super().__init__(self.detail)

class UnauthorizedException(Exception):
    def __init__(self, detail):
        self.detail = detail
        super().__init__(self.detail)

