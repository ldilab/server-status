import GPUtil
import psutil
import time

while True:
    cpu_percent = psutil.cpu_percent(interval=1)
    print("-" * 50)
    print(f"CPU Usage: {cpu_percent}%")

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
        print(f"AccountingMode: {gpu.accounting_mode}")
        print(f"AccountingBuffers: {gpu.accounting_buffers}")
        print(f"AccountingMaxMemoryUsage: {gpu.accounting_max_memory_usage}")
        print(f"AccountingMaxMemoryUsage: {gpu.accounting_max_memory_usage}")
        print(f"AccountingMemoryUsage: {gpu.accounting_memory_usage}")
        print(f"AccountingUtilizationGPU: {gpu.accounting_utilization_gpu}")
        print(f"AccountingUtilizationMemory: {gpu.accounting_utilization_memory}")

    import docker
    docker_client = docker.from_env()
    dockers = docker_client.containers.list()

    time.sleep(1)


