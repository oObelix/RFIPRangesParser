from typing import List, Tuple, Any, Dict
import uuid
from typing import Optional, Awaitable
from tornado import web
from tornado.auth import AuthError
from config import Config
from tornado.options import define, options
import tornado.ioloop
from db_session import session
from models import CollectedData, Users
import jwt

config = Config()
JWT_SECRET = config.jwt_secret
PREFIX = 'Bearer '

config = Config()
define("port", default=config.server_port, type=int)


class Application(tornado.web.Application):
    def __init__(self):
        handlers: List[Tuple[str, Any]] = [
            ("/api/login", ApiLoginHandler),
            ("/api/data", ApiDataHandler),
        ]
        settings: dict = dict(
            xsrf_cookies=False,
            cookie_secret=uuid.uuid4().int,
            debug=True,
        )
        super(Application, self).__init__(handlers, **settings)


class ApiLoginHandler(tornado.web.RequestHandler):
    """
    Login Handler.
    This method aim to provide a new authorization token upon database
    credentials success.
    """
    def data_received(self, chunk: bytes) -> Optional[Awaitable[None]]:
        pass

    def prepare(self):
        self.set_header("Content-Type", "application/json")

    def get(self):
        pass

    def post(self):
        try:
            login: str = self.get_argument("login")
            password: str = self.get_argument("password")
        except web.MissingArgumentError as e:
            self.write({"Error": "Missing arguments"})
        else:
            if Users.valid(session, login, password):
                user: Any = Users.data_by_login(session, login)

                encoded: str = jwt.encode({
                    'id': user.id,
                },
                    JWT_SECRET,
                    algorithm='HS256'
                )
                response: Dict[str, str] = {'token': encoded}
                self.write(response)
            else:
                self.set_status(401)
                self.write({"Error": "Auth Failed!"})


class ApiDataHandler(tornado.web.RequestHandler):
    """
    Api Data Handler.
    Needs Authorization with token to access it.
    """
    def data_received(self, chunk: bytes) -> Optional[Awaitable[None]]:
        pass

    def prepare(self):
        self.set_header("Content-Type", "application/json")

    def post(self):
        pass

    def get(self):
        # print(self.request.headers)
        try:
            token: str = self.request.headers.get("Authorization"
                                                  )[len(PREFIX):]
            decoded: Dict[str, int] = jwt.decode(token, SECRET,
                                                 algorithms='HS256')
            if not Users.valid_id(session, decoded['id']):
                raise AuthError("Invalid token or token was expired")
        except BaseException as e:
            # print(e)
            self.set_status(401)
            self.write({"Error": str(e)})
        else:
            # print(decoded, type(decoded))
            Users.connected(session, decoded['id'])
            data: List[Any] = CollectedData.get_collected_data(session)
            total: int = len(data)
            result: Dict[Optional] = {
                "data": [{"id": item.id,
                          "begin_ip_address": item.begin_ip_address,
                          "end_ip_address": item.end_ip_address,
                          "total_count": item.total_count
                          } for item in data],
                "total": total
            }
            self.write(result)


if __name__ == "__main__":
    app: Any = Application()
    app.listen(options.port)
    tornado.ioloop.IOLoop.current().start()
