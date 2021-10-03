import asyncio
import json

from loguru import logger

from gql import gql, Client
from gql.transport.websockets import WebsocketsTransport

#transport = WebsocketsTransport(url='wss://localhost:8000/graphql/')
transport = WebsocketsTransport(url='ws://localhost:8000/graphql/')

client = Client(
    transport=transport,
    #fetch_schema_from_transport=True, #TODO:Ariadne problem?
)

query = gql("""
subscription {
  counter
}
""")


async def main():
    async with client as session:
        #schema = await session.fetch_schema()
        #logger.debug(schema)
        async for result in session.subscribe(query):
            print(json.dumps(result))

if __name__ == "__main__":
    asyncio.run(main())