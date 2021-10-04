import arcade
import imgui

from .page import Page


class DemoPage(Page):
    def draw(self):
        imgui.show_test_window()

def install(app):
    app.add_page(DemoPage, 'demo', 'Demo in Demo')
