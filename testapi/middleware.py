from testapi.response import NotFoundResponseJson, BadRequestResponse
import inspect


class Middleware:
    def __init__(self, route):
        self.route = route

    async def __call__(self,
                       scope,
                       receive,
                       send
                       ):
        if scope['type'] != 'http':
            raise Exception("Only HTTP methods")
        message = await self.read_message(receive)

        response = await self.process_message(scope, message)

        await self.response(response, send)

    async def process_message(self,
                              scope,
                              content: str):
        method = scope['method']
        path = scope['path']
        query_string = self.parse_query_string(scope['query_string'])
        api_func, params = self.route.get_method_with_params(method, path)
        if api_func is None:
            return NotFoundResponseJson()
        kwargs = {}
        for param, default in params.items():
            if param not in query_string and default == inspect._empty:
                return BadRequestResponse(f"Param {param} is required")
            if param in query_string:
                kwargs[param] = query_string[param]
        response = await api_func(**kwargs)
        return response

    @staticmethod
    def parse_query_string(query_string):
        query_string = query_string.decode()
        
        result = '' if not query_string else {x[0]: x[1] for x in [x.split('=') for x in query_string.split('&')]}
        
        return result

    @staticmethod
    async def read_message(receive):
        more_body = True
        body = ''
        while more_body:
            chunk = await receive()
            body += chunk['body'].decode()
            more_body = chunk['more_body']

        return body

    @staticmethod
    async def response(response,
                       send
                       ):
        await send({
            'type': 'http.response.start',
            'status': response.status_code,
            'headers': response.headers
        })
        await send({
            'type': 'http.response.body',
            'body': response.content
        })