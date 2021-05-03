"""
Chaque case est un bouton(tkinter)
On utilise un tableau à 3 dimensions:
    - dimension 1: les coordonnées en x
    - dimension 2: les coordonnées en y
    - dimension 3: la valeur de la case(ID) et son état (nous reviendrons plus en détail sur ces valeurs)
L'ID de la case est sa valeur:
    - 0 pour les case est vide
    - 1 à 8 pour les différents numérots
    - 9 ou plus pour les bombes
L'état de la case peut prendre 3 valeurs:
    - 0 : la case n'est pas encore ouverte
    - 1 : la case est ouverte
    - 2 : il y a un drapeau sur la case
"""

from random import randint
from tkinter import*
from time import time_ns,sleep
from math import sqrt,exp
from winsound import PlaySound,SND_ASYNC,SND_LOOP
import sqlite3
from PIL import Image,ImageTk

########################################################################################################
######################################### CLASSES ######################################################
########################################################################################################
class Grille:
    def __init__(self,grille,taille_case,taille_label):
        self.grille=grille
        self.image_label=case_vide
        self.taille_label=taille_label
        self.taille_case=taille_case
        self.grille_button=[[0 for i in range(c)]for i in range (l)]
        self.grille_label=[[0 for i in range(c)]for i in range (l)]
        self.premier_clic=False

    def generer_boutons(self):
        """Méthode qui génère les boutons. Elle génère également la "grille de fond" qui affiche les valeurs des cases au joueur.
        Les boutons ont deux actions : clic gauche, qui dévoile la case; et clic droit, qui pose un drapeau."""
        for i in range(len(self.grille)):
            for j in range(len(self.grille[i])):
                self.grille_label[i][j] = Label(grille,bd=1,justify=CENTER,relief="flat",image=self.image_label,width=self.taille_label,height=self.taille_label,bg='black')
                self.grille_label[i][j].grid(column=j,row=i)
                self.grille_button[i][j] = Button(grille,width=self.taille_case,height=self.taille_case,image=case_cachee,relief='flat',bg='black')
                self.grille_button[i][j].grid(column=j,row=i)
                self.grille_button[i][j].bind("<Button-3>",lambda i,x=i,y=j: self.afficheFlag(x,y))
                self.grille_button[i][j].bind("<Button-1>",lambda i,x=i,y=j: self.click(x,y))

    def affiche_valeurs(self,ligne,colonne):
        """ permet de savoir quelle valeur afficher quand on click sur une case """
        if self.grille[ligne][colonne][1]==0:

            if self.grille[ligne][colonne][0] == 0 :
                self.image_label=case_vide
            elif self.grille[ligne][colonne][0] == 1 :
                self.image_label=case1
            elif self.grille[ligne][colonne][0] == 2 :
                self.image_label=case2
            elif self.grille[ligne][colonne][0] == 3 :
                self.image_label=case3
            elif self.grille[ligne][colonne][0] == 4 :
                self.image_label=case4
            elif self.grille[ligne][colonne][0] == 5 :
                self.image_label=case5
            elif self.grille[ligne][colonne][0] == 6 :
                self.image_label=case6
            elif self.grille[ligne][colonne][0] == 7 :
                self.image_label=case7
            elif self.grille[ligne][colonne][0] == 8 :
                self.image_label=case8
            elif self.grille[ligne][colonne][0]==9 :
                self.image_label=case_bombe

                global vie,label_vies
                vie-=1
                label_vies.destroy()
                label_vies=Label(window,text=("vies:",vie),font=("TkDefaultFont",20),bg="#00008E",fg="#FF001E")
                label_vies.place(x=10*coeff_reduc,y=10*coeff_reduc)

                global bombes_trouvees,bombes_posees
                bombes_trouvees+=1
                bombes_posees+=1
            try :
                self.grille_label[ligne][colonne]['image']=self.image_label
                self.grille_button[ligne][colonne].grid_remove()
                self.grille[ligne][colonne][1]=1
            except :
                    pass

    def click(self,ligne,colonne):
        """Méthode qui dévoile la case si le bouton est cliqué (via le clic gauche). Elle efface le bouton,
        et modifie la case de la grille sous le bouton pour que la bonne valeur soit affichée.
        Elle prends aussi en charge de dévoiler les cases adjacentes à une case vide (diagonale non prise en charge)"""
        

        while self.premier_clic==False and self.grille[ligne][colonne][0] != 0:
            self.grille=generer_grille(l,c,bombes)
            print('---------------------------')
            affiche_grille_console(self.grille)
        if self.premier_clic==False:
            global chrono
            chrono=time_ns()
        self.premier_clic=True


        if self.grille[ligne][colonne][0] == 0 and self.grille[ligne][colonne][1] == 0:
            self.affiche_valeurs(ligne,colonne)
            if ligne !=0 :
                self.click(ligne-1,colonne)
            if ligne !=l-1 :
                self.click(ligne+1,colonne)
            if colonne !=0 :
                self.click(ligne,colonne-1)
            if colonne !=c-1 :
                self.click(ligne,colonne+1)

        else:
            self.affiche_valeurs(ligne,colonne)
        
        verif_fin(vie,bombes_trouvees,bombes_posees)

    def afficheFlag(self,ligne,colonne):
        """Méthode qui modifie l'image du bouton pour afficher un drapeau. Le joueur ne peut ainsi plus dévoiler
        la case, à moins d'enlever le drapeau.
        Ajouter/Enlever un drapeau se fait par clic droit"""
        if not self.grille[ligne][colonne][1]==2:
            self.grille[ligne][colonne][1]=2
            self.grille_button[ligne][colonne]['image']=case_drapeau
            if self.grille[ligne][colonne][0]==9:
                global bombes_trouvees,bombes_posees
                bombes_trouvees+=1
                bombes_posees+=1
                verif_fin(vie,bombes_trouvees,bombes_posees)
            else:
                bombes_posees+=1
                verif_fin(vie,bombes_trouvees,bombes_posees)

        elif self.grille[ligne][colonne][1]==2:
            self.grille[ligne][colonne][1]=0
            self.grille_button[ligne][colonne]['image']=case_cachee
            if self.grille[ligne][colonne][0]==9:
                bombes_trouvees-=1
                bombes_posees-=1
                return bombes_trouvees,bombes_posees
            else:
                bombes_posees-=1
                verif_fin(vie,bombes_trouvees,bombes_posees)

########################################################################################################
######################################### FONCTIONS ####################################################
########################################################################################################

def ecran_titre():
    """ génère l'écran du menu principal """
    try:
        suppr_tout()
        jeu_bouton_menu.destroy()
        label_vies.destroy()
    except:
        pass
    try:
        classements_menu.destroy()
    except:
        pass
    try:
        d_menu.destroy()
        d_abando.destroy()
    except:
        pass
    try:
        v_menu.destroy()
        v_sauver.destroy()
    except:
        pass
    try:
        options_bouton_aide.destroy()
        options_bouton_fond.destroy()
        options_bouton_menu.destroy()
        options_bouton_musique.destroy()
        options_mute.destroy()
    except:
        pass
    try:
        preview_fond_label.destroy()
    except:
        pass
    try:
        image_fond_label['image']=img_menu_fond
    except:
        pass
    try:
        difficulte_facile.destroy()
        difficulte_moyen.destroy()
        difficulte_difficile.destroy()
        difficulte_menu.destroy()
    except:
        pass
    try:
        classement_menu.destroy()
        facile_menu.destroy()
        moyen_menu.destroy()
        difficile_menu.destroy()
    except:
        pass
    try:
        classement_frame_facile.destroy()
    except:
        pass
    try:
        classement_frame_moyen.destroy()
    except:
        pass
    try:
        classement_frame_difficile.destroy()
    except:
        pass
    global menu_jouer,menu_quitter,menu_classement,menu_options
    menu_jouer=Button(window,image=img_menu_bouton_jouer,bd=0,width=400*coeff_reduc,height=180*coeff_reduc,relief="flat",command=lambda:ecran_difficultes())
    menu_jouer.place(x=300*coeff_reduc,y=300*coeff_reduc)

    menu_quitter=Button(window,image=img_menu_bouton_quitter,bd=0,width=400*coeff_reduc,height=180*coeff_reduc,relief="flat",command=lambda:window.destroy())
    menu_quitter.place(x=300*coeff_reduc,y=550*coeff_reduc)

    menu_classement=Button(window,image=img_menu_bouton_classement,bd=0,width=400*coeff_reduc,height=180*coeff_reduc,relief="flat",command=lambda:ecran_classement())
    menu_classement.place(x=950*coeff_reduc,y=300*coeff_reduc)

    menu_options=Button(window,image=img_menu_bouton_options,bd=0,width=400*coeff_reduc,height=180*coeff_reduc,relief="flat",command=lambda:ecran_options())
    menu_options.place(x=950*coeff_reduc,y=550*coeff_reduc)

def ecran_classement():
    """ génère l'écran du classement pour choisir les difficultées """
    menu_jouer.destroy()
    menu_quitter.destroy()
    menu_classement.destroy()
    menu_options.destroy()
    image_fond_label['image']=classement_fond
    global classement_menu,facile_menu,moyen_menu,difficile_menu
    classement_menu=Button(window,image=difficultes_bouton_menu,bd=0,width=400*coeff_reduc,height=180*coeff_reduc,relief="flat",command=lambda:ecran_titre())
    classement_menu.place(x=950*coeff_reduc,y=550*coeff_reduc)

    facile_menu=Button(window,image=difficultes_bouton_facile,bd=0,width=400*coeff_reduc,height=180*coeff_reduc,relief="flat",command=lambda:classement_difficulte("facile"))
    facile_menu.place(x=300*coeff_reduc,y=300*coeff_reduc)

    moyen_menu=Button(window,image=difficultes_bouton_moyen,bd=0,width=400*coeff_reduc,height=180*coeff_reduc,relief="flat",command=lambda:classement_difficulte("moyen"))
    moyen_menu.place(x=300*coeff_reduc,y=550*coeff_reduc)

    difficile_menu=Button(window,image=difficultes_bouton_difficile,bd=0,width=400*coeff_reduc,height=180*coeff_reduc,relief="flat",command=lambda:classement_difficulte("difficile"))
    difficile_menu.place(x=950*coeff_reduc,y=300*coeff_reduc)

def classement_difficulte(difficulte):
    """ génère l'écran et le tableau de classement choisit avec la fonction ecran_classement """
    global classements_menu,classement_frame_facile,classement_frame_moyen,classement_frame_difficile
    if difficulte =='facile':
        facile_menu.destroy()
        moyen_menu.destroy()
        difficile_menu.destroy()

        classement_menu.destroy()
        classements_menu=Button(window,image=difficultes_bouton_menu,bd=0,width=400*coeff_reduc,height=180*coeff_reduc,relief="flat",command=lambda:ecran_titre())
        classements_menu.place(x=600*coeff_reduc,y=550*coeff_reduc)

        image_fond_label['image']=classement_fond

        classement_frame_facile=Frame(window)
        classement_frame_facile.pack(pady=130)

        execution_facile=cursor.execute(""" 
        SELECT nom,score,temps FROM FACILE ORDER BY score DESC
        """)
        selection_facile=cursor.fetchall()
        try :
            nom1_facile=selection_facile[0][0]
        except IndexError:
            nom1_facile=""
        try :
            nom2_facile=selection_facile[1][0]
        except IndexError:
            nom2_facile=""
        try :
            nom3_facile=selection_facile[2][0]
        except IndexError:
            nom3_facile=""
        try :
            nom4_facile=selection_facile[3][0]
        except IndexError:
            nom4_facile=""
        try :
            nom5_facile=selection_facile[4][0]
        except IndexError:
            nom5_facile=""


        try :
            score1_facile=selection_facile[0][1]
        except IndexError:
            score1_facile=""
        try :
            score2_facile=selection_facile[1][1]
        except IndexError:
            score2_facile=""
        try :
            score3_facile=selection_facile[2][1]
        except IndexError:
            score3_facile=""
        try :
            score4_facile=selection_facile[3][1]
        except IndexError:
            score4_facile=""
        try :
            score5_facile=selection_facile[4][1]
        except IndexError:
            score5_facile=""


        try :
            temps1_facile=selection_facile[0][2]
        except IndexError:
            temps1_facile=""
        try :
            temps2_facile=selection_facile[1][2]
        except IndexError:
            temps2_facile=""
        try :
            temps3_facile=selection_facile[2][2]
        except IndexError:
            temps3_facile=""
        try :
            temps4_facile=selection_facile[3][2]
        except IndexError:
            temps4_facile=""
        try :
            temps5_facile=selection_facile[4][2]
        except IndexError:
            temps5_facile=""

        tab_nom_facile=Label(classement_frame_facile,width=30,height=2,relief="raised",bg="#1BE34D",text="nom")
        tab_nom_facile.grid(row=0,column=0)
        tab_score_facile=Label(classement_frame_facile,width=30,height=2,relief="raised",bg="#1BE34D",text="score")
        tab_score_facile.grid(row=0,column=1)
        tab_temps_facile=Label(classement_frame_facile,width=30,height=2,relief="raised",bg="#1BE34D",text="temps")
        tab_temps_facile.grid(row=0,column=2)

        tab_nom1_facile=Label(classement_frame_facile,width=30,height=2,relief="raised",bg="#20FD05",text=nom1_facile)
        tab_nom1_facile.grid(row=1,column=0)
        tab_nom2_facile=Label(classement_frame_facile,width=30,height=2,relief="raised",bg="#20FD05",text=nom2_facile)
        tab_nom2_facile.grid(row=2,column=0)
        tab_nom3_facile=Label(classement_frame_facile,width=30,height=2,relief="raised",bg="#20FD05",text=nom3_facile)
        tab_nom3_facile.grid(row=3,column=0)
        tab_nom4_facile=Label(classement_frame_facile,width=30,height=2,relief="raised",bg="#20FD05",text=nom4_facile)
        tab_nom4_facile.grid(row=4,column=0)
        tab_nom5_facile=Label(classement_frame_facile,width=30,height=2,relief="raised",bg="#20FD05",text=nom5_facile)
        tab_nom5_facile.grid(row=5,column=0)

        tab_score1_facile=Label(classement_frame_facile,width=30,height=2,relief="raised",bg="#20FD05",text=str(score1_facile))
        tab_score1_facile.grid(row=1,column=1)
        tab_score2_facile=Label(classement_frame_facile,width=30,height=2,relief="raised",bg="#20FD05",text=str(score2_facile))
        tab_score2_facile.grid(row=2,column=1)
        tab_score3_facile=Label(classement_frame_facile,width=30,height=2,relief="raised",bg="#20FD05",text=str(score3_facile))
        tab_score3_facile.grid(row=3,column=1)
        tab_score4_facile=Label(classement_frame_facile,width=30,height=2,relief="raised",bg="#20FD05",text=str(score4_facile))
        tab_score4_facile.grid(row=4,column=1)
        tab_score5_facile=Label(classement_frame_facile,width=30,height=2,relief="raised",bg="#20FD05",text=str(score5_facile))
        tab_score5_facile.grid(row=5,column=1)

        tab_temps1_facile=Label(classement_frame_facile,width=30,height=2,relief="raised",bg="#20FD05",text=temps1_facile)
        tab_temps1_facile.grid(row=1,column=2)
        tab_temps2_facile=Label(classement_frame_facile,width=30,height=2,relief="raised",bg="#20FD05",text=temps2_facile)
        tab_temps2_facile.grid(row=2,column=2)
        tab_temps3_facile=Label(classement_frame_facile,width=30,height=2,relief="raised",bg="#20FD05",text=temps3_facile)
        tab_temps3_facile.grid(row=3,column=2)
        tab_temps4_facile=Label(classement_frame_facile,width=30,height=2,relief="raised",bg="#20FD05",text=temps4_facile)
        tab_temps4_facile.grid(row=4,column=2)
        tab_temps5_facile=Label(classement_frame_facile,width=30,height=2,relief="raised",bg="#20FD05",text=temps5_facile)
        tab_temps5_facile.grid(row=5,column=2)

    elif difficulte=='moyen':
        facile_menu.destroy()
        moyen_menu.destroy()
        difficile_menu.destroy()

        classement_menu.destroy()
        classements_menu=Button(window,image=difficultes_bouton_menu,bd=0,width=400*coeff_reduc,height=180*coeff_reduc,relief="flat",command=lambda:ecran_titre())
        classements_menu.place(x=600*coeff_reduc,y=550*coeff_reduc)

        image_fond_label['image']=classement_fond

        classement_frame_moyen=Frame(window)
        classement_frame_moyen.pack(pady=130)

        execution_moyen=cursor.execute(""" 
        SELECT nom,score,temps FROM MOYEN ORDER BY score DESC
        """)
        selection_moyen=cursor.fetchall()
        try :
            nom1_moyen=selection_moyen[0][0]
        except IndexError:
            nom1_moyen=""
        try :
            nom2_moyen=selection_moyen[1][0]
        except IndexError:
            nom2_moyen=""
        try :
            nom3_moyen=selection_moyen[2][0]
        except IndexError:
            nom3_moyen=""
        try :
            nom4_moyen=selection_moyen[3][0]
        except IndexError:
            nom4_moyen=""
        try :
            nom5_moyen=selection_moyen[4][0]
        except IndexError:
            nom5_moyen=""


        try :
            score1_moyen=selection_moyen[0][1]
        except IndexError:
            score1_moyen=""
        try :
            score2_moyen=selection_moyen[1][1]
        except IndexError:
            score2_moyen=""
        try :
            score3_moyen=selection_moyen[2][1]
        except IndexError:
            score3_moyen=""
        try :
            score4_moyen=selection_moyen[3][1]
        except IndexError:
            score4_moyen=""
        try :
            score5_moyen=selection_moyen[4][1]
        except IndexError:
            score5_moyen=""


        try :
            temps1_moyen=selection_moyen[0][2]
        except IndexError:
            temps1_moyen=""
        try :
            temps2_moyen=selection_moyen[1][2]
        except IndexError:
            temps2_moyen=""
        try :
            temps3_moyen=selection_moyen[2][2]
        except IndexError:
            temps3_moyen=""
        try :
            temps4_moyen=selection_moyen[3][2]
        except IndexError:
            temps4_moyen=""
        try :
            temps5_moyen=selection_moyen[4][2]
        except IndexError:
            temps5_moyen=""

        tab_nom_moyen=Label(classement_frame_moyen,width=30,height=2,relief="raised",bg="#FD209D",text="nom")
        tab_nom_moyen.grid(row=0,column=0)
        tab_score_moyen=Label(classement_frame_moyen,width=30,height=2,relief="raised",bg="#FD209D",text="score")
        tab_score_moyen.grid(row=0,column=1)
        tab_temps_moyen=Label(classement_frame_moyen,width=30,height=2,relief="raised",bg="#FD209D",text="temps")
        tab_temps_moyen.grid(row=0,column=2)

        tab_nom1_moyen=Label(classement_frame_moyen,width=30,height=2,relief="raised",bg="#8230FF",text=nom1_moyen)
        tab_nom1_moyen.grid(row=1,column=0)
        tab_nom2_moyen=Label(classement_frame_moyen,width=30,height=2,relief="raised",bg="#8230FF",text=nom2_moyen)
        tab_nom2_moyen.grid(row=2,column=0)
        tab_nom3_moyen=Label(classement_frame_moyen,width=30,height=2,relief="raised",bg="#8230FF",text=nom3_moyen)
        tab_nom3_moyen.grid(row=3,column=0)
        tab_nom4_moyen=Label(classement_frame_moyen,width=30,height=2,relief="raised",bg="#8230FF",text=nom4_moyen)
        tab_nom4_moyen.grid(row=4,column=0)
        tab_nom5_moyen=Label(classement_frame_moyen,width=30,height=2,relief="raised",bg="#8230FF",text=nom5_moyen)
        tab_nom5_moyen.grid(row=5,column=0)

        tab_score1_moyen=Label(classement_frame_moyen,width=30,height=2,relief="raised",bg="#8230FF",text=str(score1_moyen))
        tab_score1_moyen.grid(row=1,column=1)
        tab_score2_moyen=Label(classement_frame_moyen,width=30,height=2,relief="raised",bg="#8230FF",text=str(score2_moyen))
        tab_score2_moyen.grid(row=2,column=1)
        tab_score3_moyen=Label(classement_frame_moyen,width=30,height=2,relief="raised",bg="#8230FF",text=str(score3_moyen))
        tab_score3_moyen.grid(row=3,column=1)
        tab_score4_moyen=Label(classement_frame_moyen,width=30,height=2,relief="raised",bg="#8230FF",text=str(score4_moyen))
        tab_score4_moyen.grid(row=4,column=1)
        tab_score5_moyen=Label(classement_frame_moyen,width=30,height=2,relief="raised",bg="#8230FF",text=str(score5_moyen))
        tab_score5_moyen.grid(row=5,column=1)

        tab_temps1_moyen=Label(classement_frame_moyen,width=30,height=2,relief="raised",bg="#8230FF",text=temps1_moyen)
        tab_temps1_moyen.grid(row=1,column=2)
        tab_temps2_moyen=Label(classement_frame_moyen,width=30,height=2,relief="raised",bg="#8230FF",text=temps2_moyen)
        tab_temps2_moyen.grid(row=2,column=2)
        tab_temps3_moyen=Label(classement_frame_moyen,width=30,height=2,relief="raised",bg="#8230FF",text=temps3_moyen)
        tab_temps3_moyen.grid(row=3,column=2)
        tab_temps4_moyen=Label(classement_frame_moyen,width=30,height=2,relief="raised",bg="#8230FF",text=temps4_moyen)
        tab_temps4_moyen.grid(row=4,column=2)
        tab_temps5_moyen=Label(classement_frame_moyen,width=30,height=2,relief="raised",bg="#8230FF",text=temps5_moyen)
        tab_temps5_moyen.grid(row=5,column=2)

    elif difficulte=='difficile':
        facile_menu.destroy()
        moyen_menu.destroy()
        difficile_menu.destroy()
        
        classement_menu.destroy()
        classements_menu=Button(window,image=difficultes_bouton_menu,bd=0,width=400*coeff_reduc,height=180*coeff_reduc,relief="flat",command=lambda:ecran_titre())
        classements_menu.place(x=600*coeff_reduc,y=550*coeff_reduc)

        image_fond_label['image']=classement_fond

        classement_frame_difficile=Frame(window)
        classement_frame_difficile.pack(pady=130)

        execution_difficile=cursor.execute(""" 
        SELECT nom,score,temps FROM DIFFICILE ORDER BY score DESC
        """)
        selection_difficile=cursor.fetchall()
        try :
            nom1_difficile=selection_difficile[0][0]
        except IndexError:
            nom1_difficile=""
        try :
            nom2_difficile=selection_difficile[1][0]
        except IndexError:
            nom2_difficile=""
        try :
            nom3_difficile=selection_difficile[2][0]
        except IndexError:
            nom3_difficile=""
        try :
            nom4_difficile=selection_difficile[3][0]
        except IndexError:
            nom4_difficile=""
        try :
            nom5_difficile=selection_difficile[4][0]
        except IndexError:
            nom5_difficile=""


        try :
            score1_difficile=selection_difficile[0][1]
        except IndexError:
            score1_difficile=""
        try :
            score2_difficile=selection_difficile[1][1]
        except IndexError:
            score2_difficile=""
        try :
            score3_difficile=selection_difficile[2][1]
        except IndexError:
            score3_difficile=""
        try :
            score4_difficile=selection_difficile[3][1]
        except IndexError:
            score4_difficile=""
        try :
            score5_difficile=selection_difficile[4][1]
        except IndexError:
            score5_difficile=""


        try :
            temps1_difficile=selection_difficile[0][2]
        except IndexError:
            temps1_difficile=""
        try :
            temps2_difficile=selection_difficile[1][2]
        except IndexError:
            temps2_difficile=""
        try :
            temps3_difficile=selection_difficile[2][2]
        except IndexError:
            temps3_difficile=""
        try :
            temps4_difficile=selection_difficile[3][2]
        except IndexError:
            temps4_difficile=""
        try :
            temps5_difficile=selection_difficile[4][2]
        except IndexError:
            temps5_difficile=""

        tab_nom_difficile=Label(classement_frame_difficile,width=30,height=2,relief="raised",bg="#F70142",text="nom")
        tab_nom_difficile.grid(row=0,column=0)
        tab_score_difficile=Label(classement_frame_difficile,width=30,height=2,relief="raised",bg="#F70142",text="score")
        tab_score_difficile.grid(row=0,column=1)
        tab_temps_difficile=Label(classement_frame_difficile,width=30,height=2,relief="raised",bg="#F70142",text="temps")
        tab_temps_difficile.grid(row=0,column=2)

        tab_nom1_difficile=Label(classement_frame_difficile,width=30,height=2,relief="raised",bg="#E420B3",text=nom1_difficile)
        tab_nom1_difficile.grid(row=1,column=0)
        tab_nom2_difficile=Label(classement_frame_difficile,width=30,height=2,relief="raised",bg="#E420B3",text=nom2_difficile)
        tab_nom2_difficile.grid(row=2,column=0)
        tab_nom3_difficile=Label(classement_frame_difficile,width=30,height=2,relief="raised",bg="#E420B3",text=nom3_difficile)
        tab_nom3_difficile.grid(row=3,column=0)
        tab_nom4_difficile=Label(classement_frame_difficile,width=30,height=2,relief="raised",bg="#E420B3",text=nom4_difficile)
        tab_nom4_difficile.grid(row=4,column=0)
        tab_nom5_difficile=Label(classement_frame_difficile,width=30,height=2,relief="raised",bg="#E420B3",text=nom5_difficile)
        tab_nom5_difficile.grid(row=5,column=0)

        tab_score1_difficile=Label(classement_frame_difficile,width=30,height=2,relief="raised",bg="#E420B3",text=str(score1_difficile))
        tab_score1_difficile.grid(row=1,column=1)
        tab_score2_difficile=Label(classement_frame_difficile,width=30,height=2,relief="raised",bg="#E420B3",text=str(score2_difficile))
        tab_score2_difficile.grid(row=2,column=1)
        tab_score3_difficile=Label(classement_frame_difficile,width=30,height=2,relief="raised",bg="#E420B3",text=str(score3_difficile))
        tab_score3_difficile.grid(row=3,column=1)
        tab_score4_difficile=Label(classement_frame_difficile,width=30,height=2,relief="raised",bg="#E420B3",text=str(score4_difficile))
        tab_score4_difficile.grid(row=4,column=1)
        tab_score5_difficile=Label(classement_frame_difficile,width=30,height=2,relief="raised",bg="#E420B3",text=str(score5_difficile))
        tab_score5_difficile.grid(row=5,column=1)

        tab_temps1_difficile=Label(classement_frame_difficile,width=30,height=2,relief="raised",bg="#E420B3",text=temps1_difficile)
        tab_temps1_difficile.grid(row=1,column=2)
        tab_temps2_difficile=Label(classement_frame_difficile,width=30,height=2,relief="raised",bg="#E420B3",text=temps2_difficile)
        tab_temps2_difficile.grid(row=2,column=2)
        tab_temps3_difficile=Label(classement_frame_difficile,width=30,height=2,relief="raised",bg="#E420B3",text=temps3_difficile)
        tab_temps3_difficile.grid(row=3,column=2)
        tab_temps4_difficile=Label(classement_frame_difficile,width=30,height=2,relief="raised",bg="#E420B3",text=temps4_difficile)
        tab_temps4_difficile.grid(row=4,column=2)
        tab_temps5_difficile=Label(classement_frame_difficile,width=30,height=2,relief="raised",bg="#E420B3",text=temps5_difficile)
        tab_temps5_difficile.grid(row=5,column=2)        

def ecran_difficultes():
    """ génère l'écran des difficultés """
    image_fond_label['image']=difficultes_fond
    menu_jouer.destroy()
    menu_quitter.destroy()
    menu_classement.destroy()
    menu_options.destroy()
    global difficulte_facile,difficulte_moyen,difficulte_difficile,difficulte_menu
    difficulte_facile=Button(window,image=difficultes_bouton_facile,bd=0,width=400*coeff_reduc,height=180*coeff_reduc,relief="flat",command=lambda:debut_facile())
    difficulte_facile.place(x=300*coeff_reduc,y=300*coeff_reduc)

    difficulte_moyen=Button(window,image=difficultes_bouton_moyen,bd=0,width=400*coeff_reduc,height=180*coeff_reduc,relief="flat",command=lambda:debut_normal())
    difficulte_moyen.place(x=300*coeff_reduc,y=550*coeff_reduc)

    difficulte_difficile=Button(window,image=difficultes_bouton_difficile,bd=0,width=400*coeff_reduc,height=180*coeff_reduc,relief="flat",command=lambda:debut_difficile())
    difficulte_difficile.place(x=950*coeff_reduc,y=300*coeff_reduc)

    difficulte_menu=Button(window,image=difficultes_bouton_menu,bd=0,width=400*coeff_reduc,height=180*coeff_reduc,relief="flat",command=lambda:ecran_titre())
    difficulte_menu.place(x=950*coeff_reduc,y=550*coeff_reduc)

def ecran_options():
    """ génère l'écran des options """
    image_fond_label['image']=img_options_fond
    menu_jouer.destroy()
    menu_quitter.destroy()
    menu_classement.destroy()
    menu_options.destroy()
    global options_bouton_aide,options_bouton_fond,options_bouton_menu,options_bouton_musique,preview_fond_label,options_mute
    options_bouton_aide=Button(window,image=img_options_bouton_aide,bd=0,width=400*coeff_reduc,height=180*coeff_reduc,relief="flat",command=lambda:aide())
    options_bouton_aide.place(x=300*coeff_reduc,y=300*coeff_reduc)

    options_bouton_fond=Button(window,image=img_options_bouton_fond,bd=0,width=400*coeff_reduc,height=180*coeff_reduc,relief="flat",command=lambda:changer_fond())
    options_bouton_fond.place(x=300*coeff_reduc,y=550*coeff_reduc)

    preview_fond_label=Label(window,image=preview_fond4,bd=0,width=335*coeff_reduc,height=185*coeff_reduc, bg='black')
    preview_fond_label.place(x=20*coeff_reduc,y=20*coeff_reduc)

    options_bouton_menu=Button(window,image=img_options_bouton_menu,bd=0,width=400*coeff_reduc,height=180*coeff_reduc,relief="flat",command=lambda:ecran_titre())
    options_bouton_menu.place(x=950*coeff_reduc,y=550*coeff_reduc)

    options_bouton_musique=Button(window,image=img_options_bouton_musique,bd=0,width=400*coeff_reduc,height=180*coeff_reduc,relief="flat",command=lambda:changer_musique())
    options_bouton_musique.place(x=950*coeff_reduc,y=300*coeff_reduc)

    options_mute=Checkbutton(window,text="mute",bg="#222222",fg="#E645FF",selectcolor="#222222",font=("TkDefaultFont",15),bd=0,command=lambda:mute())
    options_mute.place(x=1400*coeff_reduc,y=450*coeff_reduc)

def affiche_grille_console(grille):
    """Permet d'afficher la grille dans la console
    Utilisée pour le développement
    grille: nom de la grille
    c: nombre de colones de la grille"""
    for i in (grille):
        to_send = ""
        for j in i :
            to_send += str(j[0])+" "
        print(to_send)

def generer_grille(x,y,nb_bombes):
    """ Fonction qui génère des bombes placées aléatoirement dans la grille(grille console).
    Elle prend en compte le fait qu'une case ait déjà une bombe
    Puis elle génère les nombres autour des bombes en prenant en compte les cas spéciaux
    grille: nom de la grille
    nb_bombes: nombre de bombes à placer
    c: nombre de colones
    l: nombre de lignes
    """
    assert x*y>nb_bombes,"TROP DE BOMBES"
    grille=[[[0,0] for i in range(y+2)]for i in range (x+2)]
    bombes_placees=0
    while bombes_placees!=nb_bombes:
        a=randint(1,x)
        b=randint(1,y)
        if grille[a][b][0]<9:
            grille[a][b][0]=9
            bombes_placees+=1

    for i in range(len(grille)):
        for j in range (len(grille[i])):
            if grille[i][j][0]>=9:
                grille[i][j+1][0]+=1
                grille[i][j-1][0]+=1
                grille[i+1][j][0]+=1
                grille[i-1][j][0]+=1
                grille[i-1][j-1][0]+=1
                grille[i+1][j+1][0]+=1
                grille[i+1][j-1][0]+=1
                grille[i-1][j+1][0]+=1

    for i in range(len(grille)):
        for j in range (len(grille[i])):
            if grille[i][j][0]>=9:
                grille[i][j][0]=9

    grille = grille[1:-1]
    for i in range(len(grille)) :
        grille[i] = grille[i][1:-1]

    return grille

def debut_facile():
    """Début de la partie en difficulté facile. On initialise le chrono, et génère la grille 
    (en donnant l = nombre de lignes, c= nombre de colonne, bombes = nombre de bombes, vie = le nombre de vie)
    """
    try:
        difficulte_facile.destroy()
        difficulte_moyen.destroy()
        difficulte_difficile.destroy()
    except:
        pass
    global l,c,bombes,vie,nbmax,casehaut,casebas,bombes_trouvees,bombes_posees,chrono   #Toutes ces variables sont utilisés au sein du code
    l=9
    c=9
    bombes=10
    vie=3

    nbmax=(l*c)-1   # indice de la dernière cases, tout en bas à droite (dans un cadre de 9x9, cette case sera 80)
    casehaut=[]
    casebas=[]
    casehaut.append(0)
    for i in range(l):
        casehaut.append((i+1)*c)
        casebas.append(((i+1)*c)-1)
    casebas.append(c*l)
    bombes_trouvees=0
    bombes_posees=0
    
    debut_de_partie()
    chrono=time_ns()

def debut_normal():
    """Début de la partie en difficulté normal. On initialise le chrono, et génère la grille 
    (en donnant l = nombre de lignes, c = nombre de colonne, bombes = nombre de bombes, vie = le nombre de vie)
    """
    try:
        difficulte_facile.destroy()
        difficulte_moyen.destroy()
        difficulte_difficile.destroy()
    except:
        pass
    global l,c,bombes,vie,nbmax,casehaut,casebas,bombes_trouvees,bombes_posees,chrono   #Toutes ces variables sont utilisés au sein du code
    l=12
    c=12
    bombes=25
    vie=3

    nbmax=(l*c)-1   # indice de la dernière cases, tout en bas à droite (dans un cadre de 9x9, cette case sera 80)
    casehaut=[]
    casebas=[]
    casehaut.append(0)
    for i in range(l):
        casehaut.append((i+1)*c)
        casebas.append(((i+1)*c)-1)
    casebas.append(c*l)
    bombes_trouvees=0
    bombes_posees=0
    
    debut_de_partie()
    chrono=time_ns()

def debut_difficile():
    """Début de la partie en difficulté maximale. On initialise le chrono, et génère la grille 
    (en donnant l = nombre de lignes, c = nombre de colonne, bombes = nombre de bombes, vie = le nombre de vie)
    """
    try:
        difficulte_facile.destroy()
        difficulte_moyen.destroy()
        difficulte_difficile.destroy()
    except:
        pass
    global l,c,bombes,vie,nbmax,casehaut,casebas,bombes_trouvees,bombes_posees,chrono   #Toutes ces variables sont utilisés au sein du code
    l=12
    c=24
    bombes=80
    vie=3

    nbmax=(l*c)-1   # indice de la dernière cases, tout en bas à droite (dans un cadre de 9x9, cette case sera 80)
    casehaut=[]
    casebas=[]
    casehaut.append(0)
    for i in range(l):
        casehaut.append((i+1)*c)
        casebas.append(((i+1)*c)-1)
    casebas.append(c*l)
    bombes_trouvees=0
    
    debut_de_partie()
    chrono=time_ns()

def debut_de_partie():
    """ génère l'écran du début de la partie et la grille(graphiquement) """
    try:
        global image_fond_label

        image_fond_label=Label(window, image=fond_en_cours)
        image_fond_label.place(x=0,y=0,relwidth=1,relheight=1) 
        suppr_tout()
    except:
        pass
    global grille_console
    grille_console=generer_grille(l,c,bombes)
    affiche_grille_console(grille_console)

    global grille
    grille=Frame(window)
    grille.pack(pady=int(resolution[-3]))
    taille=58*coeff_reduc
    gr=Grille(grille_console,taille,taille+4)
    gr.generer_boutons()

    global jeu_bouton_menu
    jeu_bouton_menu=Button(window,image=img_jeu_bouton_menu,bd=0,width=190,height=80,relief="flat",command=lambda:ecran_titre())
    jeu_bouton_menu.place(x=10*coeff_reduc,y=800*coeff_reduc)

    global label_vies
    label_vies=Label(window,text=("vies:",vie),font=("TkDefaultFont",20),bg="black",fg="#FF001E")
    label_vies.place(x=10*coeff_reduc,y=10*coeff_reduc)

def verif_fin(vie,bombes_trouvees,bombes_posees):
    """ vérifie si le jeu est fini (victoire ou défaite) """
    if vie==0:
        etat='defaite'
        fin_du_jeu(etat)
    if bombes_trouvees==bombes and bombes_posees==bombes:
        etat='victoire'
        fin_du_jeu(etat)

def fin_du_jeu(etat):
    """ crée les différents écrans de fin et tout ce qui doit se passer à la fin du jeu """
    global image_fond_label,d_menu,d_abando,v_menu,v_sauver,chrono,score
    if etat=='defaite':
        try:
            suppr_tout()
            jeu_bouton_menu.destroy()
            label_vies.destroy()
        except:
            pass
        print("Perdu")
        image_fond_label['image']=ecran_defaite
        image_fond_label.place(x=0,y=0,relwidth=1,relheight=1)
        d_abando=Button(window,image=dommage_quitter,bd=0,width=400*coeff_reduc,height=180*coeff_reduc,relief="flat",command=lambda:window.destroy())
        d_abando.place(x=850*coeff_reduc,y=550*coeff_reduc)
        d_menu=Button(window,image=dommage_menu,bd=0,width=400*coeff_reduc,height=180*coeff_reduc,relief="flat",command=lambda:ecran_titre())
        d_menu.place(x=300*coeff_reduc,y=550*coeff_reduc)
    else:
        try:
            suppr_tout()
            jeu_bouton_menu.destroy()
            label_vies.destroy()
        except:
            pass
        print('Bravo')
        chrono=(time_ns()-chrono)
        print(temps_str(temps_chrono(chrono)))
        score=scores(chrono,3)
        score=int(score)
        print(score)

        image_fond_label['image']=ecran_victoire
        image_fond_label.place(x=0,y=0,relwidth=1,relheight=1)
        v_menu=Button(window,image=bravo_menu,bd=0,width=400*coeff_reduc,height=180*coeff_reduc,relief="flat",command=lambda:ecran_titre())
        v_menu.place(x=300*coeff_reduc,y=550*coeff_reduc)
        v_sauver=Button(window,image=bravo_score,bd=0,width=400*coeff_reduc,height=180*coeff_reduc,relief="flat",command=lambda:inserer_db_popup(score,temps_str(temps_chrono(chrono))))
        v_sauver.place(x=850*coeff_reduc,y=550*coeff_reduc)

def aide():
    """ crée une pop-up qui explique comment jouer quand on appuie sur le bouton aide dans les options """
    aide_popup=Toplevel()
    aide_popup.title("Explications")
    aide_popup.configure(bg='black',width=(window.winfo_screenwidth()/2),height=(window.winfo_screenheight()/2))
    aide_popup.iconphoto(False,logo)
    aide_popup.transient(window)
    aide_popup.grab_set()

    principe=Label(aide_popup,text="Le but du jeu est de trouver où sont les bombes.\n Vous pouvez pour cela placer des drapeaux",fg='#FF22FF',bg='black')
    principe.grid(row=0,column=1)
    controle=Label(aide_popup,text="Poser/enlever un drapeau = clic droit. \nOuvrir une case = clic gauche",fg='#22FFFF',bg='black')
    controle.grid(row=0,column=3)

    bouton_cachee=Button(aide_popup,image=case_cachee,bd=0,bg='black',relief="flat")
    bouton_cachee.grid(row=2,column=0)
    txt_bouton_cachee=Label(aide_popup,text="<- Ceci est une case non dévoilée",bg='black',fg='#22FFB6')
    txt_bouton_cachee.grid(row=2,column=1)

    bouton_vide=Button(aide_popup,image=case_vide,bd=0,bg='black',relief="flat")
    bouton_vide.grid(row=3,column=0)
    txt_bouton_vide=Label(aide_popup,text="<- Ceci est une case dévoilée et vide",bg='black',fg='#FFC722')
    txt_bouton_vide.grid(row=3,column=1)

    bouton_drapeau=Button(aide_popup,image=case_drapeau,bd=0,bg='black',relief="flat")
    bouton_drapeau.grid(row=2,column=2)
    txt_bouton_drapeau=Label(aide_popup,text="<- Ceci est une case avec un drapeau",bg='black',fg='#FF229D')
    txt_bouton_drapeau.grid(row=2,column=3)

    bouton_chiffre=Button(aide_popup,image=case8,bd=0,bg='black',relief="flat")
    bouton_chiffre.grid(row=3,column=2)
    txt_bouton_chiffre=Label(aide_popup,text="<- Ceci est une case dévoilée, et indique le \nnombre de bombe autour d'elle (ici, 8)",bg='black',fg='#22E0FF')
    txt_bouton_chiffre.grid(row=3,column=3)

    txt_vies=Label(aide_popup,text="Attention vous avez 3 vies que vous pouvez perdre",bg='black',fg='#FF001E')
    txt_vies.grid(row=4,column=1)

    bouton_bombe=Button(aide_popup,image=case_bombe,bd=0,bg='black',relief="flat")
    bouton_bombe.grid(row=4,column=2)

    txt_vies2=Label(aide_popup,text="<- en tombant sur des bombes",bg='black',fg='#FF001E')
    txt_vies2.grid(row=4,column=3)

def changer_fond():
    """ permet de changer de fond à partir du bouton associé dans les options """
    global fond_en_cours,preview_fond_label
    try:
        preview_fond_label.destroy()
    except:
        pass
    if fond_en_cours==fond1:
        fond_en_cours=fond2
        preview_fond_label=Label(window,image=preview_fond2,width=335*coeff_reduc,height=185*coeff_reduc, bg='black')
        preview_fond_label.place(x=20*coeff_reduc,y=20*coeff_reduc)
    elif fond_en_cours==fond2:
        fond_en_cours=fond3
        preview_fond_label=Label(window,image=preview_fond3,width=335*coeff_reduc,height=185*coeff_reduc, bg='black')
        preview_fond_label.place(x=20*coeff_reduc,y=20*coeff_reduc)
    elif fond_en_cours==fond3:
        fond_en_cours=fond4
        preview_fond_label=Label(window,image=preview_fond4,width=335*coeff_reduc,height=185*coeff_reduc, bg='black')
        preview_fond_label.place(x=20*coeff_reduc,y=20*coeff_reduc)
    elif fond_en_cours==fond4:
        fond_en_cours=fond1
        preview_fond_label=Label(window,image=preview_fond1,width=335*coeff_reduc,height=185*coeff_reduc, bg='black')
        preview_fond_label.place(x=20*coeff_reduc,y=20*coeff_reduc)

def temps_chrono(temps):
    """retourne le temps passé en nano-secondes sous la forme d'un tuple (minutes,secondes,milli-secondes)"""
    ms=0
    s=0
    m=0
    h=0
    if temps >= 1000000:
        ms=int(temps/1000000)
    if ms >= 1000:
        s=int(ms/1000)
        ms=int(ms-(1000*s))
    if s >= 60:
        m=int(s/60)
        s=int(s-(60*m))
    if m >= 60:
        h=int(m/60)
        m=int(m-(60*h))
    temps_final=(m,s,ms)
    return temps_final

def temps_str(temps):
    """ cette fonction transforme l'affichage du temps (sous forme de tuple) en str sous la forme m:s:ms """
    temps=str(temps)
    temps=temps.replace("(","")
    temps=temps.replace(")","")
    temps=temps.replace(" ","")
    temps=temps.replace(",",":")
    return temps

def scores(chrono,nb_vies):
    """cette fonction génère un score en fonction du temps et du nomber de vies perdus"""
    score=(1/sqrt(chrono/10))*exp(2*nb_vies+5)*10**5
    return score

def changer_musique():
    """cette fonction change de musique quand on appuie sur F12 ou sur le bouton dédié à cet effet dans les 
    options"""
    global son_joue
    if son_joue==6:
        PlaySound("mainloop1.wav",SND_ASYNC|SND_LOOP)
        son_joue=1
        print("son = mainloop1")
    elif son_joue==1:
        PlaySound("mainloop2.wav",SND_ASYNC|SND_LOOP)
        son_joue=2
        print("son = mainloop2")
    elif son_joue==2:
        PlaySound("mainloop3.wav",SND_ASYNC|SND_LOOP)
        son_joue=3
        print("son = mainloop3")
    elif son_joue==3:
        PlaySound("mainloop4.wav",SND_ASYNC|SND_LOOP)
        son_joue=4
        print("son = mainloop4")
    elif son_joue==4:
        PlaySound("mainloop5.wav",SND_ASYNC|SND_LOOP)
        son_joue=5
        print("son = mainloop5")
    elif son_joue==5:
        PlaySound("mainloop6.wav",SND_ASYNC|SND_LOOP)
        son_joue=6
        print("son = mainloop6")

def mute():
    global etat_mute
    if etat_mute==False:
        PlaySound("sound_mute.wav",SND_ASYNC|SND_LOOP)
        etat_mute=True
    else:
        changer_musique()
        etat_mute=False

def inserer_db_popup(score,temps):
    """ crée une pop-up qui permet d'insérer un nom pour la db """
    global popup_nom
    popup_nom=Toplevel()
    popup_nom.title("Entrez un nom")
    popup_nom.configure(bg="black")
    popup_nom.iconphoto(False,logo)
    popup_nom.transient(window)
    popup_nom.grab_set()

    temps_affiche=StringVar()
    temps_afficher=Label(popup_nom,textvariable=temps_affiche, bg='black',fg='#0066FF',width=20)
    temps_afficher.pack()
    temps_affiche.set("Vous avez mis " + str(temps))

    vies_affiche=StringVar()
    vies_afficher=Label(popup_nom,textvariable=vies_affiche, bg='black',fg='#FF001E',width=20)
    vies_afficher.pack()
    vies_affiche.set("Il vous restait " + str(vie) + " vies")

    score_affiche=StringVar()
    score_afficher=Label(popup_nom,textvariable=score_affiche, bg='black',fg='#FF00FF',width=20)
    score_afficher.pack()
    score_affiche.set("Votre score est de " + str(score))

    bravo_afficher=Label(popup_nom,text="Bravo ! Entrez votre nom :",bg='black',fg="#FFCC33",width=20)
    bravo_afficher.pack()
    nom=StringVar()
    champ_saisie=Entry(popup_nom,width=20,textvariable=nom)
    champ_saisie.pack(padx=5,pady=5)
    champ_saisie.focus()

    bouton_valider=Button(popup_nom,text="Valider",bd=0,command=lambda:inserer_db(nom.get(),score,temps),fg='#FF00FF')
    bouton_valider.pack()

def inserer_db(nom,score,temps):
    """ permet d'insérer un score dans la db (sous la forme: id, nom, score, temps) """
    try :
        cursor.execute("""
    CREATE TABLE IF NOT EXISTS FACILE (
    id integer primary key autoincrement unique,
    nom TEXT,
    score INT,
    temps TEXT)
    """)
    except :
        pass

    cursor.execute("INSERT INTO FACILE (nom,score,temps) VALUES (?,?,?)",(nom,score,temps))
    db.commit()
    popup_nom.destroy()
    print("données enregistrées")

def suppr_tout():
    """ permet de supprimer toute la grille """
    grille.destroy()

########################################################################################################
######################################### PROGRAMME PRINCIPAL ##########################################
########################################################################################################

# ouverture de la db
db=sqlite3.connect("classement.db")
cursor=db.cursor()

# création de la fenêtre et adaptation de l'écran
window=Tk()

division_resolution=1
resolution=str(int(window.winfo_screenwidth()/division_resolution)), "x", str(int(window.winfo_screenheight()/division_resolution))
resolution=str(resolution)
resolution=resolution.replace(" ","")
resolution=resolution.replace("'","")
resolution=resolution.replace(",","")
resolution=resolution.replace("(","")
resolution=resolution.replace(")","")

window.geometry(resolution)

# gestion du plein écran, F11 pour être en plein écran, Echap pour en sortir
window.attributes("-fullscreen",False)
window.bind("<F11>", lambda event: window.attributes("-fullscreen",not window.attributes("-fullscreen")))
window.bind("<Escape>", lambda event: window.attributes("-fullscreen", False))

# raccourcis clavier pour fermer la fenêtre, le raccourcis est F4
window.bind("<F4>",lambda event: window.destroy())

# définition des images dans le code

coeff_reduc=((window.winfo_screenwidth()/1600)*(window.winfo_screenheight()/900))
coeff_reduc=round(coeff_reduc,2)

##Menu Principal
img_menu_fond_pilar=Image.open('menu_fond.png')
img_menu_fond_pil=img_menu_fond_pilar.resize((window.winfo_screenwidth(),window.winfo_screenheight()))
img_menu_fond=ImageTk.PhotoImage(img_menu_fond_pil)

img_menu_bouton_jouer_pilar=Image.open('menu_bouton_jouer.png')
taille_image=round((img_menu_bouton_jouer_pilar.size[0])*coeff_reduc)
taille_image1=round((img_menu_bouton_jouer_pilar.size[1])*coeff_reduc)
img_menu_bouton_jouer_pil=img_menu_bouton_jouer_pilar.resize((taille_image,taille_image1))
img_menu_bouton_jouer=ImageTk.PhotoImage(img_menu_bouton_jouer_pil)

img_menu_bouton_quitter_pilar=Image.open('menu_bouton_quitter.png')
img_menu_bouton_quitter_pil=img_menu_bouton_quitter_pilar.resize((taille_image,taille_image1))
img_menu_bouton_quitter=ImageTk.PhotoImage(img_menu_bouton_quitter_pil)

img_menu_bouton_classement_pilar=Image.open('menu_bouton_classement.png')
img_menu_bouton_classement_pil=img_menu_bouton_classement_pilar.resize((taille_image,taille_image1))
img_menu_bouton_classement=ImageTk.PhotoImage(img_menu_bouton_classement_pil)

img_menu_bouton_options_pilar=Image.open('menu_bouton_options.png')
img_menu_bouton_options_pil=img_menu_bouton_options_pilar.resize((taille_image,taille_image1))
img_menu_bouton_options=ImageTk.PhotoImage(img_menu_bouton_options_pil)


##Menu des options
img_options_fond_pilar=Image.open("options_fond.png")
img_options_fond_pil=img_options_fond_pilar.resize((window.winfo_screenwidth(),window.winfo_screenheight()))
img_options_fond=ImageTk.PhotoImage(img_options_fond_pil)

img_options_bouton_aide_pilar=Image.open('options_bouton_aide.png')
img_options_bouton_aide_pil=img_options_bouton_aide_pilar.resize((taille_image,taille_image1))
img_options_bouton_aide=ImageTk.PhotoImage(img_options_bouton_aide_pil)

img_options_bouton_fond_pilar=Image.open('options_bouton_fond.png')
img_options_bouton_fond_pil=img_options_bouton_fond_pilar.resize((taille_image,taille_image1))
img_options_bouton_fond=ImageTk.PhotoImage(img_options_bouton_fond_pil)

img_options_bouton_menu_pilar=Image.open('options_bouton_menu.png')
img_options_bouton_menu_pil=img_options_bouton_menu_pilar.resize((taille_image,taille_image1))
img_options_bouton_menu=ImageTk.PhotoImage(img_options_bouton_menu_pil)

img_options_bouton_musique_pilar=Image.open('options_bouton_musique.png')
img_options_bouton_musique_pil=img_options_bouton_musique_pilar.resize((taille_image,taille_image1))
img_options_bouton_musique=ImageTk.PhotoImage(img_options_bouton_musique_pil)

##Menu des classements
classement_fond_pilar=Image.open("classement_fond.png")
classement_fond_pil=classement_fond_pilar.resize((window.winfo_screenwidth(),window.winfo_screenheight()))
classement_fond=ImageTk.PhotoImage(classement_fond_pil)


##Menu des difficultés
difficultes_fond_pilar=Image.open("difficultes_fond.png")
difficultes_fond_pil=difficultes_fond_pilar.resize((window.winfo_screenwidth(),window.winfo_screenheight()))
difficultes_fond=ImageTk.PhotoImage(difficultes_fond_pil)

difficultes_bouton_facile_pilar=Image.open('difficultes_bouton_facile.png')
difficultes_bouton_facile_pil=difficultes_bouton_facile_pilar.resize((taille_image,taille_image1))
difficultes_bouton_facile=ImageTk.PhotoImage(difficultes_bouton_facile_pil)

difficultes_bouton_moyen_pilar=Image.open('difficultes_bouton_moyen.png')
difficultes_bouton_moyen_pil=difficultes_bouton_moyen_pilar.resize((taille_image,taille_image1))
difficultes_bouton_moyen=ImageTk.PhotoImage(difficultes_bouton_moyen_pil)

difficultes_bouton_difficile_pilar=Image.open('difficultes_bouton_difficile.png')
difficultes_bouton_difficile_pil=difficultes_bouton_difficile_pilar.resize((taille_image,taille_image1))
difficultes_bouton_difficile=ImageTk.PhotoImage(difficultes_bouton_difficile_pil)

difficultes_bouton_menu_pilar=Image.open('difficultes_bouton_menu.png')
difficultes_bouton_menu_pil=difficultes_bouton_menu_pilar.resize((taille_image,taille_image1))
difficultes_bouton_menu=ImageTk.PhotoImage(difficultes_bouton_menu_pil)


##Écran de défaite
ecran_defaite_pilar=Image.open("dommage_fond.png")
ecran_defaite_pil=ecran_defaite_pilar.resize((window.winfo_screenwidth(),window.winfo_screenheight()))
ecran_defaite=ImageTk.PhotoImage(ecran_defaite_pil)

dommage_bouton_menu_pilar=Image.open('dommage_bouton_menu.png')
dommage_bouton_menu_pil=dommage_bouton_menu_pilar.resize((taille_image,taille_image1))
dommage_menu=ImageTk.PhotoImage(dommage_bouton_menu_pil)

dommage_bouton_quitter_pilar=Image.open('dommage_bouton_quitter.png')
dommage_bouton_quitter_pil=dommage_bouton_quitter_pilar.resize((taille_image,taille_image1))
dommage_quitter=ImageTk.PhotoImage(dommage_bouton_quitter_pil)


##Écran de victoire
ecran_victoire_pilar=Image.open("bravo_fond.png")
ecran_victoire_pil=ecran_victoire_pilar.resize((window.winfo_screenwidth(),window.winfo_screenheight()))
ecran_victoire=ImageTk.PhotoImage(ecran_victoire_pil)

bravo_bouton_menu_pilar=Image.open('bravo_bouton_menu.png')
bravo_bouton_menu_pil=bravo_bouton_menu_pilar.resize((taille_image,taille_image1))
bravo_menu=ImageTk.PhotoImage(bravo_bouton_menu_pil)

bravo_bouton_sauvegarder_score_pilar=Image.open('bravo_bouton_sauvegarder_score.png')
bravo_bouton_sauvegarder_score_pil=bravo_bouton_sauvegarder_score_pilar.resize((taille_image,taille_image1))
bravo_score=ImageTk.PhotoImage(bravo_bouton_sauvegarder_score_pil)


##Images en cours cours de jeu
case_bombe_pilar=Image.open("case_bombe.png")
taille_image=round((case_bombe_pilar.size[0])*coeff_reduc)
case_bombe_pil=case_bombe_pilar.resize(( taille_image,taille_image ))
case_bombe=ImageTk.PhotoImage(case_bombe_pil)

case_cachee_pilar=Image.open("case_cachee.png")
case_cachee_pil=case_cachee_pilar.resize(( taille_image,taille_image ))
case_cachee=ImageTk.PhotoImage(case_cachee_pil)

case_drapeau_pilar=Image.open("case_drapeau.png")
case_drapeau_pil=case_drapeau_pilar.resize(( taille_image,taille_image ))
case_drapeau=ImageTk.PhotoImage(case_drapeau_pil)

case_vide_pilar=Image.open("case_vide.png")
case_vide_pil=case_vide_pilar.resize(( taille_image,taille_image ))
case_vide=ImageTk.PhotoImage(case_vide_pil)

case1_pilar=Image.open("case1.png")
case1_pil=case1_pilar.resize(( taille_image,taille_image ))
case1=ImageTk.PhotoImage(case1_pil)

case2_pilar=Image.open("case2.png")
case2_pil=case2_pilar.resize(( taille_image,taille_image ))
case2=ImageTk.PhotoImage(case2_pil)

case3_pilar=Image.open("case3.png")
case3_pil=case3_pilar.resize(( taille_image,taille_image ))
case3=ImageTk.PhotoImage(case3_pil)

case4_pilar=Image.open("case4.png")
case4_pil=case4_pilar.resize(( taille_image,taille_image ))
case4=ImageTk.PhotoImage(case4_pil)

case5_pilar=Image.open("case5.png")
case5_pil=case5_pilar.resize(( taille_image,taille_image ))
case5=ImageTk.PhotoImage(case5_pil)

case6_pilar=Image.open("case6.png")
case6_pil=case6_pilar.resize(( taille_image,taille_image ))
case6=ImageTk.PhotoImage(case6_pil)

case7_pilar=Image.open("case7.png")
case7_pil=case7_pilar.resize(( taille_image,taille_image ))
case7=ImageTk.PhotoImage(case7_pil)

case8_pilar=Image.open("case8.png")
case8_pil=case8_pilar.resize(( taille_image,taille_image ))
case8=ImageTk.PhotoImage(case8_pil)

img_jeu_bouton_menu_pilar=Image.open('options_bouton_menu.png')
img_jeu_bouton_menu_pil=img_jeu_bouton_menu_pilar.resize((200,90))
img_jeu_bouton_menu=ImageTk.PhotoImage(img_jeu_bouton_menu_pil)

##Fonds + logo
fond1_pilar=Image.open("fond1.png")
fond1_pil=fond1_pilar.resize((window.winfo_screenwidth(),window.winfo_screenheight()))
fond1=ImageTk.PhotoImage(fond1_pil)

fond2_pilar=Image.open("fond2.png")
fond2_pil=fond2_pilar.resize((window.winfo_screenwidth(),window.winfo_screenheight()))
fond2=ImageTk.PhotoImage(fond2_pil)

fond3_pilar=Image.open("fond3.png")
fond3_pil=fond3_pilar.resize((window.winfo_screenwidth(),window.winfo_screenheight()))
fond3=ImageTk.PhotoImage(fond3_pil)

fond4_pilar=Image.open("fond4.png")
fond4_pil=fond4_pilar.resize((window.winfo_screenwidth(),window.winfo_screenheight()))
fond4=ImageTk.PhotoImage(fond4_pil)

logo=PhotoImage(file="logo_cyberdemineur.png")

## Image de preview
taille_preview1=round((window.winfo_screenwidth()//4)*coeff_reduc)
taille_preview2=round((window.winfo_screenheight()//4)*coeff_reduc)
preview_fond_pilar=Image.open('fond1.png')
preview_fond_pil=preview_fond_pilar.resize((taille_preview1,taille_preview2))
preview_fond1=ImageTk.PhotoImage(preview_fond_pil)

preview_fond_pilar=Image.open('fond2.png')
preview_fond_pil=preview_fond_pilar.resize((taille_preview1,taille_preview2))
preview_fond2=ImageTk.PhotoImage(preview_fond_pil)

preview_fond_pilar=Image.open('fond3.png')
preview_fond_pil=preview_fond_pilar.resize((taille_preview1,taille_preview2))
preview_fond3=ImageTk.PhotoImage(preview_fond_pil)

preview_fond_pilar=Image.open('fond4.png')
preview_fond_pil=preview_fond_pilar.resize((taille_preview1,taille_preview2))
preview_fond4=ImageTk.PhotoImage(preview_fond_pil)
# définition de l'image de fond
image_fond_label=Label(window, image=img_menu_fond)
image_fond_label.place(x=0,y=0,relwidth=1,relheight=1)

window.configure(bg="black")
window.iconphoto(False,logo)
window.title("Cyber démineur")

fond_en_cours=fond4


ecran_titre()

# lecture des musiques
son_joue=1
changer_musique()
window.bind("<F12>",lambda event:changer_musique())
etat_mute=False


window.mainloop()


# fermeture de la db
cursor.close()
db.close()