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


def main():
    for result in client.subscribe(query):
        print (result)

if __name__ == "__main__":
    main()