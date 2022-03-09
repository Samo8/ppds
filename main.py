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
		self.accessData = Semaphore(1)
		self.turniket = Semaphore(1)
		self.ls_monitor = LS()
		self.ls_cidlo = LS()
		self.validData = Event()


def monitor(shared, monitor_id):
	# monitor nemôže pracovať, kým nie je aspoň 1 platný údaj v úložisku
	# # shared.validData.wait()
	while True:
		# monitor má prestávku 500 ms od zapnutia alebo poslednej aktualizácie
		sleep(0.5)
		# zablokujeme turniket, aby sme vyhodili čidlá z KO
		shared.turniket.wait()
		# získame prístup k úložisku
		pocet_citajucich_monitorov = shared.ls_monitor.lock(shared.accessData)
		shared.turniket.signal()
		
		# prístup k údajom simulovaný nasledovným výpisom
		print(f'monit{monitor_id}: pocet_citajucich_monitorov: {pocet_citajucich_monitorov}\n')
		# aktualizovali sme údaje, odchádzame z úložiska
		shared.ls_monitor.unlock(shared.accessData)


def cidlo(shared, cidlo_id):
	while True:
		# čidlá prechádzajú cez turniket, pokým ho nezamkne monitor
		shared.turniket.wait()
		shared.turniket.signal()
		
		# získame prístup k úložisku
		pocet_zapisujucich_cidiel = shared.ls_cidlo.lock(shared.accessData)
		# prístup k údajom simulovaný čakaním v intervale 10 až 15 ms
		# podľa špecifikácie zadania informujeme o čidle a zápise, ktorý ide vykonať
		# trvanie_zapisu = rand(10 az 15 ms)
		trvanie_zapisu = randint(10, 15) / 1000
		print(f'cidlo {cidlo_id}:  pocet_zapisujucich_cidiel: {pocet_zapisujucich_cidiel}, trvanie_zapisu: {trvanie_zapisu}\n')
		sleep(trvanie_zapisu)
		# po zapísaní údajov signalizujeme, že údaj je platný
		shared.validData.signal()
		# a odchádzame z úložiska preč
		shared.ls_cidlo.unlock(shared.accessData)
		
		
def main():
	shared = Shared()
	monitors = [Thread(monitor, shared, m) for m in range(2)]
	sensors = [Thread(cidlo, shared, s) for s in range(10)]
	for thread in monitors + sensors: thread.join()
	

if __name__ == '__main__':
	main()
