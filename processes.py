import subprocess

last_bg_pid = None


def run_background(cmd):
	global last_bg_pid

	process = subprocess.Popen(cmd)
	last_bg_pid = process.pid

	print(f"[Background PID {process.pid}]")

	return process.pid
