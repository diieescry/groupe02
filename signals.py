import signal
import os


def handle_sigint(signum, frame):
	print("\nCTRL+C détecté")


def handle_sigchld(signum, frame):
	try:
		while True:
			pid, status = os.waitpid(-1, os.WNOHANG)

			if pid == 0:
				break

	except ChildProcessError:
		pass


def setup_signals():
	signal.signal(signal.SIGINT, handle_sigint)
	signal.signal(signal.SIGCHLD, handle_sigchld)
