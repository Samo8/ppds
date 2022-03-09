from cv2 import trace
from fei.ppds import Mutex, Thread, Semaphore, Event, print
from time import sleep
from random import randint


class LS(object):
	"""class representing Lightswitch object
	we have counter and simple mutex here"""

	def __init__(self):
		self.cnt = 0
		self.mutex = Mutex()
		
	def lock(self, sem):
		"""function used to lock.
		:param sem: Semaphore which wait() is called on
		:return: None
		"""
		self.mutex.lock()
		self.cnt += 1
		if self.cnt == 1:
			sem.wait()
		self.mutex.unlock()		
		return self.cnt

	def unlock(self, sem):
		"""function used to unlock.
		:param sem: Semaphore which signal() is called on
		:return: None
		"""
		self.mutex.lock()
		self.cnt -= 1
		if self.cnt == 0:
			sem.signal()
		self.mutex.unlock()


class Shared:
	def __init__(self):
		self.access_data = Semaphore(1)
		self.turniket = Semaphore(1)
		self.ls_monitor = LS()
		self.ls_sensor = LS()
		self.valid_data = Event()


def monitor(shared, monitor_id):
	while True:
		sleep(randint (40, 50) / 1000)
		
		shared.turniket.wait()
		number_of_reading_monitors = shared.ls_monitor.lock(shared.access_data)
		shared.turniket.signal()
		print(f'monitor{monitor_id}: number_of_reading_monitors: {number_of_reading_monitors}\n')
		shared.ls_monitor.unlock(shared.access_data)


def sensor(shared, sensor_id):
	while True:
		shared.turniket.wait()
		shared.turniket.signal()
		number_of_writing_sensors = shared.ls_sensor.lock(shared.access_data)
		sleep_time = randint (50, 60) / 1000
		sleep(sleep_time)

		if (sensor_id == 2):
			write_duration = randint(20, 25) / 1000
		else:
			write_duration = randint(10, 20) / 1000
		print(f'sensor {sensor_id}:  number_of_writing_sensors: {number_of_writing_sensors}, write_duration: {write_duration}\n')
		sleep(write_duration)
		shared.valid_data.signal()
		shared.ls_sensor.unlock(shared.access_data)
		
		
def main():
	shared = Shared()
	monitors = [Thread(monitor, shared, m) for m in range(8)]
	sensors = [Thread(sensor, shared, s) for s in range(3)]
	for thread in monitors + sensors: thread.join()
	

if __name__ == '__main__':
	main()
