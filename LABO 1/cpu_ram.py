import psutil
import time


def cpu_ram():
    while True:
        # CODIGO: utilizando la libreria psutil, obtener %CPU y %RAM
        cpu = psutil.cpu_percent(interval=15)
        ram = psutil.virtual_memory()[2]
        print("CPU: %" + str(cpu) + "\tRAM: %" + str(ram))
        #time.sleep(1)


if __name__ == "__main__":
    cpu_ram()
