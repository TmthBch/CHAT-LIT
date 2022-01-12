console.log('Le script est bien chargé!');

async function sendText() {
  console.log("L'utilisateur a cliqué sur le bouton !");
  
  // ON RECUPÈRE LES VARIABLES A ENVOYER AU SERVEUR
  var inText = document.getElementById('inText').value;

  // ON EMBALLE TOUT CA DANS UN JSON
  var colis = {
    inText: inText
  }
  console.log('Envoi colis:', colis);

  // PARAMÈTRES DE LA REQUÊTE
  const requete = {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(colis)
  };

  // ENVOI ET RECUPERATION DE LA REPONSE
  const response = await fetch('/analyze/', requete)
  const data = await response.json();
  console.log(data);

  var outText = document.getElementById('outText');
  outText.innerHTML = ""; // vider la div si elle contenait déjà qqc
  for (token in data.reponse) {
    var tokenTuple = data.reponse[token];
    if (tokenTuple[1] != ""){ // Si radical != "" c'est que le mot est un nom
      outText.innerHTML += "<span style='text-decoration:" + tokenTuple[4] + ";'>" + tokenTuple[1] + "<span style='color:" + tokenTuple[3] + ";'>" + tokenTuple[2] + "</span></span> ";
    }
    else{ // Si ce n'est pas un nom on affiche simplement le texte du token
      outText.innerHTML += tokenTuple[0] + " ";
    }
  }
}

