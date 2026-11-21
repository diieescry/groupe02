import os
import sys
import shlex
import signal
import readline
from contextlib import redirect_stdout
from parser import parse_command

# Historique
history = []
# Auto-completion
def completer(text, state):
    commands = [
        "go", "quit", "path", "say", "info",
        "past", "osinfo", "list", "show",
        "copy", "move", "del", "newdir", "newfile"
    ]

    options = [cmd for cmd in commands if cmd.startswith(text)]

    if state < len(options):
        return options[state]

    return None


readline.set_completer(completer)
readline.parse_and_bind("tab: complete")

# Informations du projet
def osinfo():
    print("Systèmes d'Exploitation -- UIR/ESIN")


# Aide
def info():
    print("""
========== OPSH HELP ==========

go       : Changer de dossier
path     : Afficher le chemin
say      : Afficher un message
list     : Afficher les fichiers
show     : Lire un fichier
copy     : Copier un fichier
move     : Deplacer un fichier
del      : Supprimer un fichier
newdir   : Creer un dossier
newfile  : Creer un fichier
past     : Afficher l'historique
osinfo   : Informations du projet
quit     : Quitter OPSH

===============================
""")


# Commandes internes
def builtin(args):

    command = args[0]

    if command == "quit":
        print("Fermeture de OPSH...")
        return True

    elif command == "go":

        destination = args[1] if len(args) > 1 else "~"
        destination = os.path.expanduser(destination)

        try:
            os.chdir(destination)
        except OSError as error:
            print("Erreur :", error)

    elif command == "path":
        print(os.getcwd())

    elif command == "say":
        print(" ".join(args[1:]))

    elif command == "info":
        info()

    elif command == "past":
        for number, item in enumerate(history, start=1):
            print(number, item)

    elif command == "osinfo":
        osinfo()

    else:
        return False

    return True


# Alias
aliases = {
    "list": "ls",
    "show": "cat",
    "copy": "cp",
    "move": "mv",
    "del": "rm",
    "newdir": "mkdir",
    "newfile": "touch"
}


# Analyse des redirections
def parse_redirections(args):

    command = []
    input_file = None
    output_file = None
    append = False

    i = 0

    while i < len(args):

        if args[i] in ("<", ">", ">>"):

            operator = args[i]

            if i + 1 >= len(args):
                raise ValueError("Nom du fichier manquant")

            filename = args[i + 1]

            if operator == "<":
                input_file = filename

            elif operator == ">":
                output_file = filename
                append = False

            elif operator == ">>":
                output_file = filename
                append = True

            i += 2

        else:
            command.append(args[i])
            i += 1

    if not command:
        raise ValueError("Commande manquante")

    return command, input_file, output_file, append


# Execution des commandes externes
def execute(args, input_file=None,
            output_file=None, append=False, background=False):

    args = args.copy()
    args[0] = aliases.get(args[0], args[0])

    pid = os.fork()

    if pid == 0:

        try:

            # Redirection d'entree <
            if input_file:

                fd = os.open(input_file, os.O_RDONLY)
                os.dup2(fd, 0)
                os.close(fd)

            # Redirection de sortie > ou >>
            if output_file:

                flags = os.O_WRONLY | os.O_CREAT

                if append:
                    flags |= os.O_APPEND
                else:
                    flags |= os.O_TRUNC

                fd = os.open(output_file, flags, 0o666)

                os.dup2(fd, 1)
                os.close(fd)

            os.execvp(args[0], args)

        except Exception as error:
            print("Erreur :", error, file=sys.stderr)
            os._exit(1)

        else:
            if background:
                print(f"[Background] PID: {pid}", flush=True)
            else:
                os.waitpid(pid, 0)


# Programme principal
# Execution des pipes entre deux processus
def execute_pipe(left_args, right_args):

    # Verification des commandes
    if not left_args or not right_args:
        print("Erreur : commande manquante dans le pipe")
        return

    # Traduction des alias
    left_args = left_args.copy()
    right_args = right_args.copy()

    left_args[0] = aliases.get(left_args[0], left_args[0])
    right_args[0] = aliases.get(right_args[0], right_args[0])

    # Creation du pipe
    read_fd, write_fd = os.pipe()

    # Premier processus
    left_pid = os.fork()

    if left_pid == 0:

        try:
            # Sortie du premier processus vers le pipe
            os.dup2(write_fd, 1)

            os.close(read_fd)
            os.close(write_fd)

            os.execvp(left_args[0], left_args)

        except Exception as error:
            os.write(2, f"Erreur : {error}\n".encode())
            os._exit(127)

    # Deuxieme processus
    right_pid = os.fork()

    if right_pid == 0:

        try:
            # Entree du deuxieme processus depuis le pipe
            os.dup2(read_fd, 0)

            os.close(read_fd)
            os.close(write_fd)

            os.execvp(right_args[0], right_args)

        except Exception as error:
            os.write(2, f"Erreur : {error}\n".encode())
            os._exit(127)

    # Processus parent
    os.close(read_fd)
    os.close(write_fd)

    os.waitpid(left_pid, 0)
    os.waitpid(right_pid, 0)
# Programme principal
def main():
        # Gestion des signaux

    def handle_sigint(signum, frame):
        raise KeyboardInterrupt

    def handle_sigchld(signum, frame):
        while True:
            try:
                pid, status = os.waitpid(-1, os.WNOHANG)
                if pid == 0:
                    break
            except ChildProcessError:
                break

    signal.signal(signal.SIGINT, handle_sigint)
    signal.signal(signal.SIGCHLD, handle_sigchld)
    print("================================")
    print("       OPSH - MINI SHELL")
    print("       UIR / ESIN")
    print("================================")

    while True:

        try:

            command = input("opsh> ")

            if not command.strip():
                continue
            args = parse_command(command)

            
            history.append(command)
                      # Gestion des pipes ->
            if "->" in args:
                pipe_index = args.index("->")

                left_args = args[:pipe_index]
                right_args = args[pipe_index + 1:]

                if not left_args or not right_args:
                    print("Erreur : commande manquante dans le pipe")
                    continue

                if "->" in right_args:
                    print("Erreur : un seul pipe est autorise")
                    continue

                execute_pipe(left_args, right_args)
                continue
            # Analyse des redirections
            try:
                args, input_file, output_file, append = (
                    parse_redirections(args)
                )

            except ValueError as error:
                print("Erreur :", error)
                continue

            # Commandes internes
            if args[0] in (
                "quit", "go", "path", "say",
                "info", "past", "osinfo"
            ):

                if input_file:
                    print("Redirection d'entree non disponible pour ce builtin")
                    continue

                if output_file:

                    mode = "a" if append else "w"

                    with open(output_file, mode) as file:
                        with redirect_stdout(file):
                            result = builtin(args)

                else:
                    result = builtin(args)

                if args[0] == "quit":
                    break

                continue

            # Commandes externes
            # Gestion du background &
            background = False

            if args and args[-1] == "&":
                args = args[:-1]
                background = True

            # Commandes externes
            execute(
                args,
                input_file,
                output_file,
                append,
                background=background
            )

        except KeyboardInterrupt:
            print("\nUtilisez quit pour quitter OPSH")

        except EOFError:
            print("\nFermeture de OPSH...")
            break

        except Exception as error:
            print("Erreur :", error)


if __name__ == "__main__":
    main()