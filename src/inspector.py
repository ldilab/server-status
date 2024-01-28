import time

import docker
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
        try:
            disks = self.system_client.disk_partitions()
            for disk in disks:
                self.disk_infos[disk.mountpoint] = {
                    "device": disk.device,
                    "mount": disk.mountpoint,
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
                "used": {
                    "percent": round(mem.used / mem.total * 100, 2),
                    "raw": mem.used
                },
                "available": {
                    "percent": round(mem.available / mem.total * 100, 2),
                    "raw": mem.available
                },
                "free": {
                    "percent": round(mem.free / mem.total * 100, 2),
                    "raw": mem.free
                },
            }
        except:
            dynamic_memory_infos = {}

        return {
            "dynamic": dynamic_memory_infos,
            "static": self.memory_infos
        }

    def get_disk_info(self) -> dict:
        try:
            disks = self.system_client.disk_partitions()
            dynamic_disk_infos = {}
            for disk in disks:
                dynamic_disk_infos[disk.mountpoint] = {
                    "used": {
                        "percent": self.system_client.disk_usage(disk.mountpoint).percent,
                        "raw": self.system_client.disk_usage(disk.mountpoint).used
                    },
                    "free": {
                        "percent": self.system_client.disk_usage(disk.mountpoint).free,
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
            gpus = self.gpu_client.getGPUs()
            dynamic_gpu_infos = {}
            for gpu in gpus:
                dynamic_gpu_infos[gpu.id] = {
                    "load": {
                        "percent": gpu.memoryUtil * 100,
                        "raw": gpu.load,
                    },
                    "used": {
                        "percent": gpu.memoryUsed / gpu.memoryTotal * 100,
                        "raw": gpu.memoryUsed
                    },
                    "free": {
                        "percent": gpu.memoryFree / gpu.memoryTotal * 100,
                        "raw": gpu.memoryFree
                    },
                    "temperature": {
                        "raw": gpu.temperature
                    }
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
            dynamic_docker_container_infos = {}
            for docker_container in docker_containers:
                dynamic_docker_container_infos[docker_container.id] = {
                    "name": docker_container.name,
                    "image_tag": docker_container.image.tags,
                    "image_label": docker_container.image.labels,
                    "status": docker_container.status,
                    "mounts": docker_container.attrs['Mounts'],
                    "state": docker_container.attrs['State'],
                }
        except:
            dynamic_docker_container_infos = {}

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
                    "labels": docker_image.labels,
                    "attrs": docker_image.attrs
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
        return {
            "last_update": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(self.last_update)),
            "cpu": self.cpu,
            "memory": self.memory,
            "disks": self.disks,
            "gpus": self.gpus,
            "docker_containers": self.docker_containers,
            "docker_images": self.docker_images
        }
