# Variables management for OPSH
variables = {}

last_status = 0
last_pid = 0

def export_var(name, value):
    variables[name] = value


def get_var(name):
    return variables.get(name, "")


def expand_variables(text):
    global last_status
    global last_pid

    text = text.replace("$?", str(last_status))
    text = text.replace("$!", str(last_pid))

    for name, value in variables.items():
        text = text.replace(f"${name}", value)
        text = text.replace(f"${{{name}}}", value)

    return text