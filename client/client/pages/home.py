import arcade
import imgui

from .page import Page

class Home(Page):
    def draw(self):
        imgui.begin("Home")

        imgui.text("Welcome to the Django Arcade!")
        
        imgui.end()

def install(app):
    app.add_page(Home, "home", "Home")