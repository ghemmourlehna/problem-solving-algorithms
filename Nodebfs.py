class Node:
    def __init__(self, state, parent=None, action=None, g=0):
        self.state = state        # Etat du puzzle (RushHourPuzzle)
        self.parent = parent      # Référence vers le parent
        self.action = action      # Action effectuée pour arriver ici
        self.g = g if parent is None else parent.g + 1

    def getPath(self,csv_file):
        """
        Retourne la liste des états (RushHourPuzzle) depuis la racine jusqu'à ce nœud.
        """
        path = [] 
        node = self #nœud courant
        while node is not None: #Boucle pour remonter dans l’arbre
            path.append(node.state) #On ajoute son état (node.state) à la liste path
            node = node.parent
        return list(reversed(path)) #on a les neouds du courant jusqu a la racine donc on inverse la liste pour avoir de la racine au 
    
    def getSolution(self):
        """
        Retourne la liste des actions depuis l'état initial jusqu'à ce nœud.
        """
        actions = [] 
        node = self 
        while node.parent is not None:  
            actions.append(node.action)
            node = node.parent
        return list(reversed(actions))
    
    