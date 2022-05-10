from tkinter import *

bleu_fonce = '#22155C'
bleu_clair = '#159CDA'
blanc = '#DDF4FF'
rouge = '#FF5454'
taille_case = 50
taille_grille = taille_case * 10


cases = [[[(k, i), (k + taille_case, i), (k, i + taille_case), (k + taille_case, i + taille_case)] for k in range(0, taille_case, taille_case)] for i in range(0, taille_grille, taille_case)]

appartenance_bateau_j1 = [[False for i in range(10)] for k in range(10)]
appartenance_bateau_j2 = [[False for i in range(10)] for k in range(10)]

grille_tir_j1 = [[False for i in range(10)] for k in range(10)]
grille_tir_j2 = [[False for i in range(10)] for k in range(10)]

bateaux_j1 = [[] for i in range(5)]
bateaux_j2 = [[] for i in range(5)]

class Bateau:
    def __init__(self, longueur, liste_cases, joueur):
        self.longueur = longueur
        self.liste_cases = liste_cases
        self.coule = False
        self.joueur = joueur


    
    def placer_bateau(self):
        pass


def PlacerBateau(lon_bateau, appartenance_bateau, bateaux,aire_jeu_placer, bouton,fen):
    global COMPTEURCASESPLACEES
    COMPTEURCASESPLACEES = 0
    bouton.destroy()
    aire_jeu_placer.bind("<Button-1>", lambda event : PlacerCaseBateau(bateaux, event, appartenance_bateau, aire_jeu_placer, lon_bateau, fen))
    



def PlacerCaseBateau(bateaux, event, appartenance_bateau,aire_jeu_placer, lon_bateau, fen):
    global COMPTEURCASESPLACEES
    global COMPTEURBATEAU
    bateau = bateaux[COMPTEURBATEAU - 1]
    a, b, x1, y1, x2, y2 = IdentificationCase(event)

    if Valide(bateau, a, b, appartenance_bateau):
        appartenance_bateau[a][b] = True
        bateau.append((a,b))
        Case(x1, y1, x2, y2, aire_jeu_placer, bleu_fonce)
        COMPTEURCASESPLACEES += 1
    if COMPTEURCASESPLACEES == lon_bateau:
            
            
            COMPTEURBATEAU += 1
            aire_jeu_placer.unbind("<Button-1>")
            if COMPTEURBATEAU == 5:
                fen.destroy()

    


#verification qu'une case choisie est valide 
def Valide(bateau: list, a, b, appartenance_bateau):
    cases_voisines = [[a + 1, b], [a - 1, b], [a, b - 1], [a, b + 1]]
    valide = True 
    if not appartenance_bateau[a][b]:
        for case in cases_voisines:
            if case[0] >= 0 and case[0] <= 9 and case[1] >= 0 and case[1] <= 9: #vérification que la case voisine appartient à la grille
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
        aire_jeu.create_line(taille_case * colonne, 0, taille_case * colonne, taille_grille, fill = blanc)
        aire_jeu.create_line(0, taille_case * colonne, taille_grille, taille_case * colonne, fill = blanc)

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



def EtapePlacerBateaux(appartenance_bateau, bateaux):
    global COMPTEURBATEAU 
    COMPTEURBATEAU = 0
    fen = Tk()

    aire_jeu_placer = Canvas(fen, width = taille_grille, height = taille_grille, bg = bleu_clair)
    aire_jeu_placer.pack(side = LEFT, padx = 10, pady = 10)
    Grille(aire_jeu_placer)

    bateau2 = Button(text="Torpilleur (2 cases)", command= lambda: PlacerBateau(2, appartenance_bateau, bateaux, aire_jeu_placer, bateau2, fen))
    bateau3s = Button(text="Sous-marin (3 cases)", command= lambda: PlacerBateau(3, appartenance_bateau, bateaux,aire_jeu_placer, bateau3s, fen))
    bateau3c = Button(text="Contre-torpilleur (3 cases)", command= lambda: PlacerBateau(3, appartenance_bateau, bateaux,aire_jeu_placer, bateau3c, fen))
    bateau4 = Button(text="Croiseur (4 cases)", command= lambda: PlacerBateau(4, appartenance_bateau, bateaux,aire_jeu_placer, bateau4, fen))
    bateau5 = Button(text="Porte-avion (5 cases)", command= lambda: PlacerBateau(5, appartenance_bateau, bateaux,aire_jeu_placer, bateau5, fen))
    bateau2.pack()
    bateau3s.pack()
    bateau3c.pack()
    bateau4.pack()
    bateau5.pack()


    fen.mainloop()
    

EtapePlacerBateaux(appartenance_bateau_j1, bateaux_j1)
EtapePlacerBateaux(appartenance_bateau_j2, bateaux_j2)


fen = Tk()

aire_jeu1 = Canvas(fen, width=taille_grille, height=taille_grille, bg=bleu_clair)
aire_jeu1.pack(side=LEFT, padx=10, pady=10)
aire_jeu2 = Canvas(fen, width=taille_grille, height=taille_grille, bg=bleu_clair)
aire_jeu2.pack(side=RIGHT, padx=10, pady=10)
Grille(aire_jeu1)
Grille(aire_jeu2)
aire_jeu1.bind("<Button-1>", lambda event : Tir(event, appartenance_bateau_j1))

fen.mainloop()
