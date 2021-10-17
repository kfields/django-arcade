import arcade

class MyGame(arcade.Window):
    """
    Main application class.
    """

    def __init__(self):
        super().__init__(800, 600, "Test")
        self.total_time = 0.0
        self.output = ""
        arcade.set_background_color(arcade.color.ALABAMA_CRIMSON)
        self.total_time = 0.0

    def on_draw(self):
        arcade.start_render()
        arcade.draw_rectangle_filled(400, 300, 100, 100, arcade.color.RED, self.total_time * 100)
        arcade.draw_rectangle_filled(200, 300, 100, 100, arcade.color.BLUE, self.total_time * 120)
        arcade.draw_rectangle_filled(600, 300, 100, 100, arcade.color.GREEN, self.total_time * 140)
        arcade.draw_text(self.output,
                         800 // 2, 600 // 2 - 50,
                         arcade.color.WHITE, 100,
                         anchor_x="center")

    def on_update(self, delta_time):
        self.total_time += delta_time
        self.output = "0" * (int(self.total_time) % 10)


MyGame().run()