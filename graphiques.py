from tkinter import *

bleu = '#159CDA'
blanc = '#DDF4FF'
rouge = '#FF5454'


cases = [[[(k, i), (k + 25, i), (k, i + 25), (k + 25, i + 25)] for k in range(0, 250, 25)] for i in range(0, 250, 25)]

appartenance_bateau_j1 = [[False for i in range(10)] for k in range(10)]
appartenance_bateau_j2 = [[False for i in range(10)] for k in range(10)]

class Bateau:
    def __init__(self, longueur, liste_cases, joueur):
        self.longueur = longueur
        self.liste_cases = liste_cases
        self.coule = False
        self.joueur = joueur


    
    def placer_bateau(self):
        pass


#verification qu'une case choisie est valide 
def Valide(bateau, case_choisie, appartenance_bateau):
    cases_a_cote = [[1, 0], [-1,0], [0, -1], [0, 1]]
    valide = False
    for case in cases_a_cote:
        if [case_choisie[0] + case[0], case_choisie[1] + case[1]] in bateau.liste_cases:
            valide = True
        if  (case_choisie[0] + case[0], case_choisie[1] + case[1]) in appartenance_bateau:
            valide = False

    if valide:
        bateau.liste_cases.append(case_choisie)

#action de tirer sur une case, comprend le cas où un bateau est touché et quand aucun n'est touché
def Tir(event, appartenance_bateau): 

    a, b, x1, y1, x2, y2 = IdentificationCase(event)

    if appartenance_bateau[a][b]:
        Case(x1, y1, x2, y2, aire_jeu1)
    else:
        Croix(x1, y1, x2, y2, aire_jeu1)
    
def Croix(x1, y1, x2, y2, aire_jeu):
    aire_jeu.create_line(x1, y1, x2, y2)
    aire_jeu.create_line(x1, y2, x2, y1)


def Grille(aire_jeu): #création de la grille de base
    for colonne in range(1, 10):
        aire_jeu.create_line(25 * colonne, 0, 25 * colonne, 250, fill = blanc)
        aire_jeu.create_line(0, 25 * colonne, 250, 25 * colonne, fill = blanc)

def Case(x1, y1, x2, y2, aire_jeu):
    aire_jeu.create_rectangle(x1, y1, x2, y2, fill = rouge,outline= blanc)

def IdentificationCase(event):
    clic = (event.x,event.y)
    coord = 0
    a = 0
    b = 0
    while coord == 0:
        if clic[1] > cases[a][b][-1][-1]:
            a += 1
        if clic[0] > cases[a][b][-1][0]:
            b += 1
        else:
            if clic[1] <= cases[a][b][-1][-1]:
                coord = [cases[a][b][0], cases[a][b][-1]]

    x1, y1, x2, y2 = coord[0][0], coord[0][1], coord[1][0], coord[1][1]

    return a, b, x1, y1, x2, y2

appartenance_bateau_j1[2][3] = True
appartenance_bateau_j1[9][9] = True


fen = Tk()

aire_jeu1 = Canvas(fen, width = 249, height = 249, bg = bleu)
aire_jeu1.pack(side = LEFT, padx = 10, pady = 10)
aire_jeu2 = Canvas(fen, width = 249, height = 249, bg = bleu)
aire_jeu2.pack(side = RIGHT, padx = 10, pady = 10)
Grille(aire_jeu1)
Grille(aire_jeu2)
aire_jeu1.bind("<Button-1>", lambda event : Tir(event, appartenance_bateau_j1))

fen.mainloop()
