from django.shortcuts import render
from django.http import JsonResponse
import json
import datetime
import spacy
from spacy.lang.lt.examples import sentences

nlp = spacy.load("lt_core_news_lg")

# Create your views here.

def home(request):
	return render(request, 'home.html')

def variables(request):
	nom = "Édouard"
	hobbies = ["ping pong", "lecture", "musique"]

	membres = [
		{"nom":"Dupond", "prenom":"Sophie"},
		{"nom":"Hache", "prenom":"Anne"},
		{"nom":"Von Ergstadt", "prenom":"Émile"},
		{"nom":"Dupuit", "prenom":"Alex"},
	]

	bigmac = {
		"Énergie": "504kcal",
		"Matières grasses": "25g",
		"Dont acides gras saturés": "9,2g",
		"Sucres": "8,2g",
		"Sel": "2,2g"
	}

	langue = "fi"

	date_birthday = datetime.date(1997, 7, 5)

	return render(request, 'variables.html', 
		{"nom":nom, 
		"hobbies":hobbies,
		"membres":membres,
		"bigmac":bigmac,
		"langue":langue,
		"date_birthday":date_birthday})

def testSpacy(request):
	doc = nlp("Ceci est une phrase d'exemple.")

	return render(request, 'testSpacy.html',
		{"doc":doc})

# fonction pour trouver le bon groupe de déclinaison.
# Certains mots en "-is" et "-ė" au nominatif
# peuvent appartenir à deux groupes différents.
# On cherche le génitif pour déterminer le groupe dans ces cas-là.
def test_groupe(lemme):
	rep = ""
	if lemme[-2:] in ["as", "ys"]:
		rep = "1"
		return rep
	if lemme[-2:] == "is":
		test = lemme[:-2] + "io"
		test_analyse = nlp(test)
		if test_analyse[0].morph.get("Case") == ["Gen"]:
			rep = "1"
			return rep
		test = lemme[:-2] + "ies"
		test_analyse = nlp(test)
		if test_analyse[0].morph.get("Case") == ["Gen"]:
			rep = "3"
			return rep
	elif lemme[-1] in ["a", "i"]:
		rep = "2"
		return rep
	elif lemme[-1] == "ė":
		test = lemme[:-1] + "ės"
		test_analyse = nlp(test)
		if test_analyse[0].morph.get("Case") == ["Gen"]:
			rep = "2"
			return rep
		test = lemme[:-1] + "ers"
		test_analyse = nlp(test)
		if test_analyse[0].morph.get("Case") == ["Gen"]:
			rep = "5"
			return rep
	elif lemme[-2:] == "us":
		rep = "4"
		return rep
	elif lemme[-2:] == "uo":
		rep = "5"
		return rep


def analyze(request):
	colis = json.loads(request.body)
	text = colis['inText']
	print("A analyser :", text)
	output = nlp(text)
	rep = []
	for token in output:
		radical = ""
		terminaison = ""
		couleur = ""
		if token.pos_ == "NOUN":
			groupe = test_groupe(token.lemma_)
			print(groupe)
			# GROUPE 1
			if groupe == "1":
				# SINGULIER
				if token.morph.get("Number") == ["Sing"]:
					if token.morph.get("Case") in [["Gen"], ["Acc"], ["Ins"], ["Loc"], ["Voc"]]:
						radical = token.text[:-1]
						terminaison = token.text[-1]
					elif token.morph.get("Case") in [["Nom"], ["Dat"]]:
						radical = token.text[:-2]
						terminaison = token.text[-2:]
				# PLURIEL
				elif token.morph.get("Number") == ["Plur"]:
					if token.morph.get("Case") == ["Gen"]:
						radical = token.text[:-1]
						terminaison = token.text[-1]
					elif token.morph.get("Case") in [["Nom"], ["Acc"], ["Voc"]]:
						radical = token.text[:-2]
						terminaison = token.text[-2:]
					elif token.morph.get("Case") in [["Dat"], ["Ins"]]:
						radical = token.text[:-3]
						terminaison = token.text[-3:]
					elif token.morph.get("Case") == ["Loc"]:
						radical = token.text[:-4]
						terminaison = token.text[-4:]
			# GROUPE 2
			elif groupe == "2":
				# SINGULIER
				if token.morph.get("Number") == ["Sing"]:
					if token.morph.get("Case") in [["Nom"], ["Acc"], ["Ins"], ["Voc"]]:
						radical = token.text[:-1]
						terminaison = token.text[-1]
					elif token.morph.get("Case") in [["Gen"], ["Dat"]]:
						radical = token.text[:-2]
						terminaison = token.text[-2:]
					elif token.morph.get("Case") == ["Loc"]:
						radical = token.text[:-3]
						terminaison = token.text[-3:]
				# PLURIEL
				elif token.morph.get("Number") == ["Plur"]:
					if token.morph.get("Case") == ["Gen"]:
						radical = token.text[:-1]
						terminaison = token.text[-1]
					elif token.morph.get("Case") in [["Nom"], ["Acc"], ["Voc"]]:
						radical = token.text[:-2]
						terminaison = token.text[-2:]
					elif token.morph.get("Case") in [["Dat"], ["Loc"]]:
						radical = token.text[:-3]
						terminaison = token.text[-3:]
					elif token.morph.get("Case") == ["Ins"]:
						radical = token.text[:-4]
						terminaison = token.text[-4:]
			# GROUPE 3
			elif groupe == "3":
				# SINGULIER
				if token.morph.get("Number") == ["Sing"]:
					if token.morph.get("Case") == ["Acc"]:
						radical = token.text[:-1]
						terminaison = token.text[-1]
					elif token.morph.get("Case") in [["Nom"], ["Voc"]]:
						radical = token.text[:-2]
						terminaison = token.text[-2:]
					elif token.morph.get("Case") in [["Gen"], ["Dat"], ["Ins"], ["Loc"]]:
						radical = token.text[:-3]
						terminaison = token.text[-3:]
				# PLURIEL
				elif token.morph.get("Number") == ["Plur"]:
					if token.morph.get("Case") == ["Gen"]:
						radical = token.text[:-1]
						terminaison = token.text[-1]
					elif token.morph.get("Case") in [["Nom"], ["Acc"], ["Voc"]]:
						radical = token.text[:-2]
						terminaison = token.text[-2:]
					elif token.morph.get("Case") in [["Dat"], ["Loc"]]:
						radical = token.text[:-3]
						terminaison = token.text[-3:]
					elif token.morph.get("Case") == ["Ins"]:
						radical = token.text[:-4]
						terminaison = token.text[-4:]
			# GROUPE 4
			elif groupe == "4":
				# SINGULIER
				if token.morph.get("Number") == ["Sing"]:
					if token.morph.get("Case") == ["Acc"]:
						radical = token.text[:-1]
						terminaison = token.text[-1]
					elif token.morph.get("Case") in [["Nom"], ["Dat"], ["Voc"]]:
						radical = token.text[:-2]
						terminaison = token.text[-2:]
					elif token.morph.get("Case") in [["Gen"], ["Ins"], ["Loc"]]:
						radical = token.text[:-3]
						terminaison = token.text[-3:]
				# PLURIEL
				elif token.morph.get("Number") == ["Plur"]:
					if token.morph.get("Case") == ["Gen"]:
						radical = token.text[:-1]
						terminaison = token.text[-1]
					elif token.morph.get("Case") in [["Nom"], ["Acc"], ["Voc"]]:
						radical = token.text[:-2]
						terminaison = token.text[-2:]
					elif token.morph.get("Case") == ["Dat"]:
						radical = token.text[:-3]
						terminaison = token.text[-3:]
					elif token.morph.get("Case") in [["Ins"], ["Loc"]]:
						radical = token.text[:-4]
						terminaison = token.text[-4:]
			# GROUPE 5
			elif groupe == "5":
				# SINGULIER
				if token.morph.get("Number") == ["Sing"]:
					if token.morph.get("Case") == ["Nom"]:
						radical = token.text[:-2]
						terminaison = token.text[-2:]
					elif token.morph.get("Case") in [["Gen"], ["Acc"]]:
						radical = token.text[:-3]
						terminaison = token.text[-3:]
					elif token.morph.get("Case") in [["Ins"], ["Voc"]]:
						radical = token.text[:-4]
						terminaison = token.text[-4:]
					elif token.morph.get("Case") in [["Dat"], ["Loc"]]:
						radical = token.text[:-5]
						terminaison = token.text[-5:]
				# PLURIEL
				elif token.morph.get("Number") == ["Plur"]:
					if token.morph.get("Case") == ["Gen"]:
						radical = token.text[:-3]
						terminaison = token.text[-3:]
					elif token.morph.get("Case") in [["Nom"], ["Acc"], ["Voc"]]:
						radical = token.text[:-4]
						terminaison = token.text[-4:]
					elif token.morph.get("Case") in [["Dat"], ["Loc"]]:
						radical = token.text[:-5]
						terminaison = token.text[-5:]
					elif token.morph.get("Case") == ["Ins"]:
						radical = token.text[:-6]
						terminaison = token.text[-6:]

			# Sélection d'une couleur pour la terminaison en fonction du cas
			if token.morph.get("Case") == ["Nom"]:
				couleur = "red"
			elif token.morph.get("Case") == ["Gen"]:
				couleur = "blue"
			elif token.morph.get("Case") == ["Dat"]:
				couleur = "deeppink"
			elif token.morph.get("Case") == ["Acc"]:
				couleur = "green"
			elif token.morph.get("Case") == ["Ins"]:
				couleur = "mediumpurple"
			elif token.morph.get("Case") == ["Loc"]:
				couleur = "orange"
			elif token.morph.get("Case") == ["Voc"]:
				couleur = "brown"

			# Sélection d'une couleur pour le soulignement en fonction du genre et du nombre
			# Le pluriel prend la même couleur en plus sombre
			decoration = "underline "
			if token.morph.get("Number") == ["Sing"] and token.morph.get("Gender") == ["Masc"]:
				decoration += "lightblue"
			elif token.morph.get("Number") == ["Sing"] and token.morph.get("Gender") == ["Fem"]:
				decoration += "pink"
			elif token.morph.get("Number") == ["Plur"] and token.morph.get("Gender") == ["Masc"]:
				decoration += "blue"
			elif token.morph.get("Number") == ["Plur"] and token.morph.get("Gender") == ["Fem"]:
				decoration += "red"
			
		rep.append((token.text, radical, terminaison, couleur, decoration))


	return JsonResponse({ "reponse":rep, "texte":text })

