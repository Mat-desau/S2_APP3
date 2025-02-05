import numpy as np
import matplotlib.pyplot as plt
import argparse

"""
 pris de https://stackoverflow.com/questions/4624970/finding-local-maxima-minima-with-numpy-in-a-1d-numpy-array
 En entrée, valeurs provenant de TrouverLimites
 En sortie, vecteur avec 2 valeurs de moins qu'en entrée. où
            *  1 sur la coupure subite entre 0 et une valeur
            *  1 sur la coupure subite entre une valeur et 0
            * -2 sur un maximum local
            *  2 sur un minimum local
            * ex: Pour une entrée    [0, 0, 0, 0, 4, 5, 6, 7,  8, 7, 6, 5, 6, 7, 8,  9, 8, 7, 6, 5, 4, 0, 0, 0, 0]
                  on aura une sortie [   0, 0, 1, 0, 0, 0, 0, -2, 0, 0, 2, 0, 0, 0, -2, 0, 0, 0, 0, 0, 1, 0, 0]
"""
def IdentifierTransitions(histogramme):
    return np.diff(np.sign(np.diff(histogramme)))  # the one liner

def TrouverLimites(histogramme, seuil):
    pass  # Ne fait rien, permet au code initial d'exécuter sans erreurs. On peut laisser ici.
    # 7a- Mettre à 0 toutes les valeurs sous le seuil
    for i in range(0, len(histogramme)):
        if histogramme[i] < seuil:
            histogramme[i] = 0
    # 7b- appliquer la fonction IdentifierTransitions.
    Histo = IdentifierTransitions(histogramme)
    # 7c- Trouver les 3 transitions sans utiliser numpy, c-a-d avec for/if/while/etc.
    Monter = None
    Switch = None
    Descente = None
    for i in range(0, len(Histo)):
        if Monter == None:
            if Histo[i] == 1:
                Monter = i
        if Histo[i] == 2:
            Switch = i
        if Monter != None:
            if Histo[i] == 1:
                Descente = i

    # 7d retourner les 3 valeurs
    return (Monter, Switch, Descente)

# début du code.
def main():

    # 2 Lire les données
    DonnerPrimaires = np.genfromtxt("S2GE_APP3_Examen_Formatif_Donnees_v2.csv", delimiter=',')

    # 3 Définir les classes pour les histogrammes
    Index = DonnerPrimaires[:, 0]
    P = DonnerPrimaires[:, 1]
    Amplitude = DonnerPrimaires[:, 2]
    classe = 128

    Bin = np.linspace(0, 255, classe)

    # 4 Créer et afficher l'histogramme du paramètre P.
    plt.hist(P, bins=Bin, histtype='step', color='blue', label="Donnéees de P")

    #   Annoter le graphique; axes et titre.
    plt.xlabel("Numéro de détection")
    plt.ylabel("Valeur d'effectif")
    plt.title("Histogramme du paramètre P")

    # 5 récupérer les valeurs d'amplitude
    Amplitude2, Bins2 = np.histogram(P, bins=Bin)

    # 6 Trouver max et diviser toutes les hauteurs de l'histogramme par le max (Normaliser)
    HisotgrammeMax = max(Amplitude2)
    HistogrammeNorm = Amplitude2/HisotgrammeMax

    # 8 Appliquer la fonction TrouverLimites
    Monter, Switch, Descente = TrouverLimites(HistogrammeNorm, 0.2)

    # 9 Ajouter lignes verticales
    plt.vlines(Bin[Monter], 0, max(Amplitude2), colors='black')
    plt.vlines(Bin[Switch], 0, max(Amplitude2), colors='black')
    plt.vlines(Bin[Descente], 0, max(Amplitude2), colors='black')
    print(Bin[Monter], Bin[Switch], Bin[Descente])
    print(Monter, Switch, Descente)

    # 10- Ajouter argparse et affichage/sauvegarde des fichiers
    parser = argparse.ArgumentParser(description="Valeurs a entrer pour changer le code")
    parser.add_argument("--fichier", type=int, default=0, help="Entrer un valeur autre que 0 pour avoir un PNG")
    args = parser.parse_args()

    np.histogram()

    if args.fichier == 0:
        plt.show()
    else:
        plt.savefig("DESM1210_Maudit_code_de_marde.png")


main()
