import subprocess


def execute_pipe(left_cmd, right_cmd):
	p1 = subprocess.Popen(
		left_cmd,
		stdout=subprocess.PIPE,
		text=True
	)

	p2 = subprocess.Popen(
		right_cmd,
		stdin=p1.stdout,
		text=True
	)

	p1.stdout.close()
	p2.communicate()
