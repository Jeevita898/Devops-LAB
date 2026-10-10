import docker

client = docker.from_env()

image_name = "flask-apparmor"
container_name = "apparmor-test"

try:
    container = client.containers.run(
        image_name,
        name=container_name,
        detach=True,
        ports={"5000/tcp": 5000},
        security_opt=["apparmor=my-apparmor-profile"]
    )

    container.reload()

    print("Container started successfully!")
    print("Container ID:", container.short_id)
    print("Status:", container.status)

    print("\nSecurity Options:")
    print(container.attrs["HostConfig"]["SecurityOpt"])

    print("\nAppArmor Profile:")
    print(container.attrs["AppArmorProfile"])

    print("\nTest the Flask application at http://localhost:5000")

except docker.errors.APIError as e:
    print("Docker API error:", e)

finally:
    try:
        container.stop(timeout=2)
        container.remove()
        print("\nTest container stopped and removed.")
    except (NameError, docker.errors.NotFound):
        pass
