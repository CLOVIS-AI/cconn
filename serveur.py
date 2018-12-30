import atexit
import socket
from threading import Thread

from utils import byte_to_message, Message


class Serveur:

    def __init__(self, port, max_connections=1):
        print("Serveur: Démarrage...")
        self.clients = []
        self.commandes = {}
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind(("", port))
        self.socket.listen(max_connections)
        print("Serveur: Connecté sur le port", self.socket.getsockname()[1])
        atexit.register(self.eteindre)

    def lancer(self):
        print("Serveur: En route")
        while True:
            client, infos = self.socket.accept()
            Thread(target=self.__connexion_au_client, args=[client]).start()

    def __connexion_au_client(self, client):
        self.clients.append(client)
        Client(self, client)
        self.clients.remove(client)

    def enregistrer_commande(self, nom, callback):
        self.commandes[nom] = callback
        print("Serveur: Commande enregistrée:", nom)

    def eteindre(self):
        self.socket.close()
        print("Serveur: Déconnecté.")


class Client:

    def __init__(self, serveur, socket):
        self.__socket = socket
        self.__serveur = serveur
        self.coords = socket.getpeername()
        print("Serveur:", self.__socket.getpeername(), "s'est connecté.")
        self.__ecoute()

    def __ecoute(self):
        while True:
            try:
                msg = self.__socket.recv(8000)

                if msg == b'':
                    break

                for message in byte_to_message(msg):
                    if message.nom in self.__serveur.commandes:
                        print("Serveur:", self.coords, ">>>", message)
                        self.__serveur.commandes[message.nom](self.__serveur, self, *message.args)
                    else:
                        print("Serveur WARNING: Commande", message.nom, "inconnue !")
            except ConnectionResetError:
                break
        self.close(clientside=True)

    def envoyer(self, commande, *args):
        msg = Message(commande, *args)
        print("Serveur:", self.coords, "<<<", msg)
        msg.envoyer(self.__socket)

    def close(self, clientside=False):
        if clientside:
            print("Serveur:", self.coords, "s'est déconnecté.")
        else:
            print("Serveur:", self.coords, "a été déconnecté par le serveur.")
            self.__socket.close()
