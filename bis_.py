from tkinter import *
from PIL import ImageTk, Image

bleu_fonce = '#22155C'
bleu_clair = '#159CDA'
blanc = '#DDF4FF'
rouge = '#FF5454'
taille_case = 50
taille_grille = taille_case * 10


def demandernom(j):
    def nom(event): 
        global nomdonne
        nomdonne = nom1.get()
        fenetre.destroy()
        return nomdonne
    fenetre = Tk()
    nom1 = Entry(fenetre) 
    nom1.bind("<Return>", nom)
    texte = Label(fenetre, text = "Nom du joueur " + str(j) + ":") 
    nom1.pack(side=BOTTOM)
    texte.pack(side=TOP)
    fenetre.mainloop()
    return nomdonne
    
joueur1=demandernom(1)
joueur2=demandernom(2)



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



#fonction pour placer un bateau
def PlacerBateau(lon_bateau, appartenance_bateau, bateaux,aire_jeu_placer, bouton,fen):
    global COMPTEURCASESPLACEES
    global COMPTEURBATEAU
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
                fen.after(2000, fen.destroy())

    

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
    if COMPTEURCASESPLACEES <= 0 or COMPTEURBATEAU > i:
        return
    
    COMPTEURCASESPLACEES += -1
    Case(bateaux[i][-1][1] * taille_case, bateaux[i][-1][0] * taille_case, (bateaux[i][-1][1] + 1) * taille_case, (bateaux[i][-1][0] + 1) * taille_case, aire_jeu_placer, couleur = bleu_clair)
    appartenance_bateau[bateaux[i][-1][0]][bateaux[i][-1][1]] = False
    del bateaux[i][-1]

    
    
#action de tirer sur une case, comprend le cas où un bateau est touché et quand aucun n'est touché (pas finie)
def Tir(event, appartenance_bateau, grille_tir,aire_jeu_gauche, fen): 
    x = 0
    
    if x ==0 :
        a, b, x1, y1, x2, y2 = IdentificationCase(event)
        if not grille_tir[a][b]:
            if appartenance_bateau[a][b]: #un bateau est touché
                Case(x1, y1, x2, y2, aire_jeu_gauche)
            
            else:   #aucun bateau n'est touché
                Croix(x1, y1, x2, y2, aire_jeu_gauche)
            grille_tir[a][b] = True
        x +=1
        
    if x> 0:
        fen.after(1000, fen.destroy())

        return a, b
        
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
    
    global a, b 
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
def Redessiner(appartenance_bateau_j1, appartenance_bateau_j2, grille_tir_j1, grille_tir_j2, aire_jeu_gauche, aire_jeu_droite, joueur):

    #on redessine les bateaux et tirs en fonction du joueur
    if joueur==1:
        for a in range(10):
            for b in range(10):
                
                if appartenance_bateau_j1[a][b]:
                    Case(b * taille_case, a * taille_case,(b + 1) * taille_case, (a + 1)* taille_case, aire_jeu_droite, bleu_fonce)

                if grille_tir_j1[a][b] and appartenance_bateau_j2[a][b]:
                    Case(b * taille_case, a * taille_case,(b + 1) * taille_case, (a + 1)* taille_case, aire_jeu_gauche)

                elif grille_tir_j1[a][b]:
                    Croix(b * taille_case, a * taille_case,(b + 1) * taille_case, (a + 1)* taille_case, aire_jeu_gauche)

                if grille_tir_j2[a][b]:
                    Croix(b * taille_case, a * taille_case,(b + 1) * taille_case, (a + 1)* taille_case, aire_jeu_droite)
                    
    elif joueur==0:
       for c in range(10):
            for d in range(10):
                if appartenance_bateau_j2[c][d]:
                    Case(d * taille_case, c * taille_case,(d + 1) * taille_case, (c + 1)* taille_case, aire_jeu_droite, bleu_fonce)

                if grille_tir_j2[c][d] and appartenance_bateau_j1[c][d]:
                    Case(d * taille_case, c * taille_case,(d + 1) * taille_case, (c + 1)* taille_case, aire_jeu_gauche)
                    
                elif grille_tir_j2[c][d]:
                    Croix(d * taille_case, c * taille_case,(d + 1) * taille_case, (c + 1)* taille_case, aire_jeu_gauche)
                    
                if grille_tir_j1[c][d]:
                    Croix(d * taille_case, c * taille_case,(d + 1) * taille_case, (c + 1)* taille_case, aire_jeu_droite)
                 
#fonction qui affiche les règles si besoin               
def reglesdujeu():
    fen1 = Tk()
    fen1.geometry("400x400")
    
    affichageregles=""
    fichier = open("reglesdujeu.txt","r")
    for ligne in fichier:
        affichageregles+=ligne
    fichier.close()
    
    regles= Label(fen1, text=str(affichageregles).encode('utf8'))

    regles.pack(expand =YES, fill = BOTH)
    fen1.mainloop()
                    
#fonction pour qu'un joueur puisse placer ses bateaux
def EtapePlacerBateaux(appartenance_bateau, bateaux, nomjoueur):
    global COMPTEURBATEAU 
    COMPTEURBATEAU = 0
    fen = Tk()

    aire_jeu_placer = Canvas(fen, width = taille_grille, height = taille_grille, bg = bleu_clair)
    aire_jeu_placer.pack(side = LEFT, padx = 10, pady = 10)
    Grille(aire_jeu_placer)
    
    #affichage du nom du joueur
    nom= Label(fen, text = nomjoueur, fg='red')
    nom.pack(side = TOP, pady = 10)
    
    #création des boutons pour créer les bateaux
    bateau2 = Button(text="Torpilleur (2 cases)", command= lambda: PlacerBateau(2, appartenance_bateau, bateaux, aire_jeu_placer, bateau2, fen))
    bateau3s = Button(text="Sous-marin (3 cases)", command= lambda: PlacerBateau(3, appartenance_bateau, bateaux,aire_jeu_placer, bateau3s, fen))
    bateau3c = Button(text="Contre-torpilleur (3 cases)", command= lambda: PlacerBateau(3, appartenance_bateau, bateaux,aire_jeu_placer, bateau3c, fen))
    bateau4 = Button(text="Croiseur (4 cases)", command= lambda: PlacerBateau(4, appartenance_bateau, bateaux,aire_jeu_placer, bateau4, fen))
    bateau5 = Button(text="Porte-avion (5 cases)", command= lambda: PlacerBateau(5, appartenance_bateau, bateaux,aire_jeu_placer, bateau5, fen))
    
    bateau2.pack(pady=2)
    bateau3s.pack(pady=2)
    bateau3c.pack(pady=2)
    bateau4.pack(pady=2)
    bateau5.pack(pady=2)
    
    retour = Button(text="Retour", command= lambda : Retour(bateaux, appartenance_bateau, aire_jeu_placer, fen))
    retour.pack(pady=10)
    
    #affichage des règles
    aide = Button(fen, text = "?", command = lambda: reglesdujeu()) 
    aide.pack(pady=2)
    
    fen.mainloop()
    
    #fonction qui renvoie True si un des joueurs a tous ses bateaux coulés(la partie est finie), et False sinon (la partie continue)
def FinPartie(appartenance_bateau_j1, appartenance_bateau_j2, grille_tir_j1, grille_tir_j2):
    j1 = j2 = 0
    for i in range(10):
        for j in range(10):
            if appartenance_bateau_j1[i][j] and not(grille_tir_j2[i][j]):
                j1+=1
                
            if appartenance_bateau_j2[i][j] and not(grille_tir_j1[i][j]):
                j2+=1

    if j1==0 or j2==0:
        return True
    return False

#trouve le bateau auquel appartient une case choisie si elle appartient à un bateau
def TrouverBateau(bateaux, case_cherchee):
    
    for bateau in range(5):
        for case in bateaux[bateau]:
            if case_cherchee == case:
                
                return bateau

def CasBateauCoule(bateaux, grille_tir, appartenance_bateau, joueur, a, b , B):    
    
    
    if joueur == 1:
        compteur = 0
        for i in bateaux[B]:
            if grille_tir_j1[i[0]][i[1]]:
                compteur +=1
                
        if compteur == len(bateaux[B]) :
            for i in bateaux[B]:
                
                
                if a < 8 and not(grille_tir_j1[i[0]+1][i[1]]) :
                    grille_tir_j1[i[0]+1][i[1]] = True
                    
                if a > 1 and not(grille_tir_j1[i[0]-1][i[1]]):
                    grille_tir_j1[i[0]-1][i[1]] = True
                    
                if b <8 and not(grille_tir_j1[i[0]][i[1]+1]):
                    grille_tir_j1[i[0]][i[1]+1] = True
                    
                if b >1 and not(grille_tir_j1[i[0]][i[1]-1]):
                    grille_tir_j1[i[0]][i[1]-1] = True
        
    elif joueur == 0:
        
        compteur = 0
        for i in bateaux[B]:
            if grille_tir_j2[i[0]][i[1]]:
                compteur +=1
                
        if compteur == len(bateaux[B]) :
            for i in bateaux[B]:
                if a <8 and not(grille_tir_j2[i[0]+1][i[1]]):
                    grille_tir_j2[i[0]+1][i[1]] = True
                    
                if a >1 and not(grille_tir_j2[i[0]-1][i[1]]):
                    grille_tir_j2[i[0]-1][i[1]] = True
                    
                if b < 8 and not(grille_tir_j2[i[0]][i[1]+1]):
                    grille_tir_j2[i[0]][i[1]+1] = True
                    
                if b > 1 and not(grille_tir_j2[i[0]][i[1]-1]):
                    grille_tir_j2[i[0]][i[1]-1] = True
    
    
#fonction pour dessiner les deux grilles du joueur dont c'est le tour. 
def quijoue(bateaux_j1, bateaux_j2, grille_tir_j1, grille_tir_j2, appartenance_bateau_j1,appartenance_bateau_j2, joueur):
        fen = Tk()
        aire_jeu_gauche = Canvas(fen, width = taille_grille, height = taille_grille, bg = bleu_clair)
        aire_jeu_gauche.pack(side=LEFT, padx = 10, pady = 10)
        aire_jeu_droite = Canvas(fen, width = taille_grille, height = taille_grille, bg = bleu_clair)
        aire_jeu_droite.pack(side = RIGHT, padx = 10, pady = 10)
        Grille(aire_jeu_gauche)
        Grille(aire_jeu_droite)
        
        
        
        if joueur == 1:
            nom = Label(fen, text = joueur1, fg = 'red')
            nom.pack(side = TOP, pady = 10)
            Redessiner(appartenance_bateau_j1, appartenance_bateau_j2, grille_tir_j1, grille_tir_j2, aire_jeu_gauche, aire_jeu_droite, joueur)
            aire_jeu_gauche.bind("<Button-1>", lambda event : Tir(event, appartenance_bateau_j2, grille_tir_j1, aire_jeu_gauche, fen))
            

        elif joueur == 0:
            nom = Label(fen, text = joueur2, fg = 'red')
            nom.pack(side = TOP, pady = 10)
            Redessiner(appartenance_bateau_j1, appartenance_bateau_j2, grille_tir_j1, grille_tir_j2, aire_jeu_gauche, aire_jeu_droite, joueur)
            aire_jeu_gauche.bind("<Button-1>", lambda event : Tir(event, appartenance_bateau_j1, grille_tir_j2, aire_jeu_gauche, fen))
            
        #affichage des règles
        aide = Button(fen, text = "?", command = lambda: reglesdujeu()) 
        aide.pack(pady=2)
        
        fen.mainloop()
        
            
        return a, b
    
def IA_ish():
    EtapePlacerBateaux(appartenance_bateau_j1, bateaux_j1, joueur1)
    while not(FinPartie(appartenance_bateau_j1, appartenance_bateau_j2, grille_tir_j1, grille_tir_j2)):
        
        a, b = randint(0, 9), randint(0, 9)
    
        if not grille_tir_j2[a][b]:
            
            grille_tir[a][b] = True
        
        fen.after(1000, fen.destroy())
        
        CaseCherchee = (a , b)
        
        if joueur == 1:
            B = TrouverBateau(bateaux_j2, CaseCherchee)
            if B != None:
                CasBateauCoule(bateaux_j2, grille_tir_j1,appartenance_bateau_j1, joueur, a, b, B)
            FinPartie(appartenance_bateau_j1, appartenance_bateau_j2, grille_tir_j1, grille_tir_j2)
            
        elif joueur == 0:
            B = TrouverBateau(bateaux_j1, CaseCherchee)
            if B != None:
                CasBateauCoule(bateaux_j1, grille_tir_j2,appartenance_bateau_j2, joueur, a, b, B)
            FinPartie(appartenance_bateau_j1, appartenance_bateau_j2, grille_tir_j1, grille_tir_j2)
        
        joueur = (joueur+1)%2
        
    
def Gagnant(grille_tir_j1, grille_tir_j2, appartenance_bateau_j1, appartenance_bateau_j2):
    for i in range(10):
        for j in range(10):
            if appartenance_bateau_j1[i][j] and (not grille_tir_j2[i][j]):
                return joueur1
            elif appartenance_bateau_j2[i][j] and (not grille_tir_j1[i][j]):
                return joueur2

def FenetreFin(gagnant):
    fen2=Tk()
    fen2.geometry("400x400")
    
    image1 = Image.open("bateauquicoule.jpg")
    fond = ImageTk.PhotoImage(image1)

    label1 = Label(image=fond)
    label1.image = fond
    label1.place(x=0, y=0)
    
    texte = Label(fen2, text = ("C'est " + str(gagnant) +" qui gagne!"), fg='red', bg='white', font=("Helvetica",20))
    texte.pack(side=TOP)
    
    fen2.mainloop()
    
        
    
#placement des bateaux pour les deux joueurs
EtapePlacerBateaux(appartenance_bateau_j1, bateaux_j1, joueur1)
EtapePlacerBateaux(appartenance_bateau_j2, bateaux_j2, joueur2)
def PartieDeuxJoueurs():
    joueur = 0

    while not(FinPartie(appartenance_bateau_j1, appartenance_bateau_j2, grille_tir_j1, grille_tir_j2)):

        a, b = quijoue(bateaux_j1, bateaux_j2, grille_tir_j1, grille_tir_j2, appartenance_bateau_j1,appartenance_bateau_j2, joueur)

        CaseCherchee = (a , b)

        if joueur == 1:
            B = TrouverBateau(bateaux_j2, CaseCherchee)
            if B != None:
                CasBateauCoule(bateaux_j2, grille_tir_j1,appartenance_bateau_j1, joueur, a, b, B)
            FinPartie(appartenance_bateau_j1, appartenance_bateau_j2, grille_tir_j1, grille_tir_j2)

        elif joueur == 0:
            B = TrouverBateau(bateaux_j1, CaseCherchee)
            if B != None:
                CasBateauCoule(bateaux_j1, grille_tir_j2,appartenance_bateau_j2, joueur, a, b, B)
            FinPartie(appartenance_bateau_j1, appartenance_bateau_j2, grille_tir_j1, grille_tir_j2)

        joueur = (joueur+1)%2


    FenetreFin(Gagnant(grille_tir_j1, grille_tir_j2, appartenance_bateau_j1, appartenance_bateau_j2))
    
PartieDeuxJoueurs()
