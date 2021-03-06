import arcade
import imgui

NAV = [
    { 'title': 'Home', 'name': 'home'},
    { 'title': 'Users', 'name': 'users'},
    { 'title': 'Counter', 'name': 'counter'},
]

class Page(arcade.View):
    def __init__(self, window, name, title):
        super().__init__(window)
        self.app = window
        self.name = name
        self.title = title

    def reset(self):
        pass

    @classmethod
    def create(self, app, name, title, **kwargs):
        page = self(app, name, title, **kwargs)
        page.reset()
        return page

    def on_draw(self):
        arcade.start_render()

        imgui.new_frame()
        
        if self.window.view_metrics:
            self.window.view_metrics = imgui.show_metrics_window(closable=True)

        self.draw_mainmenu()
        self.draw_navbar()

        imgui.set_next_window_position(288, 32, imgui.ONCE)
        imgui.set_next_window_size(512, 512, imgui.ONCE)

        self.draw()
        
        imgui.end_frame()

    def draw_navbar(self):
        if not self.app.user.logged_in:
            return
        imgui.set_next_window_position(16, 32, imgui.ONCE)
        imgui.set_next_window_size(256, 732, imgui.ONCE)
        
        imgui.begin("Pages")

        router = self.window.router

        if imgui.listbox_header("Pages", -1, -1):

            #for entry in router.pages.values():
            for entry in NAV:
                opened, selected = imgui.selectable(entry['title'], entry['name'] == router.page.name)
                if opened:
                    self.window.router.go(entry['name'])

            imgui.listbox_footer()
        
        imgui.end()

    def draw_mainmenu(self):
        if imgui.begin_main_menu_bar():
            # File
            if imgui.begin_menu('File', True):
                clicked_quit, selected_quit = imgui.menu_item(
                    "Quit", 'Cmd+Q', False, True
                )

                if clicked_quit:
                    exit(1)

                imgui.end_menu()
            # View
            if imgui.begin_menu('View', True):
                clicked_metrics, self.window.view_metrics = imgui.menu_item(
                    "Metrics", 'Cmd+M', self.window.view_metrics, True
                )

                imgui.end_menu()

            imgui.end_main_menu_bar()

    def draw(self):
        pass

    def rel(self, x, y):
        pos = imgui.get_cursor_screen_pos()
        x1 = pos[0] + x
        y1 = pos[1] + y
        return x1, y1
