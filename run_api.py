import uuid
from typing import Optional, Awaitable
from tornado.options import define, options
import tornado.web
from db_init import get_collected_data

define("port", default=8888, type=int)


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            # ("/", MainHandler),
            ("/api/login", ApiLoginHandler),
            ("/api/data", ApiDataHandler),
        ]
        settings = dict(
            xsrf_cookies=True,
            cookie_secret=uuid.uuid4().int,
            debug=True,
        )
        super(Application, self).__init__(handlers, **settings)


# class MainHandler(tornado.web.RequestHandler):
#     def data_received(self, chunk: bytes) -> Optional[Awaitable[None]]:
#         pass
#
#     def get(self):
#         self.write('Main Handler')


class ApiLoginHandler(tornado.web.RequestHandler):
    def data_received(self, chunk: bytes) -> Optional[Awaitable[None]]:
        pass

    def prepare(self):
        self.set_header("Content-Type", "application/json")

    def get(self):
        self.write('{"handler": "Api Login Handler"}')


class ApiDataHandler(tornado.web.RequestHandler):
    def data_received(self, chunk: bytes) -> Optional[Awaitable[None]]:
        pass

    def prepare(self):
        self.set_header("Content-Type", "application/json")

    def get(self):
        self.write('{"handler": "Api Data Handler"}')


if __name__ == "__main__":
    app = Application()
    app.listen(options.port)
    tornado.ioloop.IOLoop.current().start()
