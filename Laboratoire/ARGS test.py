import argparse
import sys

def CheckArgs(args = None):
    parse = argparse.ArgumentParser(description='Voici les paramètre à passer')

    parse.add_argument('-T', '--Texte', help='Entrer du texte en paramètre', type=str)

    parse.add_argument('-E', '--entier', help='Entrer un entier', default='10', type=int)

    parse.add_argument('-Z', '--etat', help='entrer vrai ou faux', action='store_True')

    parse.add_argument('-P', '--princ', help='Argument principale', default='OK', required=True, type=str)

    resultat = parse.parse_args(args)
    return( resultat.Texte, resultat.entier, resultat.etat, resultat.princ)

if __name__ == '__main__' :
    T,E,ETAT,P = CheckArgs(sys.argv[1:])
    print("T = ", T)
    print("E = ", E)
    print("Z = ", ETAT)
    print('P = ', P)

if ETAT == True:
    print("\n", T, "j'ai", E, "ans et", P)