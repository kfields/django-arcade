import os, sys

sys.path.append(os.getcwd())

from app import App

app = App()

app.setup()

app.run()
