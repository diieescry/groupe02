import subprocess
import re

def command_substitution(text):

    matches = re.findall(r'\$\((.*?)\)', text)

    for cmd in matches:

        result = subprocess.check_output(
            cmd,
            shell=True,
            text=True
        ).strip()

        text = text.replace(
            f"$({cmd})",
            result
        )

    return text
