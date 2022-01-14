# CHAT-LIT
CHromatisateur Automatique de Terminaisons LITuaniennes

# CE QUE C'EST
Une application qui permet de faire ressortir automatiquement les terminaisons des noms communs en lituaniens à l'aide de couleurs. Le but étant de faciliter la détection des différents cas, et donc des différents acteurs de la phrase à l'apprenant débutant dans cette langue.

# COMMENT CA MARCHE
Tapez, ou copiez-collez, une phrase en lituanien dans la zone prévue à cet effet, puis cliquez sur le bouton Analyser !. Votre phrase s'affichera de nouveau juste en dessous du cadre. Les noms communs apparaîtront avec leur terminaison colorée en fonction du cas auquel est le mot en question. Il seront également soulignés de manière à indiquer leur genre et leur nombre. Les codes couleurs correspondant sont disponibles dans l'encadré au dessus de la zone de texte.

# COMMENT L'INSTALLER
Téléchargez le contenu du répertoire github. Installez Python, Spacy et Django (pip install -U Django et pip install -U spacy). Installez aussi le modèle de langue pour le lituanien (spacy download lt_core_news_lg). Déplacez vous à la racine du répertoire github et lancez la commande "python manage.py runserver" puis renz-vous sur votre navigateur web à l'adresse "127.0.0.1:8000". L'application devrait s'afficher. Suivez ensuite les instructions du paragraphe précédent.
