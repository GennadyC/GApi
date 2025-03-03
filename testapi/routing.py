import inspect


class Route:
    def __init__(self):
        self.routes = {}

    def add_route(self, path, method):
        def wrapper(f):
            params = {}
            signature = inspect.signature(f)
            for param in signature.parameters.values():
                params[param.name] = param.default
            
            if path not in self.routes:
                self.routes[path] = {
                    method: {
                        'func': f,
                        'params': params,
                    }
                }
            else:
                self.routes[path][method] = {
                    'func': f,
                    'params': params
                }
            return f

        return wrapper

    def get_method_with_params(self, method, path):
        if path not in self.routes or method not in self.routes[path]:
            return None, None
        return self.routes[path][method]['func'], self.routes[path][method]['params']

    def get(self, path):
        return self.add_route(path, "GET")

    def post(self, path):
        return self.add_route(path, "POST")

    def put(self, path):
        return self.add_route(path, "PUT")

    def delete(self, path):
        return self.add_route(path, "DELETE")
