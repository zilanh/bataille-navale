from tkinter import *

cases = [[[(k, i), (k + 50, i), (k, i + 50), ] for k in range(0, 500, 50)] for i in range(0, 500, 50)]

appartenance_bateau = {}

def Touche(x,y,joueur):
    if joueur == 1:
        aire_jeu1.create_rectangle(cases[x][y][i] for i in range(4))

def Tir(x,y):
    pass

def Grille(): #création de la grille de base
    for colonne in range(1, 10):
        aire_jeu1.create_line(50 * colonne, 0, 50 * colonne, 500, fill = 'black')
        aire_jeu1.create_line(0, 50 * colonne, 500, 50 * colonne, fill = 'black')

        aire_jeu2.create_line(50 * colonne, 0, 50 * colonne, 500, fill = 'black')
        aire_jeu2.create_line(0, 50 * colonne, 500, 50 * colonne, fill = 'black')

fen = Tk()


aire_jeu1 = Canvas(fen, width = 500, height = 500, bg = 'lightgrey')
aire_jeu1.pack(side = LEFT, padx = 10, pady = 10)
aire_jeu2 = Canvas(fen, width = 500, height = 500, bg = 'lightgrey')
aire_jeu2.pack(side = RIGHT, padx = 10, pady = 10)

Grille()

fen.mainloop()
