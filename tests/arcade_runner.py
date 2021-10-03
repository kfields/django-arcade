from queue import Queue
from threading import Thread, Event
from sys import stdout, stderr
from time import sleep

import asyncio
import json

from loguru import logger

from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport
from gql.transport.websockets import WebsocketsTransport

import pyglet
import arcade

import imgui
from arcade_imgui import ArcadeRenderer

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Starting Template"

#
#
#

class GqlJob:
    def __init__(self, fn, cb):
        self.fn = fn
        self.cb = cb
        self.result = None

class GqlRunner:
    def __init__(self, url, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.url = url
        self.jobs = []
        self.results = []
        '''
        self.httpClient = Client(
            transport=AIOHTTPTransport(url='http://' + url),
            fetch_schema_from_transport=True
        )
        '''
        self.wsClient = Client(
            transport=WebsocketsTransport(url='ws://' + url),
        )

    async def start(self):
        self.wsSession = await self.wsClient.__aenter__()

    async def stop(self):
        await self.wsClient.__aexit__()

    def add(self, fn, cb):
        self.jobs.append(GqlJob(fn, cb))

    def do_callbacks(self):
        while len(self.results) != 0:
            result = self.results.pop(0)
            result[0](result[1])

    def step(self):
        while len(self.jobs) != 0:
            job = self.jobs.pop(0)
            task = asyncio.create_task(job.fn())

        self.do_callbacks()

    def execute(self, query, cb):
        #logger.debug('execute')
        async def fn():
            client = Client(
                transport=AIOHTTPTransport(url='http://' + self.url),
                fetch_schema_from_transport=True
            )

            async with client as session:
                #logger.debug('execute response')
                result = await session.execute(query)
                #logger.debug(result)
                cb(result)
        self.add(fn, cb)

    def subscribe(self, query, cb):
        async def fn(): 
            session = self.wsSession
            async for result in session.subscribe(query):
                cb(result)
        self.add(fn, cb)


runner = GqlRunner('localhost:8000/graphql/')

getMessageQuery = gql("""
query {
  getMessage
}
""")

counterQuery = gql("""
subscription {
  counter
}
""")

counter2Query = gql("""
subscription {
  counter2
}
""")

def cb(data):
    print(data)

class Gui:
    def __init__(self, window):
        self.window = window
        # Must create or set the context before instantiating the renderer
        imgui.create_context()
        self.renderer = ArcadeRenderer(window)

    def draw(self):
        imgui.render()
        self.renderer.render(imgui.get_draw_data())

class MyGame(arcade.Window):
    """
    Main application class.

    NOTE: Go ahead and delete the methods you don't need.
    If you do need a method, delete the 'pass' and replace it
    with your own code. Don't leave 'pass' in this program.
    """

    def __init__(self, width, height, title):
        super().__init__(width, height, title, resizable=True)
        self.gui = Gui(self)
        arcade.set_background_color(arcade.color.AMAZON)

        self.test_input = 0

    def setup(self):
        """ Set up the game variables. Call to re-start the game. """
        # Create your sprites and sprite lists here

        runner.subscribe(counterQuery, cb)
        runner.subscribe(counter2Query, cb)


    def on_draw(self):
        """
        Render the screen.
        """

        # This command should happen before we start drawing. It will clear
        # the screen to the background color, and erase what we drew last frame.
        arcade.start_render()

        imgui.new_frame()

        imgui.begin("Test Window")

        imgui.text("This is the test window.")
        changed, self.test_input = imgui.input_int("Integer Input Test", self.test_input)

        imgui.end()

        imgui.end_frame()

        # Call draw() on all your sprite lists below
        self.gui.draw()

    def on_update(self, delta_time):
        """
        All the logic to move, and the game logic goes here.
        Normally, you'll call update() on the sprite lists that
        need it.
        """
        runner.execute(getMessageQuery, cb)

    def on_key_press(self, key, key_modifiers):
        """
        Called whenever a key on the keyboard is pressed.

        For a full list of keys, see:
        https://api.arcade.academy/en/latest/arcade.key.html
        """
        pass

    def on_key_release(self, key, key_modifiers):
        """
        Called whenever the user lets off a previously pressed key.
        """
        pass

    def on_mouse_motion(self, x, y, delta_x, delta_y):
        """
        Called whenever the mouse moves.
        """
        pass

    def on_mouse_press(self, x, y, button, key_modifiers):
        """
        Called when the user presses a mouse button.
        """
        pass

    def on_mouse_release(self, x, y, button, key_modifiers):
        """
        Called when a user releases a mouse button.
        """
        pass

class EventLoop(pyglet.app.EventLoop):
    
    async def main(self, interval=1/60):
        """Begin processing events, scheduled functions and window updates.

        This method returns when :py:attr:`has_exit` is set to True.

        Developers are discouraged from overriding this method, as the
        implementation is platform-specific.
        """
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

        await runner.start()

        while not self.has_exit:
            timeout = self.idle()
            platform_event_loop.step(timeout)
            runner.step()
            await asyncio.sleep(0)

        await runner.stop()

        self.is_running = False
        self.dispatch_event('on_exit')
        platform_event_loop.stop()


    def run(self, interval=1/60):
        asyncio.run(self.main(interval))

pyglet.app.event_loop = EventLoop()

def main():
    """ Main function """
    game = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()