#import os, sys

from pathlib import Path

#sys.path.append(os.getcwd())

import pyglet

class Router:
    def __init__(self, app) -> None:
        self.app = app
        self.pages = {}

    def setup(self):
        from .routes import routes
        self.load_routes(routes)

    def use(self, name):
        import importlib.util
        spec = importlib.util.find_spec(f"client.pages.{name}")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        module, install = module, module.install
        install(self)

    def load_routes(self, routes):
        self.routes = routes
        for route in routes:
            self.use(route)

    def add_page(self, klass, name, title):
        # print(page.__dict__)
        self.pages[name] = { 'klass': klass, 'name': name, 'title': title }

    def go(self, name, **kwargs):
        if not self.app.user.logged_in:
            name = 'login'
        def callback(delta_time):
            entry = self.pages[name]
            self.page = page = entry['klass'].create(self.app, name, entry['title'], **kwargs)
            self.app.show_view(page)
        pyglet.clock.schedule_once(callback, 0)