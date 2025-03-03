import typing
import json


class BaseResponse:
    """
    Base response class
    """
    def __init__(self,
                 content: str = None,
                 status_code: int = None,
                 headers: typing.Mapping[str, str] | None = None
                 ):
        self.content_type = None
        self.render_content(content=content)
        self.status_code = status_code
        self.headers = self.render_headers(headers)
    
    def render_content(self, content):
        if type(content) == dict:
            self.content = json.dumps(content).encode('utf-8')
            self.content_type = 'application/json'
        elif type(content) == str:
            self.content = content.encode('utf-8')
            self.content_type = 'text/plain; charset="utf-8"'
        elif content is None:
            self.content = json.dumps({}).encode('utf-8')
            self.content_type = 'application/json'
        else:
            raise Exception("Content type {} is not supported yet".format(type(content)))

    def render_headers(self, headers):
        need_append_content_type = True
        need_append_content_length = True
        if headers is None:
            headers = []
        else:
            for h in headers:
                if 'content-type' == h[0].lower():
                    need_append_content_type = False
                if 'content-length' == h[0].lower():
                    need_append_content_length = False
        
        if need_append_content_type:
            headers.append(['Content-Type', self.content_type])
        
        if need_append_content_length:
            headers.append(['Content-Lenght', str(len(self.content))])
        
        return headers


class HTTPResponse(BaseResponse):
    """
    Class for custom response
    """
    def __init__(self,
                 content: str = '',
                 status_code: int = 200,
                 headers: typing.Mapping[str, str] | None = None
                 ):
        if status_code is None:
            raise Exception("Status code can't be None")
        super.__init__(content=content, status_code=status_code, headers=headers)


class JSONResponse(BaseResponse):
    """
    JSONResponse
    """
    def __init__(self,
                 content: typing.Any,
                 status_code: int = 200
                 ):
        if status_code is None:
            raise Exception("Status code can't be None")
        super().__init__(
            content=content,
            status_code=status_code,
            headers=[["Content-Type", "application/json"]]
        )


class TextPlainResponse(BaseResponse):
    """
    Text response
    """
    def __init__(self,
                 content: str = '',
                 status_code: int = 200):
        if status_code is None:
            raise Exception("Status code can't be None")
        super().__init__(
            content=content,
            status_code=status_code,
            headers=[["Content-Type", "text/plain; charset=\"utf-8\""]]
        )


class NotFoundResponseText(TextPlainResponse):
    """
    Not found response in text format
    """
    def __init__(self,
                 content: str | None = None
                 ):
        if content is None:
            content = "Not Found"
        super().__init__(
            content=content,
            status_code=404
        )


class NotFoundResponseJson(JSONResponse):
    """
    Not found response in json format
    """
    def __init__(self,
                 content: typing.Mapping[str, str] | None = None,
                 ):
        if content is None:
            content = {"Error": "Not Found"}
        super().__init__(
            content=content,
            status_code=404
        )


class BadRequestResponse(JSONResponse):
    """
    Bad request response
    """
    def __init__(self, 
                 content: typing.Mapping[str, str] | None = None,
                 ):
        if content is None:
            content = {"Error": "request error"}
        super().__init__(
            content,
            status_code=400
            )
