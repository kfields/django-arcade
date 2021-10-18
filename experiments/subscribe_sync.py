import asyncio
import json

from loguru import logger

from gql import gql, Client
from gql.transport.websockets import WebsocketsTransport

transport = WebsocketsTransport(url='ws://localhost:8000/graphql/')

client = Client(
    transport=transport,
    #fetch_schema_from_transport=True, #TODO:Ariadne and a lot of servers only support subscriptions over websockets!
)

query = gql("""
subscription {
  counter
}
""")


def main():
    for result in client.subscribe(query):
        print (result)

if __name__ == "__main__":
    main()