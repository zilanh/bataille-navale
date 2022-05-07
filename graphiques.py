from tkinter import *

bleu_fonce = '#22155C'
bleu_clair = '#159CDA'
blanc = '#DDF4FF'
rouge = '#FF5454'


cases = [[[(k, i), (k + 25, i), (k, i + 25), (k + 25, i + 25)] for k in range(0, 250, 25)] for i in range(0, 250, 25)]

appartenance_bateau_j1 = [[False for i in range(10)] for k in range(10)]
appartenance_bateau_j2 = [[False for i in range(10)] for k in range(10)]

bateaux_j1 = []
bateaux_j2 = []

class Bateau:
    def __init__(self, longueur, liste_cases, joueur):
        self.longueur = longueur
        self.liste_cases = liste_cases
        self.coule = False
        self.joueur = joueur


    
    def placer_bateau(self):
        pass


def PlacerBateau(lon_bateau, appartenance_bateau, bateaux,aire_jeu_placer, bouton):
    
    aire_jeu_placer.bind("<Button-1>", lambda event : PlacerCaseBateau(bateaux, event, appartenance_bateau, aire_jeu_placer, lon_bateau, bouton))
    



def PlacerCaseBateau(bateau, event, appartenance_bateau,aire_jeu_placer, lon_bateau, bouton):

    a, b, x1, y1, x2, y2 = IdentificationCase(event)
    if Valide(bateau, a, b, appartenance_bateau):
        appartenance_bateau[a][b] = True
        Case(x1, y1, x2, y2, aire_jeu_placer, bleu_fonce)
    


#verification qu'une case choisie est valide 
def Valide(bateau: list, a, b, appartenance_bateau):
    cases_voisines = [[a + 1, b], [a - 1, b], [a, b - 1], [a, b + 1]]
    valide = True 
    if not appartenance_bateau[a][b]:
        for case in cases_voisines:
            if case[0] >= 0 and case[0] <= 9 and case[1] >= 0 and case[0] <= 9: #vérification que la case voisine appartient à la grille
                if appartenance_bateau[case[0]][case[1]] and ((case[0], case[1]) not in bateau):
                    valide = False
    return valide
        
#action de tirer sur une case, comprend le cas où un bateau est touché et quand aucun n'est touché
def Tir(event, appartenance_bateau): 

    a, b, x1, y1, x2, y2 = IdentificationCase(event)

    if appartenance_bateau[a][b]:
        Case(x1, y1, x2, y2, aire_jeu1)
    else:
        Croix(x1, y1, x2, y2, aire_jeu1)

#trace une croix
def Croix(x1, y1, x2, y2, aire_jeu):
    aire_jeu.create_line(x1, y1, x2, y2)
    aire_jeu.create_line(x1, y2, x2, y1)

#crée la grille de base 
def Grille(aire_jeu): #création de la grille de base
    for colonne in range(1, 10):
        aire_jeu.create_line(25 * colonne, 0, 25 * colonne, 250, fill = blanc)
        aire_jeu.create_line(0, 25 * colonne, 250, 25 * colonne, fill = blanc)

#colorie une case
def Case(x1, y1, x2, y2, aire_jeu, couleur = rouge):
    aire_jeu.create_rectangle(x1, y1, x2, y2, fill=couleur, outline=blanc)

#renvoie la case sur laquelle on clique et ses coordonnées sur le canvas
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

def EtapePlacerBateaux(appartenance_bateau, bateaux):
    fen = Tk()

    aire_jeu_placer = Canvas(fen, width = 250, height = 250, bg = bleu_clair)
    aire_jeu_placer.pack(side = LEFT, padx = 10, pady = 10)
    Grille(aire_jeu_placer)

    bateau2 = Button(text="Torpilleur (2 cases)", command= lambda: PlacerBateau(2, appartenance_bateau, bateaux, aire_jeu_placer, bateau2))
    bateau3s = Button(text="Sous-marin (3 cases)", command= lambda: PlacerBateau(3, appartenance_bateau, bateaux,aire_jeu_placer, bateau3s))
    bateau3c = Button(text="Contre-torpilleur (3 cases)", command= lambda: PlacerBateau(3, appartenance_bateau, bateaux,aire_jeu_placer, bateau3c))
    bateau4 = Button(text="Croiseur (4 cases)", command= lambda: PlacerBateau(4, appartenance_bateau, bateaux,aire_jeu_placer, bateau4))
    bateau5 = Button(text="Porte-avion (5 cases)", command= lambda: PlacerBateau(5, appartenance_bateau, bateaux,aire_jeu_placer, bateau5))
    bateau2.pack()
    bateau3s.pack()
    bateau3c.pack()
    bateau4.pack()
    bateau5.pack()


    fen.mainloop()

EtapePlacerBateaux(appartenance_bateau_j1, bateaux_j1)
EtapePlacerBateaux(appartenance_bateau_j2, bateaux_j2)


fen = Tk()

aire_jeu1 = Canvas(fen, width=250, height=250, bg=bleu_clair)
aire_jeu1.pack(side=LEFT, padx=10, pady=10)
aire_jeu2 = Canvas(fen, width=250, height=250, bg=bleu_clair)
aire_jeu2.pack(side=RIGHT, padx=10, pady=10)
Grille(aire_jeu1)
Grille(aire_jeu2)
aire_jeu1.bind("<Button-1>", lambda event : Tir(event, appartenance_bateau_j1))

fen.mainloop()
