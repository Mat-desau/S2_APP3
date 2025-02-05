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


"""
Fonction TrouverLimites
"""
def TrouverLimites(histogramme, seuil):
    pass  # Ne fait rien, permet au code initial d'exécuter sans erreurs. On peut laisser ici.
    # 7a- Mettre à 0 toutes les valeurs sous le seuil
    for x in range(0, len(histogramme)):
        if(histogramme[x] < seuil):histogramme[x] = 0

    # 7b- appliquer la fonction IdentifierTransitions. 
    Transitions = IdentifierTransitions(histogramme)

    # 7c- Trouver les 3 transitions sans utiliser numpy, c-a-d avec for/if/while/etc.
    Vallee = None
    LimiteGauche = None
    LimiteDroite = None

    nbrBins = len(histogramme)
    for x in range(0, nbrBins - 3):
        if (LimiteGauche == None and Transitions[x] == 1):
            LimiteGauche = x + 1

        if (LimiteGauche != None and Transitions[x] == 1):
            LimiteDroite = x + 1

        if (Transitions[x] == 2):
            Vallee = x + 1

    # 7d retourner les 3 valeurs
    return LimiteGauche, LimiteDroite, Vallee


# début du code.
def main():

    # 2 Lire les données
    # DonnerPrimaires = ???
    DonnerPrimaires = np.genfromtxt("S2GE_APP3_Examen_Formatif_Donnees_V2.csv", comments='#', delimiter=",").astype(int)

    # 3 Définir les classes pour les histogrammes
    binsAmpl = range(0, 257, 2)

    # 4 Créer et afficher l'histogramme du paramètre P. 
    #   Annoter le graphique; axes et titre.
    fig, ax = plt.subplots()
    SpectreVitesse, _, _ = ax.hist(DonnerPrimaires[:, 1], bins=binsAmpl)
    ax.set_title("Histogramme du paramètre P")
    ax.set_xlabel("Densité relative")
    ax.set_ylabel("Nombre de détections")

    # 5 récupérer les valeurs d'amplitude
    # Fait en 4 avec ax.hist (astuce)
    # méthode par Numpy (commentée)
    # SpectreVitesse, _ = np.histogram(DataMaster[:, 1], bins=binsAmpl)
    # ax.plot(binsAmpl[0:-1], SpectreVitesse)

    # 6 Trouver max et diviser toutes les hauteurs de l'histogramme par le max (Normaliser)
    SpectreVitesseNormalise = SpectreVitesse / np.max(SpectreVitesse)

    # 8 Appliquer la fonction TrouverLimites
    # TrouverLimites(DonnéesNormalisees, 0.2)
    LimiteGauche, LimiteDroite, Vallee = TrouverLimites(SpectreVitesseNormalise, 0.2)

    # 9 Ajouter lignes verticales
    ax.vlines(binsAmpl[LimiteGauche], 0, np.max(SpectreVitesse))
    ax.vlines(binsAmpl[LimiteDroite], 0, np.max(SpectreVitesse))
    ax.vlines(binsAmpl[Vallee], 0, np.max(SpectreVitesse))

    print(binsAmpl[Vallee], binsAmpl[LimiteDroite], binsAmpl[LimiteGauche] )

    # 10- Ajouter argparse et affichage/sauvegarde des fichiers
    parser = argparse.ArgumentParser(description='Description du programme python')
    parser.add_argument('--nombreoption', type=int, default=0, help='0 pour affichage, autre pour png')
    args = parser.parse_args()
    if(args.nombreoption != 0):
        fig.savefig("CIP_histoParamP.png")
    else:
        plt.show() # testé avec "--nombreoption 100"




main()
