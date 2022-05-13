from tkinter import *

bleu_fonce = '#22155C'
bleu_clair = '#159CDA'
blanc = '#DDF4FF'
rouge = '#FF5454'
taille_case = 50
taille_grille = taille_case * 10


cases = [[[(k, i), (k + taille_case, i), (k, i + taille_case), (k + taille_case, i + taille_case)] for k in range(0, taille_grille, taille_case)] for i in range(0, taille_grille, taille_case)]

#représentation des bateaux par True/False
appartenance_bateau_j1 = [[False for i in range(10)] for k in range(10)]
appartenance_bateau_j2 = [[False for i in range(10)] for k in range(10)]

#représentation des cases sur lesquelles chaque joueur a tiré par True/False
grille_tir_j1 = [[False for i in range(10)] for k in range(10)]
grille_tir_j2 = [[False for i in range(10)] for k in range(10)]

#tableau contenant les cases appartenant à chaque bateau
bateaux_j1 = [[] for i in range(5)]
bateaux_j2 = [[] for i in range(5)]

#variables pr déterminer le nombre de bateaux et le tour
"""
coule_j1 = 0
coule_j2 = 0
nbcasestotal = 17
"""

#fonction pour placer un bateau
def PlacerBateau(lon_bateau, appartenance_bateau, bateaux,aire_jeu_placer, bouton,fen):
    global COMPTEURCASESPLACEES
    COMPTEURCASESPLACEES = 0
    bateau = bateaux[COMPTEURBATEAU]
    bouton.destroy()
    aire_jeu_placer.bind("<Button-1>", lambda event : PlacerCaseBateau(bateau, event, appartenance_bateau, aire_jeu_placer, lon_bateau, fen))
    

#fonction pour placer une case d'un bateau
def PlacerCaseBateau(bateau, event, appartenance_bateau,aire_jeu_placer, lon_bateau, fen):
    global COMPTEURCASESPLACEES
    global COMPTEURBATEAU
    
    a, b, x1, y1, x2, y2 = IdentificationCase(event)

    if Valide(bateau, a, b, appartenance_bateau):
        appartenance_bateau[a][b] = True
        bateau.append((a,b))
        Case(x1, y1, x2, y2, aire_jeu_placer, bleu_fonce)
        COMPTEURCASESPLACEES += 1
        
    #le bateau est fini
    if COMPTEURCASESPLACEES == lon_bateau:
            COMPTEURBATEAU += 1
            aire_jeu_placer.unbind("<Button-1>")
            
            if COMPTEURBATEAU == 5: #si tous les bateaux sont placés, ferme la fenêtre
                fen.destroy()

    


#verification qu'une case choisie est valide 
def Valide(bateau: list, a, b, appartenance_bateau):
    cases_voisines_cote = [(a + 1, b), (a - 1, b), (a, b - 1), (a, b + 1)]
    cases_voisines_partout = [(a + i, b + k) for i in range(-1, 2) for k in range(-1, 2) if i + k != i * k]
    valide_autre_bateau = True 
    valide_adjacent = True
    une_case_en_contact = False
    
    if not appartenance_bateau[a][b]: #verification que la case choisie ne contient pas déjà un bateau
        
        #vérification qu'il n'y a pas d'autre bateau à côté
        for case in cases_voisines_cote:
            if case[0] >= 0 and case[0] <= 9 and case[1] >= 0 and case[1] <= 9: #vérification que la case voisine appartient à la grille
                if appartenance_bateau[case[0]][case[1]] and ((case[0], case[1]) not in bateau): #vérification que la case voisine ne contient pas d'autre bateau 
                    valide_autre_bateau = False
                    
        #vérification que la case choise est adjacente a une case d'une même bateau et que le bateau est en ligne droite
        if len(bateau) != 0:
            for case in cases_voisines_partout:
                if case[0] >= 0 and case[0] <= 9 and case[1] >= 0 and case[1] <= 9:
                    if (not case in cases_voisines_cote) and case in bateau:
                        valide_adjacent = False
                    
                    une_case_en_contact = une_case_en_contact or (case in cases_voisines_cote and case in bateau)
            valide_adjacent = valide_adjacent and une_case_en_contact
                    
                    
    else: valide_autre_bateau = False

    
    return valide_autre_bateau and valide_adjacent

#fonction pour annuler le placement d'une case d'un bateau
def Retour(bateaux, appartenance_bateau, aire_jeu_placer, fen):
    global COMPTEURCASESPLACEES
    i = 0
    if len(bateaux[-1]) > 0:
        i = 4
    else: 
        while len(bateaux[i + 1]) > 0:
            i += 1
    if COMPTEURCASESPLACEES == 0 or len(bateaux[0]) == 0:
        return
    
    COMPTEURCASESPLACEES += -1
    Case(bateaux[i][-1][1] * taille_case, bateaux[i][-1][0] * taille_case, (bateaux[i][-1][1] + 1) * taille_case, (bateaux[i][-1][0] + 1) * taille_case, aire_jeu_placer, couleur = bleu_clair)
    appartenance_bateau[bateaux[i][-1][0]][bateaux[i][-1][1]] = False
    del bateaux[i][-1]

#action de tirer sur une case, comprend le cas où un bateau est touché et quand aucun n'est touché (pas finie)
def Tir(event, appartenance_bateau, grille_tir): 

    a, b, x1, y1, x2, y2 = IdentificationCase(event)
    if not grille_tir[a][b]:
        if appartenance_bateau[a][b]: #un bateau est touché
            Case(x1, y1, x2, y2, aire_jeu1)
            
        else:   #aucun bateau n'est touché
            Croix(x1, y1, x2, y2, aire_jeu1)
        grille_tir[a][b] = True

#trace une croix
def Croix(x1, y1, x2, y2, aire_jeu):
    aire_jeu.create_line(x1, y1, x2, y2)
    aire_jeu.create_line(x1, y2, x2, y1)

#crée la grille de base 
def Grille(aire_jeu): 
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
    #tant qu'on ne trouve pas les coordonnées on augmente l'absisse et l'ordonnée pour trouver la case
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

 #fonction pour afficher les coups précédents lors du changement de tour 
def Redessiner(ton_appartenance_bateau, autre_appartenance, tes_tirs, autres_tirs, aire_jeu_gauche, aire_jeu_droite):
    #on redessine les bateaux du joueur
    for a in range(10):
        for b in range(10):
            if ton_appartenance_bateau[a][b]:
                Case(b * taille_case, a * taille_case,(b + 1) * taille_case, (a + 1), aire_jeu_droite, bleu_fonce)
    #on redessine les tirs du joueur
    for c in range(10):
        for d in range(10):
            if tes_tirs[c][d] and autre_appartenance:
                Case(d * taille_case, c * taille_case,(d + 1) * taille_case, (c + 1), aire_jeu_gauche)
            elif tes_tirs[c][d]:
                Croix(d * taille_case, c * taille_case,(d + 1) * taille_case, (c + 1), aire_jeu_gauche)
    #on redessine les tirs de l'autre joueur
    for e in range(10):
        for f in range(10):
            if autres_tirs[e][f]:
                Croix(f * taille_case, e * taille_case,(f + 1) * taille_case, (e + 1), aire_jeu_droite)


def EtapePlacerBateaux(appartenance_bateau, bateaux):
    global COMPTEURBATEAU 
    COMPTEURBATEAU = 0
    fen = Tk()

    aire_jeu_placer = Canvas(fen, width = taille_grille, height = taille_grille, bg = bleu_clair)
    aire_jeu_placer.pack(side = LEFT, padx = 10, pady = 10)
    Grille(aire_jeu_placer)
    
    #création des boutons pour créer les bateaux
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
    
#placement des bateaux pour les deux joueurs
EtapePlacerBateaux(appartenance_bateau_j1, bateaux_j1)
EtapePlacerBateaux(appartenance_bateau_j2, bateaux_j2)


fen = Tk()

aire_jeu1 = Canvas(fen, width=taille_grille, height=taille_grille, bg=bleu_clair)
aire_jeu1.pack(side=LEFT, padx=10, pady=10)
aire_jeu2 = Canvas(fen, width=taille_grille, height=taille_grille, bg=bleu_clair)
aire_jeu2.pack(side=RIGHT, padx=10, pady=10)
Grille(aire_jeu1)
Grille(aire_jeu2)
aire_jeu1.bind("<Button-1>", lambda event : Tir(event, appartenance_bateau_j1, grille_tir_j1))

fen.mainloop()
"""
def Tour(bateaux_j1, bateaux_j2, grille_tir_j1, grille_tir_j2):
    tour = 0
    
    while coule_j1 < nbcasestotal and coule_j2 < nbcasestotal:
        quijoue(bateaux_j1, bateaux_j2, grille_tir_j1, grille_tir_j2, appartenance_bateau_j1,appartenance_bateau_j2, tour%2)
        tour+=1
        
    if coule_j1 == nbcasestotal:
        fen.destroy()
        fen = Tk()
        tabFin = Canvas(fen, width = , height = )
        texte = 
        
    elif coule_j2 == nbcasestotal:
        fen.destroy()
        fen = Tk()
        tabFin = Canvas(fen, width = , height = )
        texte =
        
def quijoue(bateaux_j1, bateaux_j2, grille_tir_j1, grille_tir_j2, appartenance_bateau_j1,appartenance_bateau_j2, joueur):
        fen = Tk()

        aire_jeu1 = Canvas(fen, width = taille_grille, height = taille_grille, bg = bleu_clair)
        aire_jeu1.pack(side=LEFT, padx = 10, pady = 10)
        aire_jeu2 = Canvas(fen, width = taille_grille, height = taille_grille, bg = bleu_clair)
        aire_jeu2.pack(side = RIGHT, padx = 10, pady = 10)
        Grille(aire_jeu1)
        Grille(aire_jeu2)
        aire_jeu1.bind("<Button-1>", lambda event : Tir(event, appartenance_bateau_j1, grille_tir_j1, joueur))
        
        fen.mainloop()

"""  
