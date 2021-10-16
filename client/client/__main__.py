import os, sys

sys.path.append(os.getcwd())

import asyncio

from app import App

def main():
    """ Main function """
    app = App()
    app.run()

if __name__ == "__main__":
    main()
