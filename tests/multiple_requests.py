import argparse

from httpx import Client
from alive_progress import alive_bar


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--count", type=int, default=10000)
    parser.add_argument("--address", type=str, default="localhost")
    parser.add_argument("--port", type=int, default=8000)
    parser.add_argument("--endpoint", type=str, default="tasks")
    parser.add_argument("--delay", type=str, default="1")
    args = parser.parse_args()

    client = Client()
    with alive_bar(args.count) as bar:
        for i in range(args.count):
            response = client.post(
                url="http://{address}:{port}/{endpoint}".format(
                    address=args.address, port=args.port, endpoint=args.endpoint
                ),
                data=args.delay,
                headers={"Content-Type": "application/json"},
            )
            result = response.json()
            assert "id" in result
            bar()
    client.close()
