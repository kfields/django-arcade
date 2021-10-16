import asyncio

import os
from pathlib import Path

from loguru import logger

import pyglet
import arcade
import imgui

from arcade_imgui import ArcadeRenderer

from router import Router

from gqlrun import GqlRunner

from user import User

gqlrunner = GqlRunner('localhost:8000/graphql/')

async def run(interval=1/60):
    """Begin processing events, scheduled functions and window updates.

    This is a convenience function, equivalent to::

        pyglet.app.event_loop.run()

    """
    return await pyglet.app.event_loop.run(interval)

class EventLoop(pyglet.app.EventLoop):
    
    async def main(self, interval=1/60):
        self.clock.schedule_interval_soft(self._redraw_windows, interval)

        self.has_exit = False

        from pyglet.window import Window
        Window._enable_event_queue = False

        # Dispatch pending events
        for window in pyglet.app.windows:
            window.switch_to()
            window.dispatch_pending_events()

        platform_event_loop = pyglet.app.platform_event_loop
        platform_event_loop.start()
        self.dispatch_event('on_enter')
        self.is_running = True

        async with gqlrunner:
            while not self.has_exit:
                timeout = self.idle()
                platform_event_loop.step(timeout)
                await gqlrunner.step()

        self.is_running = False
        self.dispatch_event('on_exit')
        platform_event_loop.stop()

    def run(self, interval=1/60):
        asyncio.run(self.main(interval))

class Gui:
    def __init__(self, window):
        self.window = window
        # Must create or set the context before instantiating the renderer
        imgui.create_context()
        self.renderer = ArcadeRenderer(window)

    def draw(self):
        imgui.render()
        self.renderer.render(imgui.get_draw_data())

class App(arcade.Window):
    def __init__(self):
        super().__init__(1024, 768, "Django Arcade", resizable=True)
        self.runner = gqlrunner
        self.user = User()
        self.router = Router(self)
        self.gui = Gui(self)
        self.view_metrics = False
        self.resource_path = Path(__file__).parent.parent / 'resources'
        file_path = os.path.dirname(os.path.abspath(__file__))
        #print(file_path)
        os.chdir(file_path)
        arcade.set_background_color(arcade.color.AMAZON)

        pyglet.app.event_loop = EventLoop()

    def setup(self):
        self.router.setup()
        self.router.go('home')


    def on_draw(self):
        super().on_draw()
        self.gui.draw()

    def run(self, interval=1/60):
        self.setup()
        arcade.run()
