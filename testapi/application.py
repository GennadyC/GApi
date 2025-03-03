from testapi.routing import Route
from testapi.middleware import Middleware


class Application:
    def __init__(self):
        self.route = Route()
        self.middleware = Middleware(self.route)

    async def __call__(self,
                       scope,
                       receive,
                       send):
        await self.middleware(scope, receive, send)

    def get(self, path):
        return self.route.get(path)

    def post(self, path):
        return self.route.post(path)

    def put(self, path):
        return self.route.put(path)

    def delete(self, path):
        return self.route.delete(path)
