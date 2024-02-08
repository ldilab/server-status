import json
import time
import datetime
from io import StringIO

import docker
import gpustat
import psutil
from GPUtil import GPUtil


class Monitor:
    def __init__(self, update_interval=10):
        self.update_interval = update_interval

        self.last_update = time.time()

        self.system_client = psutil
        self.gpu_client = GPUtil
        try:
            self.docker_client = docker.from_env()
        except:
            self.docker_client = None

        self.cpu_infos = {}
        self.memory_infos = {}
        self.disk_infos = {}
        self.gpu_infos = {}

        self.docker_container_infos = {}
        self.docker_image_infos = {}

        self._set_cpu_init_info()
        self._set_memory_init_info()
        self._set_disk_init_info()
        self._set_gpu_init_info()

        self.cpu = {}
        self.memory = {}
        self.disks = {}
        self.gpus = {}
        self.docker_containers = {}
        self.docker_images = {}

    def _set_cpu_init_info(self):
        try:
            self.cpu_infos["cpu_count"] = self.system_client.cpu_count()
        except:
            pass

    def _set_memory_init_info(self):
        try:
            mem = self.system_client.virtual_memory()
            self.memory_infos["total"] = mem.total
        except:
            pass

    def _set_disk_init_info(self):
        wanted_fs = ["ext4", "ext3", "ext2", "ext1", "xfs", "btrfs", "nfs"]
        try:
            all_disks = self.system_client.disk_partitions(all=True)
            host_disks = filter(lambda disk: disk.mountpoint.startswith("/host"), all_disks)
            host_disks = filter(lambda disk: disk.fstype in wanted_fs, host_disks)
            disks = list(host_disks)

            for disk in disks:
                mount_point = disk.mountpoint.replace("/host", "")
                if mount_point == "":
                    mount_point = "/"
                self.disk_infos[mount_point] = {
                    "device": disk.device,
                    "mount": mount_point,
                    "fstype": disk.fstype,
                    "total": self.system_client.disk_usage(disk.mountpoint).total
                }
        except:
            pass

    def _set_gpu_init_info(self):
        try:
            gpus = self.gpu_client.getGPUs()
            for gpu in gpus:
                self.gpu_infos[gpu.id] = {
                    "name": gpu.name,
                    "memory_total": gpu.memoryTotal,
                    "uuid": gpu.uuid,
                    "serial": gpu.serial
                }
        except:
            pass

    def get_cpu_info(self) -> dict:
        try:
            dynamic_cpu_infos = {
                "used": {
                    "percent": self.system_client.cpu_percent(interval=None)  # Non-blocking way
                }
            }
        except:
            dynamic_cpu_infos = {}

        return {
            "dynamic": dynamic_cpu_infos,
            "static": self.cpu_infos
        }

    def get_memory_info(self) -> dict:
        try:
            mem = self.system_client.virtual_memory()
            dynamic_memory_infos = {
                # "used": {
                #     "percent": round(mem.used / mem.total * 100, 2),
                #     "raw": mem.used
                # },
                "available": {
                    "percent": round(mem.available / mem.total * 100, 2),
                    "raw": mem.available
                },
                # "free": {
                #     "percent": round(mem.free / mem.total * 100, 2),
                #     "raw": mem.free
                # },
            }
        except:
            dynamic_memory_infos = {}

        return {
            "dynamic": dynamic_memory_infos,
            "static": self.memory_infos
        }

    def get_disk_info(self) -> dict:
        wanted_fs = ["ext4", "ext3", "ext2", "ext1", "xfs", "btrfs", "nfs"]
        try:
            all_disks = self.system_client.disk_partitions(all=True)
            host_disks = filter(lambda disk: disk.mountpoint.startswith("/host"), all_disks)
            host_disks = filter(lambda disk: disk.fstype in wanted_fs, host_disks)

            disks = list(host_disks)

            dynamic_disk_infos = {}
            for disk in disks:
                mount_point = disk.mountpoint.replace("/host", "")
                if mount_point == "":
                    mount_point = "/"
                dynamic_disk_infos[mount_point] = {
                    # "used": {
                    #     "percent": self.system_client.disk_usage(disk.mountpoint).percent,
                    #     "raw": self.system_client.disk_usage(disk.mountpoint).used
                    # },
                    "free": {
                        "percent": 100 - self.system_client.disk_usage(disk.mountpoint).percent,
                        "raw": self.system_client.disk_usage(disk.mountpoint).free
                    },
                }
        except:
            dynamic_disk_infos = {}

        return {
            "dynamic": dynamic_disk_infos,
            "static": self.disk_infos
        }

    def get_gpu_info(self) -> dict:
        try:
            gpustats = gpustat.new_query()
            fp = StringIO()
            gpustats.print_json(fp=fp)
            gpu_all = json.loads(fp.getvalue())
            gpus = gpu_all["gpus"]
            dynamic_gpu_infos = {}
            for gpu in gpus:
                gpu_id = gpu["index"]
                gpu_used = gpu["memory.used"]
                gpu_total = gpu["memory.total"]
                gpu_free = gpu_total - gpu_used
                temperature = gpu["temperature.gpu"]
                command = ""
                for idx, process in enumerate(gpu["processes"]):
                    command += \
                 f"""
<button class="btn d-inline-flex align-items-center rounded" data-bs-toggle="collapse" data-bs-target="#collapseExample{idx}" aria-expanded="true" aria-current="true">
{process["command"]}
</button>
<div class="collapse show" id="collapseExample{idx}" style="">
  <ul class="list-unstyled fw-normal pb-1 small">
      <li>{" ".join(process["full_command"])}</li>
  </ul>
</div>
"""

                dynamic_gpu_infos[str(gpu_id)] = {
                    # "load": {
                    #     "percent": gpu.memoryUtil * 100,
                    #     "raw": gpu.load,
                    # },
                    # "used": {
                    #     "percent": gpu.memoryUsed / gpu.memoryTotal * 100,
                    #     "raw": gpu.memoryUsed
                    # },
                    "free": {
                        "percent": gpu_free / gpu_total * 100,
                        "raw": gpu_free
                    },
                    "temperature": {
                        "raw": temperature
                    },
                    "command": command
                }
        except:
            dynamic_gpu_infos = {}

        return {
            "dynamic": dynamic_gpu_infos,
            "static": self.gpu_infos
        }

    def get_docker_container_info(self) -> dict:
        try:
            docker_containers = self.docker_client.containers.list()
        except:
            return {
                "dynamic": {},
                "static": self.docker_container_infos
            }
        dynamic_docker_container_infos = {}
        for docker_container in docker_containers:
            container_info = {
                "name": docker_container.name,
                "image_tag": docker_container.image.tags,
                # "image_label": docker_container.image.labels,
                "status": docker_container.status,
                "mounts": docker_container.attrs['Mounts'],
                "state": docker_container.attrs['State'],
            }

            try:
                stats = docker_container.stats(stream=False, one_shot=True)
                container_info.update({
                    "pids": stats['pids_stats']['current'],
                    "mem_usage": stats['memory_stats']['usage'],
                    "mem_limit": stats['memory_stats']['limit'],
                    "mem_percent": stats['memory_stats']['usage'] / stats['memory_stats']['limit'] * 100,

                    "rx_bytes": stats['networks']['eth0']['rx_bytes'],
                    "tx_bytes": stats['networks']['eth0']['tx_bytes'],

                    "read_bytes": stats['blkio_stats']['io_service_bytes_recursive'][0]['value'],
                    "write_bytes": stats['blkio_stats']['io_service_bytes_recursive'][1]['value'],

                    "cpu_usage": stats['cpu_stats']['cpu_usage']['total_usage'] / stats['cpu_stats'][
                        'system_cpu_usage'] * 100,
                    # "stats": docker_container.stats(stream=False, one_shot=True),
                })
            except:
                pass

            dynamic_docker_container_infos[docker_container.id] = container_info

        return {
            "dynamic": dynamic_docker_container_infos,
            "static": self.docker_container_infos
        }

    def get_docker_image_info(self) -> dict:
        try:
            docker_images = self.docker_client.images.list()
            dynamic_docker_image_infos = {}
            for docker_image in docker_images:
                dynamic_docker_image_infos[docker_image.id] = {
                    "id": docker_image.id,
                    "tags": docker_image.tags,
                    "short_id": docker_image.short_id,
                    # "labels": docker_image.labels,
                }
        except:
            dynamic_docker_image_infos = {}

        return {
            "dynamic": dynamic_docker_image_infos,
            "static": self.docker_image_infos
        }

    def update(self):
        self.cpu = self.get_cpu_info()
        self.memory = self.get_memory_info()
        self.disks = self.get_disk_info()
        self.gpus = self.get_gpu_info()
        self.docker_containers = self.get_docker_container_info()
        self.docker_images = self.get_docker_image_info()

        self.last_update = time.time()

    def get_all_info(self):
        # timezone from UTC+0 to Asia/seoul
        last_update = datetime.datetime.fromtimestamp(
            self.last_update, tz=datetime.timezone(datetime.timedelta(hours=9))
        )

        return {
            "last_update": last_update.strftime('%Y-%m-%d %H:%M:%S %Z'),
            "cpu": self.cpu,
            "memory": self.memory,
            "disks": self.disks,
            "gpus": self.gpus,
            "docker_containers": self.docker_containers,
            "docker_images": self.docker_images
        }
