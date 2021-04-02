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
    Modules:
        - audioloop
        - wave 
    Sites:
        - https://askcodez.com/la-grille-a-linterieur-dun-cadre.html"""

from random import*
from tkinter import*
from time import time_ns
from math import*

########################################################################################################
######################################### CLASSES ######################################################
########################################################################################################

class Bouton:
    def __init__(self,grille,taille_case,taille_label):
        self.grille=grille
        self.image_label=case_vide
        self.taille_label=taille_label
        self.taille_case=taille_case

    def generer_boutons(self):
        """Méthode qui génère les boutons. Elle génère également la "grille de fond" qui affiche les valeurs des cases au joueur.
        Les boutons ont deux actions : clic gauche, qui dévoile la case; et clic droit, qui pose un drapeau."""
        a=0

        for i in range(c):
            for j in range(l):
                labels.append(Label(grille,bd=1,justify=CENTER,relief="flat",image=self.image_label,width=self.taille_label,height=self.taille_label))
                labels[a].grid(column=i,row=j)

                b.append(Button(grille,width=self.taille_case,height=self.taille_case,image=case_cachee,relief='flat'))
                b[a].grid(column=i,row=j)
                b[a].bind("<Button-3>",lambda i,ref=a: self.afficheFlag(ref))
                b[a].bind("<Button-1>",lambda i,ref=a: self.click(ref,premier_clic))
                a+=1

    def click(self,ref,premier_clic):
        """Méthode qui dévoile la case si le bouton est cliqué (via le clic gauche). Elle efface le bouton, 
        et modifie la case de la grille sous le bouton pour que la bonne valeur soit affichée. 
        Elle prends aussi en charge de dévoiler les cases adjacentes à une case vide (diagonale non prise en charge)"""
        info = b[ref].grid_info()
        colonne=(info["column"])
        ligne=(info["row"])

        #if premier_clic==False and self.grille[ligne][colonne][0] >=9:
        #    self.image_label=case_bombe
        #    b[ref].grid_remove()
        #    b[ref].grid_remove()
        #    print(premier_clic,"debut")
        #    premier_clic=True
        #    print(premier_clic,"df")
        #    return premier_clic

        # Changement de la case 0. Cette partie gère également la découverte auto des cases adjacentes
        if self.grille[ligne][colonne][0] == 0 and self.grille[ligne][colonne][1] == 0:
            premier_clic=True
            labels[ref]['image']=case_vide
            b[ref].grid_remove()
            gau=ref-l
            droi=ref+l
            haut=ref
            bas=ref

            try :
                if gau>=0 :
                    self.click(gau,premier_clic)
            except KeyError : pass
            try :
                if droi<=nbmax:
                    self.click(droi,premier_clic)
            except KeyError : pass
            try:
                if haut not in casehaut:
                    self.click(haut-1,premier_clic)
            except KeyError : pass
            try:
                if bas not in casebas:
                    self.click(bas+1,premier_clic)
            except KeyError : pass
            self.image_label=case_vide

        # Changements des cases 1 à 8 + bombes lorsque cliqué (beaucoup de cas à gérer )
        elif self.grille[ligne][colonne][0] == 1 and self.grille[ligne][colonne][1] == 0:
            self.image_label=case1
            labels[ref]['image']=self.image_label
            b[ref].grid_remove()
        elif self.grille[ligne][colonne][0] == 2 and self.grille[ligne][colonne][1] == 0:
            self.image_label=case2
            labels[ref]['image']=self.image_label
            b[ref].grid_remove()
        elif self.grille[ligne][colonne][0] == 3 and self.grille[ligne][colonne][1] == 0:
            self.image_label=case3
            labels[ref]['image']=self.image_label
            b[ref].grid_remove()
        elif self.grille[ligne][colonne][0] == 4 and self.grille[ligne][colonne][1] == 0:
            self.image_label=case4
            labels[ref]['image']=self.image_label
            b[ref].grid_remove()
        elif self.grille[ligne][colonne][0] == 5 and self.grille[ligne][colonne][1] == 0:
            self.image_label=case5
            labels[ref]['image']=self.image_label
            b[ref].grid_remove()
        elif self.grille[ligne][colonne][0] == 6 and self.grille[ligne][colonne][1] == 0:
            self.image_label=case6
            labels[ref]['image']=self.image_label
            b[ref].grid_remove()
        elif self.grille[ligne][colonne][0] == 7 and self.grille[ligne][colonne][1] == 0:
            self.image_label=case7
            labels[ref]['image']=self.image_label
            b[ref].grid_remove()
        elif self.grille[ligne][colonne][0] == 8 and self.grille[ligne][colonne][1] == 0:
            self.image_label=case8
            labels[ref]['image']=self.image_label
            b[ref].grid_remove()
        elif self.grille[ligne][colonne][0]>=9 and self.grille[ligne][colonne][1] == 0:
            self.image_label=case_bombe
            labels[ref]['image']=self.image_label
            global bombes_trouvees
            bombes_trouvees+=1
            global vie
            vie-=1
            b[ref].grid_remove()
            b[ref].grid_remove()
        premier_clic=True
        verif_fin(vie,bombes_trouvees)

    def afficheFlag(self,ref):
        """Méthode qui modifie l'image du bouton pour afficher un drapeau. Le joueur ne peut ainsi plus dévoiler 
        la case, à moins d'enlever le drapeau.
        Ajouter/Enlever un drapeau se fait par clic droit"""
        info = b[ref].grid_info()
        colonne=(info["column"])
        ligne=(info["row"])
        if not self.grille[ligne][colonne][1]==2:
            self.grille[ligne][colonne][1]=2
            b[ref]['image']=case_drapeau
            if self.grille[ligne][colonne][0]>=9:
                global bombes_trouvees
                bombes_trouvees+=1
                verif_fin(vie,bombes_trouvees)
        else:
            self.grille[ligne][colonne][1]=0
            b[ref]['image']=case_cachee
            if self.grille[ligne][colonne][0]>=9:
                bombes_trouvees-=1
                return bombes_trouvees


########################################################################################################
######################################### FONCTIONS ####################################################
########################################################################################################

def grille_vide(c,l):
    """Permet de générer une grille vide(grille console)
    c: le nombre de colones
    l: nombre de lignes"""
    grille=[]
    for i in range (c):
        grille.append([[0,0]]*l)
    return grille

def affiche_grille_console(grille,c):
    """Permet d'afficher la grille dans la console
    Utilisée pour le développement
    grille: nom de la grille
    c: nombre de colones de la grille"""
    for i in range(c):
        print(grille[i])

def generer_bombes(grille,nb_bombes,c,l):
    """ Fonction qui génère des bombes placées aléatoirement dans la grille(grille console).
    Elle prend en compte le fait qu'une case ait déjà une bombe
    Puis elle génère les nombres autour des bombes en prenant en compte les cas spéciaux
    grille: nom de la grille
    nb_bombes: nombre de bombes à placer
    c: nombre de colones
    l: nombre de lignes
    """
    bombes_places=0
    while bombes_places != nb_bombes:                      #Génère les bombes aléatoirement
        x = randint(0,c-1)
        y = randint(0,l-1)
        if grille[x][y][0]!=9:
            z =grille[x][y][1]
            grille[x][y]=[9,z]
            bombes_places+=1
                                                            #On place les chiffres autour des bombes (mais il y a des cas spéciaux...)

            if (x==0 and y==0):                             #Cas spécial n°1 : en haut de la grille tout à gauche
                z = grille[x+1][y][1]
                a = grille[x+1][y][0]
                a+=1
                grille[x+1][y]=[a,z]

                z = grille[x+1][y+1][1]
                a = grille[x+1][y+1][0]
                a+=1
                grille[x+1][y+1]=[a,z]

                z = grille[x][y+1][1]
                a = grille[x][y+1][0]
                a+=1
                grille[x][y+1]=[a,z]

            elif (x==0 and y==(c-1)):                         #Cas n°2: en haut de la grille, tout à droite
                z = grille[x][y-1][1]
                a = grille[x][y-1][0]
                a+=1
                grille[x][y-1]=[a,z]

                z = grille[x+1][y-1][1]
                a = grille[x+1][y-1][0]
                a+=1
                grille[x+1][y-1]=[a,z]

                z = grille[x+1][y][1]
                a = grille[x+1][y][0]
                a+=1
                grille[x+1][y]=[a,z]

            elif (x==0 and (y!=0 or y!=(c-1))):              #Cas n°3 : en haut de la grille, ni à gauche, ni à droite
                z = grille[x][y-1][1]
                a = grille[x][y-1][0]
                a+=1
                grille[x][y-1]=[a,z]

                z = grille[x+1][y-1][1]
                a = grille[x+1][y-1][0]
                a+=1
                grille[x+1][y-1]=[a,z]

                z = grille[x+1][y][1]
                a = grille[x+1][y][0]
                a+=1
                grille[x+1][y]=[a,z]

                z = grille[x+1][y+1][1]
                a = grille[x+1][y+1][0]
                a+=1
                grille[x+1][y+1]=[a,z]

                z = grille[x][y+1][1]
                a = grille[x][y+1][0]
                a+=1
                grille[x][y+1]=[a,z]

            elif (x==(l-1) and y==0):                       #Cas n°4 : Tout en bas, à gauche
                z = grille[x-1][y][1]
                a = grille[x-1][y][0]
                a+=1
                grille[x-1][y]=[a,z]

                z = grille[x-1][y+1][1]
                a = grille[x-1][y+1][0]
                a+=1
                grille[x-1][y+1]=[a,z]

                z = grille[x][y+1][1]
                a = grille[x][y+1][0]
                a+=1
                grille[x][y+1]=[a,z]

            elif (x==(l-1) and y==(c-1)):                   #Cas n°5 : Tout en bas, à droite
                z = grille[x-1][y][1]
                a = grille[x-1][y][0]
                a+=1
                grille[x-1][y]=[a,z]

                z = grille[x-1][y-1][1]
                a = grille[x-1][y-1][0]
                a+=1
                grille[x-1][y-1]=[a,z]

                z = grille[x][y-1][1]
                a = grille[x][y-1][0]
                a+=1
                grille[x][y-1]=[a,z]

            elif (x==(l-1) and (y!=0 or y!=(c-1))):         #Cas n°6 : Tout en bas, ni à droite, ni à gauche
                z = grille[x][y-1][1]
                a = grille[x][y-1][0]
                a+=1
                grille[x][y-1]=[a,z]

                z = grille[x-1][y-1][1]
                a = grille[x-1][y-1][0]
                a+=1
                grille[x-1][y-1]=[a,z]

                z = grille[x-1][y][1]
                a = grille[x-1][y][0]
                a+=1
                grille[x-1][y]=[a,z]

                z = grille[x-1][y+1][1]
                a = grille[x-1][y+1][0]
                a+=1
                grille[x-1][y+1]=[a,z]

                z = grille[x][y+1][1]
                a = grille[x][y+1][0]
                a+=1
                grille[x][y+1]=[a,z]

            elif y==0 and (x!=0 or x!=(c-1)):               #Cas n°7 : Tout à gauche, ni en haut ni en bas
                z = grille[x-1][y][1]
                a = grille[x-1][y][0]
                a+=1
                grille[x-1][y]=[a,z]

                z = grille[x-1][y+1][1]
                a = grille[x-1][y+1][0]
                a+=1
                grille[x-1][y+1]=[a,z]

                z = grille[x][y+1][1]
                a = grille[x][y+1][0]
                a+=1
                grille[x][y+1]=[a,z]

                z = grille[x+1][y+1][1]
                a = grille[x+1][y+1][0]
                a+=1
                grille[x+1][y+1]=[a,z]

                z = grille[x+1][y][1]
                a = grille[x+1][y][0]
                a+=1
                grille[x+1][y]=[a,z]

            elif y==(c-1) and (x!=0 or x!=(c-1)):           #Cas n°8 : Tout à droite, ni en haut ni en bas
                z = grille[x-1][y][1]
                a = grille[x-1][y][0]
                a+=1
                grille[x-1][y]=[a,z]

                z = grille[x-1][y-1][1]
                a = grille[x-1][y-1][0]
                a+=1
                grille[x-1][y-1]=[a,z]

                z = grille[x][y-1][1]
                a = grille[x][y-1][0]
                a+=1
                grille[x][y-1]=[a,z]

                z = grille[x+1][y-1][1]
                a = grille[x+1][y-1][0]
                a+=1
                grille[x+1][y-1]=[a,z]

                z = grille[x+1][y][1]
                a = grille[x+1][y][0]
                a+=1
                grille[x+1][y]=[a,z]

            else:                                         #Cas n°9 : Le cas général
                z = grille[x-1][y-1][1]
                a = grille[x-1][y-1][0]
                a+=1
                grille[x-1][y-1]=[a,z]

                z = grille[x-1][y][1]
                a = grille[x-1][y][0]
                a+=1
                grille[x-1][y]=[a,z]

                z = grille[x-1][y+1][1]
                a = grille[x-1][y+1][0]
                a+=1
                grille[x-1][y+1]=[a,z]

                z = grille[x][y+1][1]
                a = grille[x][y+1][0]
                a+=1
                grille[x][y+1]=[a,z]

                z = grille[x+1][y+1][1]
                a = grille[x+1][y+1][0]
                a+=1
                grille[x+1][y+1]=[a,z]

                z = grille[x+1][y][1]
                a = grille[x+1][y][0]
                a+=1
                grille[x+1][y]=[a,z]

                z = grille[x+1][y-1][1]
                a = grille[x+1][y-1][0]
                a+=1
                grille[x+1][y-1]=[a,z]

                z = grille[x][y-1][1]
                a = grille[x][y-1][0]
                a+=1
                grille[x][y-1]=[a,z]
        else:
            continue
    return grille

def changer_etat(grille,x,y):
    """Pour le moment, la fonction print le numéro de la case (si c'est un 1,2,3,4,9...) suivi de ses coordonnées
    Utilisée pour le développement"""
    info = b[ref].grid_info()
    colonne=(info["column"])
    ligne=(info["row"])
    print(colonne)
    b[ref].grid_forget()
    print(grille[ligne][colonne])

def debut_de_partie():

    grille_console=grille_vide(c,l)
    generer_bombes(grille_console,bombes,c,l)
    affiche_grille_console(grille_console,c)

    global labels
    labels=[]
    global b
    b = []
    global grille
    grille=Frame(window)
    grille.pack(pady=int(resolution[-3])+50)

    gr=Bouton(grille_console,58,62)
    gr.generer_boutons()

def verif_fin(vie,bombes_trouvees):
    if vie==0:
        etat='defaite'
        fin_du_jeu(etat)
    if bombes_trouvees==bombes:
        etat='victoire'
        fin_du_jeu(etat)
    

def fin_du_jeu(etat):
    if etat=='defaite':
        print("Perdu")
        window.destroy()
    else:
        print('Bravo')
        window.destroy()

def temps_chrono(temps):
    """retourne le temps passé en nano-secondes sous la forme d'un tuple (heures,minutes,secondes,milli-secondes)"""
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
    temps_final=(h,m,s,ms)
    return temps_final

def score(chrono,nb_vies):
    score=(1/sqrt(chrono/10))*exp(2*nb_vies+5)*10**7
    return score

########################################################################################################
######################################### PROGRAMME PRINCIPAL ##########################################
########################################################################################################


# génération de la grille, placement des bombes et des chiffres
c=9             # nombre de colones
l=9             # nombre de lignes
bombes=10       # nombre de bombes
vie=3
premier_clic=False

nbmax=(c*c)-1   # indice de la dernière cases, tout en bas à droite (dans un cadre de 9x9, cette case sera 80)
casehaut=[]
casebas=[]
casehaut.append(0)
for i in range(l):
    casehaut.append((i+1)*c)
    casebas.append(((i+1)*c)-1)
casebas.append(c*l)
bombes_trouvees=0

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
image_fond_label=Label(window, image=fond4)
image_fond_label.place(x=0,y=0,relwidth=1,relheight=1)

window.configure(bg="black")
window.iconphoto(False,logo)
window.title("Cyber démineur")


debut_de_partie()
chrono=time_ns()


window.mainloop()


chrono=(time_ns()-chrono)

print(temps_chrono(chrono))
print(int(score(chrono,3)))     # le plus gros score possible est à 8 chiffres