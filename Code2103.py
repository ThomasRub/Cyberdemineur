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
from time import *
from math import*

########################################################################################################
######################################### CLASSES ######################################################
########################################################################################################
class Bouton(Button):
    def set_grille(self,grille):
        self.grille=grille
class Grille:
    def __init__(self,grille,taille_case,taille_label):
        self.grille=grille
        self.image_label=case_vide
        self.taille_label=taille_label
        self.taille_case=taille_case
        self.grille_button=[[0 for i in range(c)]for i in range (l)]
        self.grille_label=[[0 for i in range(c)]for i in range (l)]

    def generer_boutons(self):
        """Méthode qui génère les boutons. Elle génère également la "grille de fond" qui affiche les valeurs des cases au joueur.
        Les boutons ont deux actions : clic gauche, qui dévoile la case; et clic droit, qui pose un drapeau."""
        for i in range(len(self.grille)):
            for j in range(len(self.grille[i])):
                self.grille_label[i][j] = Label(grille,bd=1,justify=CENTER,relief="flat",image=self.image_label,width=self.taille_label,height=self.taille_label)
                self.grille_label[i][j].grid(column=j,row=i)
                self.grille_button[i][j] = Bouton(grille,width=self.taille_case,height=self.taille_case,image=case_cachee,relief='flat')
                self.grille_button[i][j].set_grille(self)
                self.grille_button[i][j].grid(column=j,row=i)
                self.grille_button[i][j].bind("<Button-3>",lambda i,x=j,y=i: self.afficheFlag(x,y))
                self.grille_button[i][j].bind("<Button-1>",lambda i,x=j,y=i: self.click(x,y))
        for i in (self.grille):
            to_send = ""
            for j in i :
                to_send += "# "
            print(to_send)
        print('bdbfhbhbfrhvbhbv')
        for i in (self.grille_button):
            to_send = ""
            for j in i :
                to_send += "# "
            print(to_send)
        print('hbfgvhgevcftv')
        for i in (self.grille_label):
            to_send = ""
            for j in i :
                to_send += "# "
            print(to_send)



        """
        for i in self.grille :
            for j in i :
                j.append(Label(grille,bd=1,justify=CENTER,relief="flat",image=self.image_label,width=self.taille_label,height=self.taille_label))
                j[-1].grid(column=j,row=i)
                j.append(Bouton(grille,width=self.taille_case,height=self.taille_case,image=case_cachee,relief='flat'))
                j[-1].set_grille(self)
                j[-1].grid(column=j,row=i)
                j[-1].bind("<Button-3>",lambda i,x,y: self.afficheFlag(x,y))
                j[-1].bind("<Button-1>",lambda i,x,y: self.click(x,y))"""
    """
    def generer_boutons(self):
        """"""Méthode qui génère les boutons. Elle génère également la "grille de fond" qui affiche les valeurs des cases au joueur.
        Les boutons ont deux actions : clic gauche, qui dévoile la case; et clic droit, qui pose un drapeau.""""""
        a=0

        for i in range(l):
            for j in range(c):


                b.append(Button(grille,width=self.taille_case,height=self.taille_case,image=case_cachee,relief='flat'))
                b[a].grid(column=j,row=i)
                b[a].bind("<Button-3>",lambda i,ref=a: self.afficheFlag(ref))
                b[a].bind("<Button-1>",lambda i,ref=a: self.click(ref,premier_clic))
                a+=1
    """
    def affiche_valeurs(self,colonne,ligne):

        if self.grille[ligne][colonne][0] == 0 and self.grille[ligne][colonne][1] == 0:
            self.image_label=case_vide
        elif self.grille[ligne][colonne][0] == 1 and self.grille[ligne][colonne][1] == 0:
            self.image_label=case1
        elif self.grille[ligne][colonne][0] == 2 and self.grille[ligne][colonne][1] == 0:
            self.image_label=case2
        elif self.grille[ligne][colonne][0] == 3 and self.grille[ligne][colonne][1] == 0:
            self.image_label=case3
        elif self.grille[ligne][colonne][0] == 4 and self.grille[ligne][colonne][1] == 0:
            self.image_label=case4
        elif self.grille[ligne][colonne][0] == 5 and self.grille[ligne][colonne][1] == 0:
            self.image_label=case5
        elif self.grille[ligne][colonne][0] == 6 and self.grille[ligne][colonne][1] == 0:
            self.image_label=case6
        elif self.grille[ligne][colonne][0] == 7 and self.grille[ligne][colonne][1] == 0:
            self.image_label=case7
        elif self.grille[ligne][colonne][0] == 8 and self.grille[ligne][colonne][1] == 0:
            self.image_label=case8
        elif self.grille[ligne][colonne][0]==9 and self.grille[ligne][colonne][1] == 0:
            self.image_label=case_bombe
            global bombes_trouvees
            bombes_trouvees+=1
            global vie
            vie-=1
        self.grille_label[ligne][colonne]['image']=self.image_label
        self.grille_button[ligne][colonne].grid_remove()


    def click(self,ligne,colonne):
        """Méthode qui dévoile la case si le bouton est cliqué (via le clic gauche). Elle efface le bouton,
        et modifie la case de la grille sous le bouton pour que la bonne valeur soit affichée.
        Elle prends aussi en charge de dévoiler les cases adjacentes à une case vide (diagonale non prise en charge)"""

        # Changement de la case 0. Cette partie gère également la découverte auto des cases adjacentes
        if self.grille[ligne][colonne][0] == 0 and self.grille[ligne][colonne][1] == 0:
            self.affiche_valeurs(ligne,colonne)
            """
            global id
            id = []
            recherche_id_vide(colonne,ligne)
            print(id)
            for a in id:
                try:
                    self.affiche_valeurs(a)
                except KeyError:
                    pass
            """
        else:
            self.affiche_valeurs(ligne,colonne)

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

def recherche_id_vide(x,y):
    if len(grille_console[0])*x+y not in id :
        id.append(len(grille_console[0])*x+y)
        print(x,y)
        if grille_console[y][x][0]==0:
            if x != 0:
                recherche_id_vide(x-1,y)
            if x != len(grille_console[0])-1:
                recherche_id_vide(x+1,y)
            if y != 0 :
                recherche_id_vide(x,y-1)
            if y != len(grille_console)-1:
                recherche_id_vide(x,y+1)

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
    global grille_console
    grille_console=generer_grille(l,c,bombes)
    affiche_grille_console(grille_console)

    global grille
    grille=Frame(window)
    grille.pack(pady=int(resolution[-3])+50)

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
    if etat=='defaite':
        suppr_tout()
        fin=Canvas(window,width=1550,height=700)
        #fin.create_image(x=0,y=0,image=dommage)
    else:
        print('Bravo')
        suppr_tout()
        fin=Label(window,image=victoire)

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
    score=(1/sqrt(chrono/10))*exp(2*nb_vies+5)*10**2
    return score

def suppr_tout():
    grille.destroy()

########################################################################################################
######################################### PROGRAMME PRINCIPAL ##########################################
########################################################################################################


# génération de la grille, placement des bombes et des chiffres
l=8         # nombre de lignes
c=8             # nombre de colones
bombes=8       # nombre de bombes
vie=2222
premier_clic=False

nbmax=(l*c)-1   # indice de la dernière cases, tout en bas à droite (dans un cadre de 9x9, cette case sera 80)
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
case1=PhotoImage(file=r"case1.png")
case2=PhotoImage(file="case2.png")
case3=PhotoImage(file="case3.png")
case4=PhotoImage(file="case4.png")
case5=PhotoImage(file="case5.png")
case6=PhotoImage(file="case6.png")
case7=PhotoImage(file="case7.png")
case8=PhotoImage(file="case8.png")
fond4=PhotoImage(file="fond4.png")
victoire=PhotoImage(file="ecran_victoire.png")
dommage=PhotoImage(file="ecran_defaite.png")
logo=PhotoImage(file="logo_cyberdemineur.png")

# définition de l'image de fond
image_fond_label=Label(window, image=fond4)
image_fond_label.place(x=0,y=0,relwidth=1,relheight=1)

window.configure(bg="black")
window.iconphoto(False,logo)
window.title("Cyber démineur")



debut_de_partie()
chrono=time()



window.mainloop()

chrono=(time()-chrono)

print(temps_chrono(chrono))
print(int(score(chrono,3)))