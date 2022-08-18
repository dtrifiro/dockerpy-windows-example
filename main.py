import logging
import sys

import docker

logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)
requests_log = logging.getLogger("requests.packages.urllib3")
requests_log.setLevel(logging.DEBUG)
requests_log.propagate = True

client = docker.from_env()


def run(image: str):
    return client.containers.run(
        image,
        command="python -c 'print(\"hello\")'",
        stdout=True,
        stderr=True,
        # detach=True,
        remove=True,
    )


def main():

    try:
        print(f"{client.ping()=}")
    except docker.errors.APIError:
        print("Failed to communicate with the docker client")
        sys.exit(0)

    from urllib.parse import quote

    image = "python"
    # tag = "3.8-slim"
    # pulled = client.images.pull(image)
    # print(f"{pulled=}")
    out = run(image)
    print(f"{out.decode()=}")


if __name__ == "__main__":
    main()
