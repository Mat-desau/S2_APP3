import numpy as np
import matplotlib.pyplot as plt
import argparse

#Création des paramètres
def Argument():
    argu = argparse.ArgumentParser(description='Argument pour choisir la destination du fichier (à lécran ou dans un fichier)')

    argu.add_argument('--fichier', action='store_true', help='Mettre condition pour mettre laction fausse')
    argu.add_argument('--temps_mort', action='store_true', help='Mettre condition pour mettre laction fausse')

    resultat = argu.parse_args()

    return resultat

def OranisationArgument(resultat):
    #Changer la valeur de fichier dépendament des arguments
    if (resultat.fichier):
        BOOL_fichier = True
    else:
        BOOL_fichier = False

    # Changer la valeur de temps morts dépendament des arguments
    if (resultat.temps_mort):
        BOOL_temps_mort = True
    else:
        BOOL_temps_mort = False

    return (BOOL_fichier, BOOL_temps_mort)

#Appel des variables pour les fichiers
def OuvertureFichier():
    #Ouverture des fichiers
    NOM_IN1 = "S2GE_APP3_Problematique_Detecteur_Primaire.csv"
    NOM_IN2 = "S2GE_APP3_Problematique_Detecteur_Secondaire.csv"
    IN1 = open(NOM_IN1, "r")
    IN2 = open(NOM_IN2, "r")

    return(IN1, IN2)

#Verification si fichier sont OK
def Verificationfonctionnement(IN1, IN2):
    #verification de l'ouverture correct des fichiers
    print("Fonctionnement de la lecture pour document 1 = ", IN1.readable())
    print("Fonctionnement de la lecture pour document 2 = ", IN2.readable())

#lectures des donnees dans les variables de donnees
def MiseEnDonnee(IN1, IN2):
    #Transfer des données des csv dans un tableau
    donnees1 = np.genfromtxt(IN1, delimiter=',')
    donnees2 = np.genfromtxt(IN2, delimiter=',')
    return (donnees1, donnees2)

#mettre les données de chaque lectures dans les variables respectifs
def MiseEnVariable(donnees1, donnees2):
    #Transfert des premières données dans leurs varibales respectifs
    index1 = donnees1[:, 0]
    temps1 = donnees1[:, 1]
    tension1 = donnees1[:, 2]
    temps_mort1 = donnees1[:, 3]
    temperature1 = donnees1[:, 4]

    # Transfert des deuxième données dans leurs varibales respectifs
    index2 = donnees2[:, 0]
    temps2 = donnees2[:, 1]
    tension2 = donnees2[:, 2]
    temps_mort2 = donnees2[:, 3]
    temperature2 = donnees2[:, 4]

    return(index1, index2, temps1, temps2, tension1, tension2, temps_mort1, temps_mort2, temperature1, temperature2)

#histogramme de départ
def HistogrammeDepart(hist_nombre, tension1, tension2):
    sub1_1 = plt.subplot(1, 1, 1)

    hist1_min = np.floor(min(tension1))
    hist1_max = np.ceil(max(tension1))

    bins1_1 = np.logspace(np.log10(hist1_min), np.log10(hist1_max), hist_nombre)
    sub1_1.hist(tension1, bins=bins1_1, histtype='step', color='blue', label="Tension primaire")

    hist2_min = np.floor(min(tension2))
    hist2_max = np.ceil(max(tension2))

    bins1_2 = np.logspace(np.log10(hist2_min), np.log10(hist2_max), hist_nombre)
    sub1_1.hist(tension2, bins=bins1_2, histtype='step', color='red', label="Tension secondaire")
    plt.step()

    sub1_1.set_xscale('log')
    sub1_1.set_xlabel("Amplitude (mV)")
    sub1_1.set_ylabel("Detection (Nombre)")
    sub1_1.set_title("Histogramme de l'amplitude des détections")
    sub1_1.legend()
    plt.figure()

#Histogramme avec les coincidence
def HistogrammeFinale(hist_nombre, tension1, tension1_bon, tension1_mauvais, temps1, temps_mort1, temps_mort1_bon, BOOL_fichier, BOOL_temps_mort):
    if(BOOL_temps_mort == False):
        sub1_1 = plt.subplot(1, 1, 1)

        # Creations des bins
        hist1_min = np.floor(min(tension1))
        hist1_max = np.ceil(max(tension1))
        bins1_1 = np.logspace(np.log10(hist1_min), np.log10(hist1_max), hist_nombre)
        bins1_2 = np.insert(bins1_1, 0, 0)

        #Creation des valeurs pour les steps
        paliers, bin_edges = np.histogram(tension1_bon, bins=bins1_2)
        paliers2, bin_edges2 = np.histogram(tension1_bon, bins=bins1_1)
        paliersfull, bin_edgesfull = np.histogram(tension1, bins=bins1_2)
        paliersmauvais, bin_edgesmauvais = np.histogram(tension1_mauvais, bins=bins1_2)

        paliers = paliers / max(temps1 / 1000)
        paliers2 = paliers2 / max(temps1 / 1000)
        paliersfull = paliersfull / max(temps1 / 1000)
        paliersmauvais = paliersmauvais / max(temps1 / 1000)

        #Calculs de valeurs pour les barres d'erreur
        bins1_1_center = 0.5 * (bin_edges2[1:] + bin_edges2[:-1])

        # Creation des graphiques
        sub1_1.step(bins1_1, paliersfull, color='black', label="Tous")
        sub1_1.step(bins1_1, paliers, color='red', label="Coincident")
        sub1_1.errorbar(bins1_1_center, paliers2, yerr=(paliers2*CalculErreur(tension1_bon)), color='r', ls='none', marker='.' )
        sub1_1.step(bins1_1, paliersmauvais, color='green', label="Non-Coincident")

        # Attributs des graphiques
        sub1_1.set_xscale('log')
        sub1_1.set_xlabel("Amplitude (mV)")
        sub1_1.set_ylabel("Taux de détection (S-1)")
        sub1_1.grid(color='grey', which='both', linewidth=0.2, axis='both')
        sub1_1.set_title("Histogramme de l'amplitude des détections")
        sub1_1.legend()
        impression(BOOL_fichier, BOOL_temps_mort)

    if(BOOL_temps_mort == True):
        sub1_1 = plt.subplot(1, 1, 1)

        hist1_min = np.floor(min(tension1))
        hist1_max = np.ceil(max(tension1))

        #Creations des bins
        bins1_1 = np.logspace(np.log10(hist1_min), np.log10(hist1_max), hist_nombre)
        bins1_2 = np.insert(bins1_1, 0, 0)

        #Creation des valeurs pour les step et les barres d'erreur (histogramme fait + 1 automatiquement donc ont doit rajouter avant)
        paliers, bin_edges = np.histogram(tension1_bon, bins=bins1_2)
        paliers2, bin_edges2 = np.histogram(tension1_bon, bins=bins1_1)
        paliersfull, bin_edgesfull = np.histogram(tension1, bins=bins1_2)
        paliersmauvais, bin_edgesmauvais = np.histogram(tension1_mauvais, bins=bins1_2)

        Nt = CorrigerTempsMort(temps1, temps_mort1, paliers)
        Na = CorrigerTempsMort(temps1, temps_mort1, paliers2)
        Npaliersfull = CorrigerTempsMort(temps1, temps_mort1, paliersfull)
        Npaliersmauvais = CorrigerTempsMort(temps1, temps_mort1, paliersmauvais)

        Npaliersfull = Npaliersfull/max(temps1/1000)
        Npaliersmauvais = Npaliersmauvais/max(temps1/1000)
        Nt = Nt/max(temps1/1000)
        Na = Na/max(temps1/1000)

        #Calculs de valeurs pour les barres d'erreur
        bins1_1_center = 0.5 * (bin_edges2[1:] + bin_edges2[:-1])

        #Creation des graphiques
        sub1_1.step(bins1_1, Npaliersfull, color='black', label="Tous")
        sub1_1.step(bins1_1, Nt, color='red', label="Coincident corriger")
        sub1_1.errorbar(bins1_1_center, Na, yerr=(Na * CalculErreur(tension1_bon)), color='r', ls='none', marker='.')
        sub1_1.step(bins1_1, Npaliersmauvais, color='green', label="Non-Coincident")

        #Attributs des graphiques
        sub1_1.set_xscale('log')
        sub1_1.set_xlabel("Amplitude (mV)")
        sub1_1.set_ylabel("Taux de détection (S-1)")
        sub1_1.grid(color='grey', which='both', linewidth=0.2, axis='both')
        sub1_1.set_title("Histogramme de l'amplitude des détections corriger")
        sub1_1.legend()
        impression(BOOL_fichier, BOOL_temps_mort)

#Correction du temps
def CorrigerTempsMort(temps1, temps_mort1, paliers):
    #Calcul du temps mort dans l'histogramme
    Ro = paliers / max(temps1)
    Rt = Ro / (1 - (Ro*(np.sum(temps_mort1)/len(temps_mort1))))
    Nt = Rt*max(temps1)

    return Nt

#Vérification que toute est OK
def Coincidence(donnees1, donnees2, index1, temps1, temps2, tension1, temps_mort1, temperature1, temps_difference, precision):
    temps_difference = float(temps_difference)
    indexBon = np.zeros_like(index1)

    #creation d'array vides pour les coincidents
    index1_bon = np.array([])
    tension1_bon = np.array([])
    temps_mort1_bon = np.array([])
    temps1_bon = np.array([])
    temperature1_bon = np.array([])

    # creation d'array vides pour les non-coincidents
    index1_mauvais = np.array([])
    tension1_mauvais = np.array([])
    temps_mort1_mauvais = np.array([])
    temps1_mauvais = np.array([])
    temperature1_mauvais = np.array([])

    lieu = 0
    #verification de la coincidence de chaque données
    for array1 in range(0, len(donnees1)):
        for array2 in range(lieu, len(donnees2)):
            if(array2 < len(donnees2)):
                valeur = temps1[array1] - temps2[array2]
                if(np.abs(valeur) <= (temps_difference*pow(10,-3))):
                    index1_bon = np.append(index1_bon, index1[array1])
                    temps1_bon = np.append(temps1_bon, temps1[array1])
                    tension1_bon = np.append(tension1_bon, tension1[array1])
                    temps_mort1_bon = np.append(temps_mort1_bon, temps_mort1[array1])
                    temperature1_bon = np.append(temperature1_bon, temperature1[array1])

                    indexBon[array1] = index1[array1]
                    lieu = array2
                    break
                elif(lieu+precision < array2):
                    indexBon[array1] = 0
                    break
            else:
                break

    #transfert des non-coincident dans les array de non-coincident
    for val in range(0, len(index1)):
        if(indexBon[val] == 0):
            index1_mauvais = np.append(index1_mauvais, index1[val])
            temps1_mauvais = np.append(temps1_mauvais, temps1[val])
            tension1_mauvais = np.append(tension1_mauvais, tension1[val])
            temps_mort1_mauvais = np.append(temps_mort1_mauvais, temps_mort1[val])
            temperature1_mauvais = np.append(temperature1_mauvais, temperature1[val])

    return(index1_bon, index1_mauvais, temps1_bon, temps1_mauvais, tension1_bon, tension1_mauvais, temps_mort1_bon, temps_mort1_mauvais, temperature1_bon, temperature1_mauvais)

#impression dans le fichier de resultat
def impression(BOOL_fichier, BOOL_temps_mort):
    #impression dans le fichier PNG
    if BOOL_fichier == True:
        #impression de temps mort
        if BOOL_temps_mort:
            plt.savefig("DESM1210-BOIF1302_Corrige.png")
        #impression d'histogramme sans corrections
        else:
            plt.savefig("DESM1210-BOIF1302.png")
    #impression à l'écran
    if BOOL_fichier == False:
        plt.show()

#Fermer les fichiers
def CloseFichier(IN1, IN2):
    #fermeture des fichiers
    IN1.close()
    IN2.close()

def CalculErreur(tension1_bon):
    #calcul des erreurs sur chaque données
    erreur = 1 / np.sqrt(len(tension1_bon))
    return erreur

#--------------------- MAIN ---------------------
def main():
    resultat = Argument()

    BOOL_fichier, BOOL_temps_mort = OranisationArgument(resultat)

    IN1, IN2 = OuvertureFichier()

    Verificationfonctionnement(IN1, IN2)

    donnees1, donnees2 = MiseEnDonnee(IN1, IN2)

    index1, index2, temps1, temps2, tension1, tension2, temps_mort1, temps_mort2, temperature1, temperature2 = MiseEnVariable(donnees1, donnees2)

    #HistogrammeDepart(1000, tension1, tension2)

    index1_bon, index1_mauvais, temps1_bon, temps1_mauvais, tension1_bon, tension1_mauvais,\
    temps_mort1_bon, temps_mort1_mauvais, temperature1_bon, temperature1_mauvais = Coincidence(donnees1, donnees2, index1, temps1, temps2, tension1, temps_mort1, temperature1, 10, 100)

    HistogrammeFinale(20, tension1, tension1_bon, tension1_mauvais, temps1, temps_mort1, temps_mort1_bon, BOOL_fichier, BOOL_temps_mort)

    CloseFichier(IN1, IN2)

main()

