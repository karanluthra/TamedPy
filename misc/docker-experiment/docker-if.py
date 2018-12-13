import docker

client = docker.from_env()
print(client.containers.run("tamedpy"))
