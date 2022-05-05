from tkinter import *

bleu = '#159CDA'
blanc = '#DDF4FF'
rouge = '#FF5454'


cases = [[[(k, i), (k + 50, i), (k, i + 50), (k + 50, i + 50)] for k in range(0, 500, 50)] for i in range(0, 500, 50)]

appartenance_bateau = {}

class Bateau:
    def __init__(self, longueur, liste_cases, joueur):
        self.longueur = longueur
        self.liste_cases = liste_cases
        self.coule = False
        self.joueur = joueur

    def touche(self, x, y):
        if self.joueur == 1:
            aire_jeu1.create_rectangle(cases[x][y][i] for i in range(4))
        else:
            aire_jeu2.create_rectangle(cases[x][y][i] for i in range(4))
    
    def placer_bateau(self):
        pass


#verification qu'une case choisie est valide 
def Valide(bateau, case_choisie):
    cases_a_cote = [[1, 0], [-1,0], [0, -1], [0, 1]]
    valide = False
    for case in cases_a_cote:
        if [case_choisie[0] + case[0], case_choisie[1] + case[1]] in bateau.liste_cases:
            valide = True
        if  (case_choisie[0] + case[0], case_choisie[1] + case[1]) in appartenance_bateau:
            valide = False

    if valide:
        bateau.liste_cases.append(case_choisie)
    
def Tir(x,y): #
    if (x, y) in appartenance_bateau:
        appartenance_bateau[(x, y)].touche(x, y)
    
def Croix(x1, y1, x2, y2, aire_jeu):
    aire_jeu.create_line(x1,y1,x2,y2)
    aire_jeu.create_line(x1,y2,x2,y1)


def Grille(aire_jeu): #création de la grille de base
    for colonne in range(1, 10):
        aire_jeu.create_line(25 * colonne, 0, 25 * colonne, 250, fill = blanc)
        aire_jeu.create_line(0, 25 * colonne, 250, 25 * colonne, fill = blanc)

def Case(x1,y1,x2,y2, aire_jeu):
    aire_jeu.create_rectangle(x1,y1,x2,y2,fill = rouge,outline= blanc)

def cbateau(event):
    clic=(event.x,event.y)
    coord=0
    a=0
    b=0
    while coord==0:
        if clic[1]>cases[a][b][-1][-1]:
            a+=1
        if clic[0]>cases[a][b][-1][0]:
            b+=1
        else:
            if clic[1]<cases[a][b][-1][-1]:
                coord=[cases[a][b][0],cases[a][b][-1]]
    x1,y1,x2,y2=coord[0][0],coord[0][1],coord[1][0],coord[1][1]
    Case(x1,y1,x2,y2,aire_jeu1)
    
fen = Tk()

aire_jeu1 = Canvas(fen, width = 250, height = 250, bg = bleu)
aire_jeu1.pack(side = LEFT, padx = 10, pady = 10)
aire_jeu2 = Canvas(fen, width = 250, height = 250, bg = bleu)
aire_jeu2.pack(side = RIGHT, padx = 10, pady = 10)
b = Button(text = 'b', command=lambda : Croix(0,0,25, 25, aire_jeu= aire_jeu1))
b.pack()
Grille(aire_jeu1)
Grille(aire_jeu2)
aire_jeu1.bind("<Button-1>",cbateau)
c = Button(text = 'c', command=lambda : Case(25,0,50, 25, aire_jeu= aire_jeu1))
c.pack()



fen.mainloop()
