import logging
import sys
import time

import docker

logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)
requests_log = logging.getLogger("requests.packages.urllib3")
requests_log.setLevel(logging.DEBUG)
requests_log.propagate = True

import http.client

http.client.HTTPConnection.debuglevel = 5

client = docker.from_env()


def run(image: str):
    return client.containers.run(
        image,
        command="python -c 'print(\"hello\")'",
        stdout=True,
        stderr=True,
        detach=True,
        remove=True,
    )


def main():

    try:
        print(f"{client.ping()=}")
    except docker.errors.APIError:
        print("Failed to communicate with the docker client")
        sys.exit(0)

    from urllib.parse import quote

    container = client.containers.run(
        "fsouza/fake-gcs-server",
        command="echo hello",
        name="testing-python",
        stdout=True,
        stderr=True,
        detach=True,
        remove=True,
        ports={f"{10000}/tcp": None},  # assign a random port
    )
    # time.sleep(5)
    out = container.logs()
    print(f"{out.decode()=}")

    container.kill()
    print("killed container")


if __name__ == "__main__":
    main()
