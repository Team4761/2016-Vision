import threading

def thread1():
	while True:
		print("Thread1")


def thread2():
	while True:
		print("Thread2")

if __name__ == "__main__":
	t1 = threading.Thread(target=thread1)
	t2 = threading.Thread(target=thread2)
	t1.daemon = True
	t2.daemon = True
	t1.start()
	t2.start()
	while True:
		pass
