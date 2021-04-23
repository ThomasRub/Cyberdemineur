<<<<<<< HEAD
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

""" Notes pour plus tard:
        - http://tkinter.fdex.eu/doc/uwm.html """

from random import randint
from tkinter import*
from time import time_ns,sleep
from math import sqrt,exp
from winsound import PlaySound,SND_ASYNC,SND_LOOP

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
                self.grille_label[i][j] = Label(grille,bd=1,justify=CENTER,relief="flat",image=self.image_label,width=self.taille_label,height=self.taille_label)
                self.grille_label[i][j].grid(column=j,row=i)
                self.grille_button[i][j] = Button(grille,width=self.taille_case,height=self.taille_case,image=case_cachee,relief='flat')
                self.grille_button[i][j].grid(column=j,row=i)
                self.grille_button[i][j].bind("<Button-3>",lambda i,x=i,y=j: self.afficheFlag(x,y))
                self.grille_button[i][j].bind("<Button-1>",lambda i,x=i,y=j: self.click(x,y))

    def affiche_valeurs(self,ligne,colonne):
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
                global vie
                vie-=1
                global bombes_trouvees
                bombes_trouvees+=1
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
        

        while self.premier_clic==False and self.grille[ligne][colonne][0] == 9:
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
        
        verif_fin(vie,bombes_trouvees)

    def afficheFlag(self,ligne,colonne):
        """Méthode qui modifie l'image du bouton pour afficher un drapeau. Le joueur ne peut ainsi plus dévoiler
        la case, à moins d'enlever le drapeau.
        Ajouter/Enlever un drapeau se fait par clic droit"""
        if not self.grille[ligne][colonne][1]==2:
            self.grille[ligne][colonne][1]=2
            self.grille_button[ligne][colonne]['image']=case_drapeau
            if self.grille[ligne][colonne][0]==9:
                global bombes_trouvees
                bombes_trouvees+=1
                verif_fin(vie,bombes_trouvees)
        elif self.grille[ligne][colonne][1]==2:
            self.grille[ligne][colonne][1]=0
            self.grille_button[ligne][colonne]['image']=case_cachee
            if self.grille[ligne][colonne][0]==9:
                bombes_trouvees-=1
                return bombes_trouvees

########################################################################################################
######################################### FONCTIONS ####################################################
########################################################################################################

def ecran_titre():
    try:
        image_fond_label['image']=menu_fond
        ecrant.destroy()
        abando.destroy()
    except:
        pass
    global Jouer,Quitter,Classement,Options
    Jouer=Button(window,image=jouer,width=450,height=203,command=lambda:menu_jouer())
    Jouer.place(x=300,y=300)

    Quitter=Button(window,image=quitter,width=450,height=203,command=lambda:window.destroy())
    Quitter.place(x=300,y=550)

    Classement=Button(window,image=classement,width=450,height=203)
    Classement.place(x=950,y=300)

    Options=Button(window,image=options,width=450,height=203)
    Options.place(x=950,y=550)

def menu_jouer():
    Jouer.destroy()
    Quitter.destroy()
    Classement.destroy()
    Options.destroy()

    debut_facile()

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
    global l,c,bombes,vie,premier_clic,nbmax,casehaut,casebas,bombes_trouvees   #Toutes ces variables sont utilisés au sein du code
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
    
    debut_de_partie()
    chrono=time_ns()

def debut_normal():
    """Début de la partie en difficulté normal. On initialise le chrono, et génère la grille 
    (en donnant l = nombre de lignes, c = nombre de colonne, bombes = nombre de bombes, vie = le nombre de vie)
    """
    global l,c,bombes,vie,nbmax,casehaut,casebas,bombes_trouvees   #Toutes ces variables sont utilisés au sein du code
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
    
    debut_de_partie()
    chrono=time_ns()

def debut_difficile():
    """Début de la partie en difficulté maximale. On initialise le chrono, et génère la grille 
    (en donnant l = nombre de lignes, c = nombre de colonne, bombes = nombre de bombes, vie = le nombre de vie)
    """
    global l,c,bombes,vie,premier_clic,nbmax,casehaut,casebas,bombes_trouvees   #Toutes ces variables sont utilisés au sein du code
    l=13
    c=22
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
    try:
        global image_fond_label

        image_fond_label=Label(window, image=fond4)
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

    gr=Grille(grille_console,58,62)
    gr.generer_boutons()

def verif_fin(vie,bombes_trouvees):
    if vie==0:
        etat='defaite'
        fin_du_jeu(etat)
    if bombes_trouvees==bombes:
        etat='victoire'
        fin_du_jeu(etat)

def fin_du_jeu(etat):
    global image_fond_label,ecrant,rejouer,abando
    if etat=='defaite':
        suppr_tout()
        print("Perdu")
        image_fond_label['image']=ecran_defaite
        image_fond_label.place(x=0,y=0,relwidth=1,relheight=1)
        abando=Button(window, text='Abandonner ?',command=lambda:window.destroy(),height=7,width=15)
        abando.place(x=950,y=300)
        ecrant=Button(window,text='Retours à l\'écran-titre ?',command=lambda:ecran_titre())
        ecrant.place(x=950,y=550)
    else:
        print('Bravo')
        suppr_tout()
        image_fond_label['image']=ecran_victoire
        image_fond_label.place(x=0,y=0,relwidth=1,relheight=1)

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

def score(chrono,nb_vies):
    """cette fonction génère un score en fonction du temps et du nomber de vies perdus"""
    score=(1/sqrt(chrono/10))*exp(2*nb_vies+5)*10**5
    return score

def musique(son):
    """cette fonction change de musique quand on appuie sur F12
    utilisée pour le développement"""
    window.bind("<F12>",lambda event:musique(son))
    if son==0:
        PlaySound("loop_menu_cyberdemineur.wav",SND_ASYNC|SND_LOOP)
        son=1
    elif son==1:
        PlaySound("mainloop_cyberdemineur.wav",SND_ASYNC|SND_LOOP)
        son=0

def suppr_tout():
    grille.destroy()

########################################################################################################
######################################### PROGRAMME PRINCIPAL ##########################################
########################################################################################################

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
jouer=PhotoImage(file="menu_jouer.png")
menu_fond=PhotoImage(file='menu_fond.png')
quitter=PhotoImage(file="menu_quitter.png")
classement=PhotoImage(file="menu_classement.png")
options=PhotoImage(file="menu_options.png")

case_bombe=PhotoImage(file="case_bombe.png")
case_cachee=PhotoImage(file="case_cachee.png")
case_drapeau=PhotoImage(file="case_drapeau.png")
case_vide=PhotoImage(file="case_vide.png")
case1=PhotoImage(file="case1.png")
case2=PhotoImage(file="case2.png")
case3=PhotoImage(file="case3.png")
case4=PhotoImage(file="case4.png")
case5=PhotoImage(file="case5.png")
case6=PhotoImage(file="case6.png")
case7=PhotoImage(file="case7.png")
case8=PhotoImage(file="case8.png")
fond4=PhotoImage(file="fond3.png")
ecran_victoire=PhotoImage(file="ecran_victoire4.png")
ecran_defaite=PhotoImage(file="ecran_defaite.png")
logo=PhotoImage(file="logo_cyberdemineur.png")

# définition de l'image de fond
image_fond_label=Label(window, image=menu_fond)
image_fond_label.place(x=0,y=0,relwidth=1,relheight=1)

window.configure(bg="black")
window.iconphoto(False,logo)
window.title("Cyber démineur")


ecran_titre()

# lecture des musiques
son_joue=0
musique(son_joue)

window.mainloop()

# fin du chrono, affichage du temps et du score dans la console
# (temporaire)
"""chrono=(time_ns()-chrono)

print(temps_chrono(chrono))
print(int(score(chrono,3)))"""
=======
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

""" Notes pour plus tard:
        - http://tkinter.fdex.eu/doc/uwm.html """

from random import randint
from tkinter import*
from time import time_ns,sleep
from math import sqrt,exp
from winsound import PlaySound,SND_ASYNC,SND_LOOP
import sqlite3

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
                self.grille_label[i][j] = Label(grille,bd=1,justify=CENTER,relief="flat",image=self.image_label,width=self.taille_label,height=self.taille_label)
                self.grille_label[i][j].grid(column=j,row=i)
                self.grille_button[i][j] = Button(grille,width=self.taille_case,height=self.taille_case,image=case_cachee,relief='flat')
                self.grille_button[i][j].grid(column=j,row=i)
                self.grille_button[i][j].bind("<Button-3>",lambda i,x=i,y=j: self.afficheFlag(x,y))
                self.grille_button[i][j].bind("<Button-1>",lambda i,x=i,y=j: self.click(x,y))

    def affiche_valeurs(self,ligne,colonne):
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
                global vie
                vie-=1
                global bombes_trouvees
                bombes_trouvees+=1
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
        
        verif_fin(vie,bombes_trouvees)

    def afficheFlag(self,ligne,colonne):
        """Méthode qui modifie l'image du bouton pour afficher un drapeau. Le joueur ne peut ainsi plus dévoiler
        la case, à moins d'enlever le drapeau.
        Ajouter/Enlever un drapeau se fait par clic droit"""
        if not self.grille[ligne][colonne][1]==2:
            self.grille[ligne][colonne][1]=2
            self.grille_button[ligne][colonne]['image']=case_drapeau
            if self.grille[ligne][colonne][0]==9:
                global bombes_trouvees
                bombes_trouvees+=1
                verif_fin(vie,bombes_trouvees)
        elif self.grille[ligne][colonne][1]==2:
            self.grille[ligne][colonne][1]=0
            self.grille_button[ligne][colonne]['image']=case_cachee
            if self.grille[ligne][colonne][0]==9:
                bombes_trouvees-=1
                return bombes_trouvees

########################################################################################################
######################################### FONCTIONS ####################################################
########################################################################################################

def ecran_titre():
    try:
        image_fond_label['image']=menu_fond
        d_menu.destroy()
        d_abando.destroy()
    except:
        pass
    try:
        image_fond_label['image']=menu_fond
        v_menu.destroy()
        v_sauver.destroy()
    except:
        pass
    global menu_jouer,menu_quitter,menu_classement,menu_options
    menu_jouer=Button(window,image=jouer,width=450,height=203,command=lambda:ecran_difficultes())
    menu_jouer.place(x=300,y=300)

    menu_quitter=Button(window,image=quitter,width=450,height=203,command=lambda:window.destroy())
    menu_quitter.place(x=300,y=550)

    menu_classement=Button(window,image=classement,width=450,height=203,command=lambda:ecran_classement())
    menu_classement.place(x=950,y=300)

    menu_options=Button(window,image=options,width=450,height=203,command=lambda:ecran_options())
    menu_options.place(x=950,y=550)

def ecran_classement():
    try:
        image_fond_label['image']=classement_fond
        menu_jouer.destroy()
        menu_quitter.destroy()
        menu_classement.destroy()
        menu_options.destroy()
    except:
        pass

def ecran_difficultes():
    try:
        image_fond_label['image']=difficultes_fond
        menu_jouer.destroy()
        menu_quitter.destroy()
        menu_classement.destroy()
        menu_options.destroy()
    except:
        pass
    global difficulte_facile,difficulte_moyen,difficulte_difficile
    difficulte_facile=Button(window,image=difficultes_bouton_facile,width=450,height=203,command=lambda:debut_facile())
    difficulte_facile.place(x=300,y=300)

    difficulte_moyen=Button(window,image=difficultes_bouton_moyen,width=450,height=203,command=lambda:debut_normal())
    difficulte_moyen.place(x=300,y=550)

    difficulte_difficile=Button(window,image=difficultes_bouton_difficile,width=450,height=203,command=lambda:debut_difficile())
    difficulte_difficile.place(x=950,y=300)

def ecran_options():
    try:
        image_fond_label['image']=options_fond
        menu_jouer.destroy()
        menu_quitter.destroy()
        menu_classement.destroy()
        menu_options.destroy()
    except:
        pass

def menu_jouer():
    menu_jouer.destroy()
    menu_quitter.destroy()
    menu_classement.destroy()
    menu_options.destroy()

    debut_facile()

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
    global l,c,bombes,vie,premier_clic,nbmax,casehaut,casebas,bombes_trouvees   #Toutes ces variables sont utilisés au sein du code
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
    global l,c,bombes,vie,nbmax,casehaut,casebas,bombes_trouvees   #Toutes ces variables sont utilisés au sein du code
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
    global l,c,bombes,vie,premier_clic,nbmax,casehaut,casebas,bombes_trouvees   #Toutes ces variables sont utilisés au sein du code
    l=13
    c=22
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
    try:
        global image_fond_label

        image_fond_label=Label(window, image=fond4)
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

    gr=Grille(grille_console,58,62)
    gr.generer_boutons()

def verif_fin(vie,bombes_trouvees):
    if vie==0:
        etat='defaite'
        fin_du_jeu(etat)
    if bombes_trouvees==bombes:
        etat='victoire'
        fin_du_jeu(etat)

def fin_du_jeu(etat):
    global image_fond_label,ecrant,d_menu,d_abando,v_menu,v_sauver
    if etat=='defaite':
        suppr_tout()
        print("Perdu")
        image_fond_label['image']=ecran_defaite
        image_fond_label.place(x=0,y=0,relwidth=1,relheight=1)
        d_abando=Button(window, text='Abandonner ?',command=lambda:window.destroy())
        d_abando.place(x=850,y=300)
        d_menu=Button(window,image=dommage_menu,command=lambda:ecran_titre())
        d_menu.place(x=850,y=550)
    else:
        suppr_tout()
        print('Bravo')
        image_fond_label['image']=ecran_victoire
        image_fond_label.place(x=0,y=0,relwidth=1,relheight=1)
        v_menu=Button(window,image=bravo_menu,command=lambda:ecran_titre())
        v_menu.place(x=850,y=300)
        v_sauver=Button(window,image=bravo_score)
        v_sauver.place(x=850,y=550)

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

def score(chrono,nb_vies):
    """cette fonction génère un score en fonction du temps et du nomber de vies perdus"""
    score=(1/sqrt(chrono/10))*exp(2*nb_vies+5)*10**5
    return score

def musique(son):
    """cette fonction change de musique quand on appuie sur F12
    utilisée pour le développement"""
    window.bind("<F12>",lambda event:musique(son))
    if son==0:
        PlaySound("loop_menu_cyberdemineur.wav",SND_ASYNC|SND_LOOP)
        son=1
    elif son==1:
        PlaySound("mainloop_cyberdemineur.wav",SND_ASYNC|SND_LOOP)
        son=0

def inserer_db(score,temps):
    inserer="SELECT * FROM FACILE"      # insérer du code SQL entre les " "
    cursor.execute(inserer)

def suppr_tout():
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
jouer=PhotoImage(file="menu_bouton_jouer.png")
menu_fond=PhotoImage(file='menu_fond.png')
quitter=PhotoImage(file="menu_bouton_quitter.png")
classement=PhotoImage(file="menu_bouton_classement.png")
options=PhotoImage(file="menu_bouton_options.png")

options_fond=PhotoImage(file="options_fond.png")

classement_fond=PhotoImage(file="classement_fond.png")

difficultes_fond=PhotoImage(file="difficultes_fond.png")
difficultes_bouton_facile=PhotoImage(file="difficultes_bouton_facile.png")
difficultes_bouton_moyen=PhotoImage(file="difficultes_bouton_moyen.png")
difficultes_bouton_difficile=PhotoImage(file="difficultes_bouton_difficile.png")

ecran_defaite=PhotoImage(file="dommage_fond.png")
dommage_menu=PhotoImage(file="dommage_bouton_menu.png")

ecran_victoire=PhotoImage(file="bravo_fond.png")
bravo_menu=PhotoImage(file="bravo_bouton_menu.png")
bravo_score=PhotoImage(file="bravo_bouton_sauvegarder_score.png")

case_bombe=PhotoImage(file="case_bombe.png")
case_cachee=PhotoImage(file="case_cachee.png")
case_drapeau=PhotoImage(file="case_drapeau.png")
case_vide=PhotoImage(file="case_vide.png")
case1=PhotoImage(file="case1.png")
case2=PhotoImage(file="case2.png")
case3=PhotoImage(file="case3.png")
case4=PhotoImage(file="case4.png")
case5=PhotoImage(file="case5.png")
case6=PhotoImage(file="case6.png")
case7=PhotoImage(file="case7.png")
case8=PhotoImage(file="case8.png")
fond4=PhotoImage(file="fond4.png")

logo=PhotoImage(file="logo_cyberdemineur.png")

# définition de l'image de fond
image_fond_label=Label(window, image=menu_fond)
image_fond_label.place(x=0,y=0,relwidth=1,relheight=1)

window.configure(bg="black")
window.iconphoto(False,logo)
window.title("Cyber démineur")


ecran_titre()

# lecture des musiques
son_joue=0
musique(son_joue)

window.mainloop()

# fin du chrono, affichage du temps et du score dans la console
# (temporaire)
"""chrono=(time_ns()-chrono)

print(temps_chrono(chrono))
print(int(score(chrono,3)))"""

# fermeture de la db
cursor.close()
db.close()
>>>>>>> cbade5a0cc3cf57de90235e19b1524503dee7fbc
