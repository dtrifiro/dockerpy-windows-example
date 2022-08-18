import sys

import docker

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

    image = "python:3.8-slim"
    try:
        out = run(image)
    except:
        print("Failed running on first try, pulling...")
        pulled = client.images.pull(image)
        print(f"{pulled=}")
        out = run(image)

    print(f"{out.decode()=}")


if __name__ == "__main__":
    main()
