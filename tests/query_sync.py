import asyncio
import json

from loguru import logger

from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
from gql.transport.websockets import WebsocketsTransport

transport = RequestsHTTPTransport(url='http://localhost:8000/graphql/')

client = Client(
    transport=transport,
    fetch_schema_from_transport=True
)

query = gql("""
query {
  getMessage
}
""")


def main():
    result = client.execute(query)
    print(result)

if __name__ == "__main__":
    main()