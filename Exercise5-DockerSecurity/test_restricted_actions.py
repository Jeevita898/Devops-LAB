import docker

client = docker.from_env()
container = None

try:
    container = client.containers.run(
        "flask-apparmor",
        detach=True,
        security_opt=["apparmor=my-apparmor-profile"]
    )

    print("Container started with AppArmor profile.")
    print("AppArmor profile:", container.attrs["AppArmorProfile"])

    # Test 1: Read /etc/passwd
    print("\nTest 1: Read /etc/passwd")
    result = container.exec_run([
        "python", "-c", "open('/etc/passwd').read()"
    ])
    print("Result:", "BLOCKED" if result.exit_code != 0 else "ALLOWED")

    # Test 2: Read /etc/shadow
    print("\nTest 2: Read /etc/shadow")
    result = container.exec_run([
        "python", "-c", "open('/etc/shadow').read()"
    ])
    print("Result:", "BLOCKED" if result.exit_code != 0 else "ALLOWED")

    # Test 3: Execute Bash
    print("\nTest 3: Execute Bash")
    result = container.exec_run([
        "/usr/bin/bash", "-c", "echo Bash executed"
    ])
    print("Result:", "ALLOWED" if result.exit_code == 0 else "BLOCKED")
    print("Note: Bash execution is not successfully restricted yet.")

finally:
    if container is not None:
        container.stop(timeout=2)
        container.remove()
        print("\nTest container cleaned up.")
