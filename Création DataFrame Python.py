# -*- coding: utf-8 -*-
"""
Created on Thu May 16 11:48:23 2024

@author: mxmdi
"""
import pandas as pd 
import re
#import Levenshtein
#from openpyxl import load_workbook
from unidecode import unidecode
#import nltk
#from nltk.corpus import stopwords
def help_doc(nom_de_fonction:str): #nom_de_fonction doit etre ecris entre guillemets, ex:"DataBase_CIM10_fr"
    if not isinstance(nom_de_fonction, str):
        raise TypeError("Veuillez renseignez un nom de fonction ou de classe pour en connaître le fonctionnement")
    
    if nom_de_fonction == "":
        raise TypeError("Veuillez renseignez un nom de fonction ou de classe pour en connaître le fonctionnement")

  
    if nom_de_fonction == "DataBase_CIM10_fr":
        print("Cette classe à pour but de créer à partir d'un fichier texte, un dataframe panda renseignant de manière claire et épurée, la classification et la signification des code CIM10. Cf. README.txt")
    
    elif nom_de_fonction == 'nettoyage':
        print('Cette fonction est mis à part de la classe DataBase_CIM10_fr car elle permet une épuration de la base de données créée précédemment selon des critères beaucoup plus précis. Cela permet d\'augmenter la précision et la maniabilité du fichier. Cf. README.txt ')
    
    elif nom_de_fonction == 'correction_Database':
        print('Cette fonction permet de parcourir le fichier Excel et de selectionner toutes les colonnes qui commencent par <Specify malformation> afin de leur appliquer la correction.')
   
    elif nom_de_fonction == 'correction_label':
        print("Cette fonction permet de corriger les cellules d'une colonne selon des critères spécifiques. La correction appliquée est issue du fichier Database standardisée. Cf. README.txt")
            
        
    
    
    
    
    
class DataBase_CIM10_fr():
    def __init__(self,nom_fichier,nom_fichier_sortie):
        self.fichier = nom_fichier
        self.fichier_sortie = nom_fichier_sortie
        self.df = []

# Ouvrir le fichier d'entrée en mode lecture
    def open_fichier(self):
        with open(self.fichier, "r", encoding='iso-8859-1') as f_entree:
            self.lignes =f_entree.readlines()
        

    def supprimer_motif(self, ligne):
     # Diviser la ligne en utilisant le caractère "|"
     parties = ligne.split("|")
     # Sélectionner uniquement la partie avant le premier "|" et après le dernier "|"
     if len(parties) > 1:
         ligne_modifiee = parties[0] + " " + parties[-1]
     else:
         ligne_modifiee = ligne

     # Expression régulière pour capturer le motif "*** qlq chose ***"
     motif_etoiles = re.compile(r'\*\*\* [^\*]+ \*\*\*')
     # Supprimer le motif "*** qlq chose ***"
     ligne_modifiee = motif_etoiles.sub('', ligne_modifiee)
     
     # Supprimer les parenthèses sauf '(s)'
     ligne_modifiee = ligne_modifiee.replace('(s)', '[s]')  # Remplace '(s)' par '(s)' (pour remettre le motif)
     ligne_modifiee = ligne_modifiee.replace('(', '').replace(')', '')  # Remplace tous les '(' et ')' par ''
     ligne_modifiee = ligne_modifiee.replace('[s]', '(s)')  # Remplace '(s)' par '(s)' (pour remettre le motif)


     # Retourner la ligne modifiée en supprimant les espaces superflus
     return ligne_modifiee.strip()

 # Création du fichier nettoyé
    def open_fichier_sortie(self):
     self.lignes_modifiees = [self.supprimer_motif(ligne) for ligne in self.lignes]
     with open(self.fichier_sortie, "w", encoding='utf-8') as f_sortie:
         # Écrire les lignes modifiées dans le fichier de sortie
         for ligne_modifiee in self.lignes_modifiees:
             f_sortie.write(ligne_modifiee + '\n')
                
#Lecture du fichier de sortie 
    def lecture_sortie(self):
        with open(self.fichier_sortie, "r", encoding='utf-8') as f_entree:
            ligne =f_entree.readlines()
            for elt in ligne :
                print(elt)
   
#Création d'un Dataframe à partir du texte 
    def texte_to_df(self):

        # Ouvrir le fichier de sortie en mode lecture
        with open(self.fichier_sortie, "r", encoding='utf-8') as f_sortie:
            # Lire les lignes du fichier de sortie
            lignes = f_sortie.readlines()

            # Parcourir chaque ligne et extraire le code CIM-10 et le libellé associé
            for ligne in lignes:
                # Rechercher l'index du premier espace dans la ligne
                index_espace = ligne.find(" ")
                if index_espace != -1:
                    # Extraire le code CIM-10 et le libellé à partir de l'index de l'espace
                    code = ligne[:index_espace].strip()
                    libelle = ligne[index_espace:].strip()
                    # Ajouter le code et le libellé à la liste de données
                    self.df.append({"CIM-10": code, "Lib": libelle})
        self.df = pd.DataFrame(self.df)
        self.df["Lib"] = self.df["Lib"].apply(lambda x: unidecode(x).upper())
        

#Création d'un fichier excel à partir d'un Dataframe
    def export_df(self):
        try :
            self.df.to_excel('Database standardisée.xlsx', index = False)
        
        except PermissionError:
            raise PermissionError("Impossible d'écrire dans le fichier Excel. Vérifiez les autorisations, ou s'il n'est pas ouvert dans une fenêtre")
        except :
            raise TypeError("Aucun DataFrame correspondant, Ref:texte_to_df")
            
        
#Affichage du DataFrame         
    def afficher_df(self):
        print(self.df.head(100))
              
        
        
        
        


# =============================================================================
# Edition et nettoyage de la Database standardisée

def nettoyage(dataframe, column_name, pattern, replacement_pattern):
    """
    Fonction pour nettoyer une colonne d'un DataFrame en remplaçant un motif par un autre.

    Args:
    - dataframe : DataFrame pandas.
    - column_name : Nom de la colonne à nettoyer.
    - pattern : Motif à rechercher dans chaque élément de la colonne.
    - replacement_pattern : Motif de remplacement pour chaque occurrence du motif.

    Returns:
    - Le DataFrame avec la colonne spécifiée nettoyée.
    """
    # Vérifier si la colonne spécifiée existe dans le DataFrame
    if column_name not in dataframe.columns:
        raise ValueError(f"La colonne '{column_name}' n'existe pas dans le DataFrame.")

    # Nettoyer la colonne spécifiée en remplaçant le motif par le motif de remplacement
    dataframe[column_name] = dataframe[column_name].str.replace(pattern, replacement_pattern,regex=True)

    return dataframe

#=============================================================================
#Application des méthodes et fonctions 
 # Nom du fichier d'entrée
fichier_entree = r"LIBCIM10MULTI.txt"
# Nom du fichier de sortie
fichier_sortie = r"DataBase_CIM10_fr.txt"

Df = DataBase_CIM10_fr(fichier_entree, fichier_sortie)       
Df.open_fichier()
Df.open_fichier_sortie()
Df.texte_to_df()
nettoyage(Df.df,'Lib',r'\(CONGENITALE(S?)\)',"")
nettoyage(Df.df,'Lib','COMMUNICATION AURICULO-VENTRICULAIRE',"CAV")
nettoyage(Df.df,'Lib','COMMUNICATION INTERAURICULAIRE',"CIA")
nettoyage(Df.df,'Lib','COMMUNICATION INTERVENTRICULAIRE',"CIV")
nettoyage(Df.df,'Lib','COMMUNICATION VENTRICULO-AURICULAIRE',"CVA")
nettoyage(Df.df,'Lib',',',"")
Df.export_df()
#==============================================================================
#Programme de correction
def correction_Database(df, db):
    """
    Corrige les colonnes "Specify malformation" d'un DataFrame en utilisant une base de données standardisée.

    Args:
        df (pandas.DataFrame): Le DataFrame à corriger.
        db (pandas.DataFrame): La base de données standardisée contenant les codes CIM10 et les libellés corrects.

    Returns:
        pandas.DataFrame: Le DataFrame corrigé.
        dict: Un dictionnaire contenant les codes CIM10 et les libellés non corrigés.
    """
    
    global corrections_count
    # Initialiser le compteur de corrections
    corrections_count = 0

    # Initialiser le dictionnaire pour stocker les codes CIM10 et les libellés non corrigés
    non_corriges = {}

    # Trouver les colonnes à corriger
    columns_to_correct = [col for col in df.columns if col.startswith("Specify malformation")]

    # Indexer la base de données sur la colonne "CIM-10"
    db = db.set_index("CIM-10")

    # Boucle sur les colonnes à corriger
    for column in columns_to_correct:
        # Trouver la colonne CIM10 correspondante
        cim10_column = df.columns[df.columns.get_loc(column) - 1]

        # Appliquer la correction sur la colonne entière
        df[column] = df.apply(lambda row: correction_label(row[cim10_column], row[column], db, non_corriges), axis=1)

    # Afficher le nombre de corrections
    print(f"Nombre de corrections effectuées : {corrections_count}")

    # Retourner le DataFrame corrigé et le dictionnaire des codes CIM10 et libellés non corrigés
    return df, non_corriges

def correction_label(cim10_code, current_label, db, non_corriges):
    """
    Corrige un libellé en fonction du code CIM10.

    Args:
        cim10_code (str): Le code CIM10.
        current_label (str): Le libellé actuel.
        db (pandas.DataFrame): La base de données standardisée.
        non_corriges (dict): Le dictionnaire pour stocker les codes CIM10 et les libellés non corrigés.

    Returns:
        str: Le libellé corrigé.
    """

    global corrections_count

    # Vérifier si le code CIM10 est un code de malformation (commençant par "Q" et suivi de trois chiffres au maximum)
    if pd.notna(cim10_code):  # Vérifier si le code CIM10 n'est pas NaN
        cim10_code = str(cim10_code)  # Convertir le code CIM10 en chaîne de caractères uniquement si il existe
        if cim10_code.startswith("Q") and len(cim10_code) <= 4:
            # Trouver le libellé correct dans la base de données standardisée
            try:
                correct_label = db.loc[cim10_code]["Lib"]
            except KeyError:
                # Le code CIM10 n'existe pas dans la base de données, on ajoute au dictionnaire
                non_corriges[cim10_code] = current_label
                return current_label

            # Vérifier si le libellé actuel est incorrect
            if current_label != correct_label:
                corrections_count += 1
                return correct_label
            else:
                return current_label
        else:
            # Le code CIM10 ne respecte pas la condition, on ajoute au dictionnaire
            non_corriges[cim10_code] = current_label
            return current_label
    else:
        # Si le code CIM10 n'est pas un code de malformation, ne pas modifier le libellé
        return current_label
#==============================================================================
#Application de la correction sur le fichier à l'aide du fichier de références.
# Charger les fichiers Excel et CSV
df = pd.read_excel( r"\Users\mxmdi\OneDrive\Documents\Projet Stage\Extraction EDMS 2002 2020.xlsx", header=4)
db = pd.read_excel("Database standardisée.xlsx")

# Appeler la fonction de correction
df_corrected, non_corriges = correction_Database(df, db)

# Enregistrer le DataFrame corrigé
df_corrected.to_excel("test_correction.xlsx", index=False)

#Les prochaines lignes permettent de prendre connaissance des libellés qui n'ont pas été modifiés au cours du programme.  
# Enlevez le '#' devant le print pour afficher le dictionnaire des codes CIM10 et libellés non corrigés

#print(non_corriges)






    
    


