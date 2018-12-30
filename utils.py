import pickle


def byte_to_message(bytes):
    messages = []
    if bytes != b'':
        for commande in bytes.split(b'\n'):
            if commande != b'':
                parts = commande.split(b' ', 1)
                nom = parts[0].decode()
                params = pickle.loads(parts[1])

                messages.append(Message(nom, *params))
    return messages


class Message:

    def __init__(self, nom, *args):
        self.nom = nom
        self.args = []
        for arg in args:
            self.args.append(arg)

    def __str__(self) -> str:
        s = self.nom
        for arg in self.args:
            s += ' '
            s += str(arg)
        return s

    def envoyer(self, socket):
        s = self.nom.encode() + b' '
        s += pickle.dumps(self.args)
        s += b"\n"
        try:
            socket.send(s)
        except OSError:
            print("Warning: Impossible d'envoyer le message, la connexion ne doit plus être valide.")
