# CLOVIS Python Networking

Petite bibliothèque Python pour les communications réseau via TCP/IP.

## Installation & configuration

## Côté serveur

Il faut commencer par créer le serveur:
(exemple pour un serveur écoutant sur le port 12 800)

    from cconn.serveur import Serveur
    serveur = Serveur(12800)

On peut aussi définir un nombre de connexions maximales simultanées
(par défaut, un seul client peut se connecter):

    # Autoriser un maximum de 23 clients simultanés
    serveur = Serveur(12800, 23)

Ensuite, on enregistre des commandes:

    # Création d'une fonction 'ping' qui sera appelée lorsque
    # la commande sera reçue.
    def ping(serveur, client, word):
        client.envoyer("pong", word)
    
    # Enregistrement de la commande
    serveur.enregistrer_commande("ping", ping)

Il ne faut pas oublier de lancer le serveur:

    serveur.lancer()

Cet appel est une boucle infinie. Pour arrêter le serveur, il faut
utiliser `serveur.eteindre()`.

### Envoyer des données au client

Quand on reçoit une commande, on peut utiliser l'objet `client` qui
est fourni pour répondre:

    client.envoyer(NOM DE LA COMMANDE, PARAMETRES)

Le nom de la commande doit faire référence à une commande qui existe
du côté client, et les paramètres doivent correspondre aux paramètres
de la commande en question.

### Déconnecter un client

On peut déconnecter un client sans déconnecter les autres,
en utilisant:

    client.close()

à l'intérieur d'une commande.

### Performances

Le serveur crée un thread pour chaque client, qui est détruit quand
ledit client se déconnecte.

## Côté client

Création du client et connexion au serveur:
(exemple avec un serveur d'IP 127.0.0.1 et de port 12 800)

    from cconn.client import Client
    client = Client("127.0.0.1", 12800)

Il faut ensuite enregistrer les différentes commandes.
Par exemple, la commande "somme" qui répond la somme de deux nombres:

    # On crée une fonction qui sera appelée quand la
    # commande sera reçue.
    # Le paramètre 'client' permet de récupérer la connexion
    # pour pouvoir répondre; les autres paramètres sont
    # arbitraires.
    
    def somme(client, premier, deuxieme):
        client.envoyer("somme", premier + deuxieme)
    
    # On enregistre la fonction comme commande.
    client.enregistrer_commande("somme", somme)

Enfin, pour que le client écoute les réponses du serveur,
il faut activer le mode "écoute":

    client.lancer()

Cette fonction est une boucle infinie, le programme ne s'arrêtera
que quand la fonction `client.eteindre()` sera appelée.

### Envoyer un message au serveur

Syntaxe:

    client.envoyer(NOM DE LA COMMANDE, PARAMETRES)

où le nom de la commande fait référence à une commande
ayant été enregistrée du côté du serveur,
et les paramètres sont les arguments de cette commande.

Par exemple, si une commande 'somme' existe côté serveur
qui prend deux paramètres, ont peut appeler:

    client.envoyer("somme", 12, 34)

### Arrêter le client

On peut se déconnecter avec la fonction:

    client.eteindre()

Le client se déconnectera quand il aura fini de lire les messages
en cours (donc pas immédiatement).

## Exemple complet