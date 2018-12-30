# CLOVIS Python Networking

Petite bibliothèque Python pour les communications réseau via TCP/IP.

## Installation & configuration

## Côté serveur

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