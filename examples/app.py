from queue import Queue
from threading import Thread, Event
from sys import stdout, stderr
from time import sleep

import asyncio
import json

from loguru import logger

import pyglet
import arcade

import imgui
from arcade_imgui import ArcadeRenderer

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Starting Template"

from gqlrun import GqlRunner

gqlrunner = GqlRunner('localhost:8000/graphql/')

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

        await gqlrunner.start()

        while not self.has_exit:
            timeout = self.idle()
            platform_event_loop.step(timeout)
            gqlrunner.step()
            await asyncio.sleep(0)

        await gqlrunner.stop()
        asyncio.get_event_loop().stop()

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

        pyglet.app.event_loop = EventLoop()


    def setup(self):
        pass

    def draw(self):
        pass

    def on_draw(self):
        """
        Render the screen.
        """

        # This command should happen before we start drawing. It will clear
        # the screen to the background color, and erase what we drew last frame.
        arcade.start_render()

        imgui.new_frame()

        self.draw()

        imgui.end_frame()

        # Call draw() on all your sprite lists below
        self.gui.draw()

    def on_update(self, delta_time):
        """
        All the logic to move, and the game logic goes here.
        Normally, you'll call update() on the sprite lists that
        need it.
        """
        pass

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
