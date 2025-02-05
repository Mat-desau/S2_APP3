import numpy as np
import matplotlib.pyplot as plt

#Code en C en python
N = 4
LIGNES = 6

def ValideResultat(reponseTrouvee, reponseAttendu):
    for i in range(N):
        if reponseTrouvee[i] != reponseAttendu[i]:
            return False
    return True

def CalculBoucle(meterique, etat_initiale, etat_final):
    for i in range(N):
        etat_final[i] = 250
        for j in range(N):
            temp = meterique[i*N+j] + etat_initiale[j]
            if temp < etat_final[i]:
                etat_final[i] = temp

ref_meterique = [4, 3, 3, 2, 0, 3, 5, 4, 4, 3, 3, 2, 2, 5, 3, 2, 3, 4, 2, 3, 5, 2, 2, 3, 3, 4, 2, 3, 3, 0, 4, 5, 4, 5, 3, 0, 2, 3, 3, 4, 2, 3, 5, 2, 2, 3, 3, 4, 2, 5, 3, 2, 4, 3, 3, 2, 0, 3, 5, 4, 4, 3, 3, 2, 3, 2, 4, 3, 5, 4, 0, 3, 3, 2, 4, 3, 3, 2, 2, 5, 3, 4, 2, 3, 3, 0, 4, 5, 3, 4, 2, 3, 5, 2, 2, 3]

resultat_attendu = [2, 0, 2, 2, 4, 2, 4, 0, 0, 4, 2, 4, 2, 4, 0, 4, 4, 0, 4, 2, 4, 0, 4, 2]

erreurTrouvee = False
etat_actuel = np.zeros(N)
etat_nouveau = np.zeros_like(etat_actuel)

for z in range(0, LIGNES):
    CalculBoucle(ref_meterique[z*N*N:], etat_actuel, etat_nouveau)

    print(etat_nouveau)

    if ValideResultat(etat_nouveau, resultat_attendu[z*N:]) == False:
        erreurTrouvee = True

    etat_actuel = np.copy(etat_nouveau)

    if erreurTrouvee:
        print("Il a un ereur dan le calcul")
    else:
        print("Le calcul s'execute correctement")


#MAX = 60

#histogramme = np.zeros(MAX, dtype=int)
#valeurs = [[45, 14, 14, 2, 2, 45, 2, 15], [2, 37, 22, 22, 22, 2, 22, 15]]

#for i in range(0, 2):
#    for x in range(0, 8):
#        temp = int(valeurs[i][x])
#        histogramme[temp] += 1

#print(histogramme)