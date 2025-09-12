class Auth:
    def __init__(self, idms: list[str]):
        self.idms = idms

    def attempt(self, idm: str) -> bool:
        return idm in self.idms