from random import randint
from time import sleep
from fei.ppds import Thread, print, Semaphore, Mutex

N = 3
M = 12

class SimpleBarrier(object):
	def __init__(self, N):
		self.N = N
		self.cnt = 0
		self.mutex = Mutex()
		self.barrier = Semaphore(0)


	def wait(self, each = None, last = None):
		self.mutex.lock()
		self.cnt += 1
		if each:
			print(each)
		if self.cnt == self.N:
			if last:
				print(last)
			self.cnt = 0
			self.barrier.signal(self.N)
		self.mutex.unlock()
		self.barrier.wait()



class Shared(object):
	def __init__(self, m):
		self.servings = m
		self.mutex = Mutex()
		self.empty_pot = Semaphore(0)
		self.full_pot = Semaphore(0)
		self.b1 = SimpleBarrier(N)
		self.b2 = SimpleBarrier(N)

def eat(i):
	print(f'savage {i} eat start')
	sleep(randint(50, 200) / 100)
	print(f'savage {i} eat end')


def savage(i, shared):
	sleep(randint(1, 100) / 100)
	while True:
		shared.b1.wait()
		shared.b2.wait(each = '', last = '')

		shared.mutex.lock()
		if shared.servings == 0:
			print(f'savage {i}: empty pot')
			shared.empty_pot.signal()
			shared.full_pot.wait()
		print(f'savage {i}: take from pot')
		shared.servings -= 1
		shared.mutex.unlock()
		eat(i)


def cook(shared):
	while True:
		shared.empty_pot.wait()
		print('cook: cooking')
		sleep(randint(50, 200) / 100)
		print(f'cook: {M} servings --> pot')
		shared.servings += M
		shared.full_pot.signal()


def main():
	shared = Shared(0)
	savages = []
	for i in range(N):
		savages.append(Thread(savage, i, shared))

	savages.append(Thread(cook, shared))

	for t in savages:
		t.join()



if __name__ == '__main__':
	main()
