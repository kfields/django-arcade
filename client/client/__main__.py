import os, sys

sys.path.append(os.getcwd())

import asyncio

from app import App

'''
app = App()

app.setup()

app.run()
'''

async def main():
    """ Main function """
    app = App()
    app.setup()
    await app.run()

if __name__ == "__main__":
    #main()
    asyncio.run(main())