import GPUtil
import psutil
import time

while True:
    cpu_percent = psutil.cpu_percent(interval=1)
    print("-" * 50)
    print(f"CPU Usage: {cpu_percent}%")
    print(f"CPU Count: {psutil.cpu_count()}")
    print(f"CPU Frequency: {psutil.cpu_freq()}")
    print(f"CPU Stats: {psutil.cpu_stats()}")
    print(f"CPU Times: {psutil.cpu_times()}")
    print(f"CPU Times Percent: {psutil.cpu_times_percent()}")
    print(f"CPU Percent: {psutil.cpu_percent()}")
    print(f"CPU Percent Per CPU: {psutil.cpu_percent(percpu=True)}")


    mem = psutil.virtual_memory()
    mem_percent = mem.percent
    print("-" * 50)
    print(f"Memory Usage: {mem_percent}%")
    print(f"Memory Total: {mem.total}")
    print(f"Memory Available: {mem.available}")
    print(f"Memory Used: {mem.used}")
    print(f"Memory Free: {mem.free}")
    print(f"Memory Active: {mem.active}")
    print(f"Memory Inactive: {mem.inactive}")

    disks = psutil.disk_partitions()
    print("-" * 50)
    for disk in disks:
        print("-" * 50)
        print(f"Device: {disk.device}")
        print(f"Mountpoint: {disk.mountpoint}")
        print(f"Fstype: {disk.fstype}")
        print(f"Opts: {disk.opts}")
        print(f"Total: {psutil.disk_usage(disk.mountpoint).total}")
        print(f"Used: {psutil.disk_usage(disk.mountpoint).used}")
        print(f"Free: {psutil.disk_usage(disk.mountpoint).free}")
        print(f"Percent: {psutil.disk_usage(disk.mountpoint).percent}")

    gpus = GPUtil.getGPUs()
    print("-" * 50)
    for gpu in gpus:
        print("-" * 50)
        print(f"ID: {gpu.id}")
        print(f"Name: {gpu.name}")
        print(f"Load: {gpu.load}")
        print(f"MemoryTotal: {gpu.memoryTotal}")
        print(f"MemoryUsed: {gpu.memoryUsed}")
        print(f"MemoryFree: {gpu.memoryFree}")
        print(f"MemoryUtil: {gpu.memoryUtil}")
        print(f"Temperature: {gpu.temperature}")
        print(f"UUID: {gpu.uuid}")
        print(f"Serial: {gpu.serial}")
        print(f"DisplayMode: {gpu.display_mode}")
        print(f"DisplayActive: {gpu.display_active}")

    import docker
    docker_client = docker.from_env()
    docker_containers = docker_client.containers.list()
    docker_images = docker_client.images.list()
    print("-" * 50)
    for docker_container in docker_containers:
        print("-" * 50)
        print(f"ID: {docker_container.id}")
        print(f"Name: {docker_container.name}")
        print(f"Image: {docker_container.image}")
        print(f"Status: {docker_container.status}")
        print(f"Ports: {docker_container.ports}")
        print(f"Attrs: {docker_container.attrs}")
        print(f"Mounts: {docker_container.attrs['Mounts']}")
        print(f"NetworkSettings: {docker_container.attrs['NetworkSettings']}")
        print(f"State: {docker_container.attrs['State']}")

    for docker_image in docker_images:
        print("-" * 50)
        print(f"ID: {docker_image.id}")
        print(f"Tags: {docker_image.tags}")
        print(f"Labels: {docker_image.labels}")
        print(f"Attrs: {docker_image.attrs}")
        print(f"ParentId: {docker_image.attrs['ParentId']}")
        print(f"RepoDigests: {docker_image.attrs['RepoDigests']}")
        print(f"RepoTags: {docker_image.attrs['RepoTags']}")
        print(f"SharedSize: {docker_image.attrs['SharedSize']}")
        print(f"Size: {docker_image.attrs['Size']}")
        print(f"VirtualSize: {docker_image.attrs['VirtualSize']}")
        print(f"Created: {docker_image.attrs['Created']}")
        print(f"Container: {docker_image.attrs['Container']}")
        print(f"ContainerConfig: {docker_image.attrs['ContainerConfig']}")
        print(f"GraphDriver: {docker_image.attrs['GraphDriver']}")
        print(f"Os: {docker_image.attrs['Os']}")
        print(f"Architecture: {docker_image.attrs['Architecture']}")
        print(f"Author: {docker_image.attrs['Author']}")
        print(f"Config: {docker_image.attrs['Config']}")
        print(f"RootFS: {docker_image.attrs['RootFS']}")


    time.sleep(1)


