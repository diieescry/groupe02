
import os
import shutil
from pathlib import Path


# Commande LIST : afficher les fichiers et dossiers
def cmd_list(args):
    """Afficher les fichiers et dossiers du répertoire courant."""

    path = Path(args[0]) if args else Path.cwd()

    try:
        for item in sorted(path.iterdir()):
            print(item.name)

    except FileNotFoundError:
        print("Erreur : dossier introuvable")

    except NotADirectoryError:
        print("Erreur : le chemin indiqué n'est pas un dossier")

    except PermissionError:
        print("Erreur : accès refusé")


# Commande SHOW : afficher le contenu d'un fichier
def cmd_show(args):
    """Afficher le contenu d'un fichier."""

    if not args:
        print("Erreur : veuillez préciser un fichier")
        return

    try:
        with open(args[0], "r", encoding="utf-8") as file:
            print(file.read(), end="")

    except FileNotFoundError:
        print("Erreur : fichier introuvable")

    except PermissionError:
        print("Erreur : accès refusé")

    except IsADirectoryError:
        print("Erreur : le chemin indiqué est un dossier")

        # Commande COPY : copier un fichier
def cmd_copy(args):
    """Copier un fichier vers une destination."""

    if len(args) < 2:
        print("Erreur : utilisation : copy source destination")
        return

    source = args[0]
    destination = args[1]

    try:
        shutil.copy2(source, destination)
        print("Fichier copié avec succès")

    except FileNotFoundError:
        print("Erreur : fichier source introuvable")

    except PermissionError:
        print("Erreur : accès refusé")

    except IsADirectoryError:
        print("Erreur : le chemin source est un dossier")


# Commande MOVE : déplacer ou renommer un fichier
def cmd_move(args):
    """Déplacer ou renommer un fichier."""

    if len(args) < 2:
        print("Erreur : utilisation : move source destination")
        return

    source = args[0]
    destination = args[1]

    try:
        shutil.move(source, destination)
        print("Fichier déplacé avec succès")

    except FileNotFoundError:
        print("Erreur : fichier source introuvable")

    except PermissionError:
        print("Erreur : accès refusé")

        # Commande DEL : supprimer un fichier
def cmd_del(args):
    """Supprimer un fichier."""

    if not args:
        print("Erreur : veuillez préciser un fichier")
        return

    try:
        os.remove(args[0])
        print("Fichier supprimé avec succès")

    except FileNotFoundError:
        print("Erreur : fichier introuvable")

    except PermissionError:
        print("Erreur : accès refusé")

    except IsADirectoryError:
        print("Erreur : utilisez un dossier, pas un fichier")

# Commande NEWDIR : créer un dossier
def cmd_newdir(args):
    """Créer un nouveau dossier."""

    if not args:
        print("Erreur : veuillez préciser le nom du dossier")
        return

    try:
        os.mkdir(args[0])
        print("Dossier créé avec succès")

    except FileExistsError:
        print("Erreur : ce dossier existe déjà")

    except PermissionError:
        print("Erreur : accès refusé")

# Commande NEWFILE : créer un fichier vide
def cmd_newfile(args):
    """Créer un nouveau fichier."""

    if not args:
        print("Erreur : veuillez préciser le nom du fichier")
        return

    try:
        with open(args[0], "x", encoding="utf-8"):
            pass

        print("Fichier créé avec succès")

    except FileExistsError:
        print("Erreur : ce fichier existe déjà")

    except PermissionError:
        print("Erreur : accès refusé")

## Test des commandes
if __name__ == "__main__":

    print("===== TEST LIST =====")
    cmd_list([])

    print("\n===== TEST SHOW =====")
    cmd_show(["test.txt"])

    print("\n===== TEST COPY =====")
    cmd_copy(["test.txt", "copie.txt"])

    print("\n===== TEST MOVE =====")
    cmd_move(["copie.txt", "deplace.txt"])

    print("\n===== TEST DEL =====")
    cmd_del(["deplace.txt"]) 
    print("\n===== TEST NEWDIR =====")
    cmd_newdir(["mon_dossier"])
    print("\n===== TEST NEWFILE =====")
    cmd_newfile(["nouveau.txt"])
