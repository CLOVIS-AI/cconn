import socket

from cconn.utils import Message, byte_to_message


class Client:

    def __init__(self, addresse, port):
        print("Client: Démarrage...")
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((addresse, port))
        self.__est_lance = True
        self.__commandes = {}
        print("Client: Connexion établie.")

    def lancer(self):
        print("Client: À l'écoute")
        while self.__est_lance:
            msg = self.socket.recv(8000)

            if msg == b'':
                print("Client: Le serveur a fermé la connexion...")
                break

            for message in byte_to_message(msg):
                if message.nom in self.__commandes:
                    print("Serveur:", self.socket.getpeername(), ">>>", message)
                    self.__commandes[message.nom](self, *message.args)
                else:
                    print("Serveur WARNING: Commande", message.nom, "inconnue !")

        self.socket.close()
        print("Client: Déconnecté.")

    def enregistrer_commande(self, nom, callback):
        self.__commandes[nom] = callback
        print("Client: Commande enregistrée:", nom)

    def eteindre(self):
        self.__est_lance = False

    def envoyer(self, message, *args):
        msg = Message(message, *args)
        print("Client:", self.socket.getpeername(), "<<<", msg)
        msg.envoyer(self.socket)
