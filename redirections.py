import sys


def redirect_output(output_file, append=False):
    """Rediriger la sortie standard vers un fichier."""

    try:
        mode = "a" if append else "w"
        return open(output_file, mode, encoding="utf-8")

    except PermissionError:
        print("Erreur : accès refusé")
        return None

    except OSError as e:
        print(f"Erreur lors de l'ouverture du fichier : {e}")
        return None 

    # Tests des redirections
if __name__ == "__main__":

    print("===== TEST REDIRECTION > =====")

    fichier = redirect_output("resultat.txt", append=False)

    if fichier:
        fichier.write("Bonjour, test de la redirection !\n")
        fichier.close()
        print("Redirection > réussie")

    print("\n===== TEST REDIRECTION >> =====")

    fichier = redirect_output("resultat.txt", append=True)

    if fichier:
        fichier.write("Deuxième ligne ajoutée !\n")
        fichier.close()
        print("Redirection >> réussie")
        
    