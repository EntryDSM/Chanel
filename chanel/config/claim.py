from sanic_jwt import Claim


class TypeClaim(Claim):
    key = 'type'

    def setup(self, payload, str):
        return 
