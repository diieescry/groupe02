import os
import shlex

def parse_command(command):
    """
    Analyse la commande entrée par l'utilisateur.
    """
    command = os.path.expandvars(command)
    args = shlex.split(command)
    return args