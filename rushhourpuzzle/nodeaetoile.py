class Node:
    def __init__(self, rushHourPuzzle, parent=None, action="", c=1, heuristic=1):
        self.state = rushHourPuzzle
        self.parent = parent
        self.action = action
        self.g = 0 if not self.parent else self.parent.g + c
        self.h = 0
        self.f = 0
        self.setF(heuristic)  
        self.heuristic_used = heuristic  
    # ---- Heuristiques ----
    def heuristic1(self):
        for vehicle in self.state.vehicles:
            if vehicle["id"] == 'X':
                return self.state.board_width - 2 - vehicle["x"]
        return 0

    def heuristic2(self):
        for vehicle in self.state.vehicles:
            if vehicle["id"] == 'X':
                unique_vehicles = set(self.state.board[vehicle["y"]][vehicle["x"]:])
                if ' ' in unique_vehicles:
                    return self.heuristic1() + len(unique_vehicles) - 2
                return self.heuristic1() + len(unique_vehicles) - 1
        return 0

    def heuristic3(self):
        for vehicle in self.state.vehicles:
            if vehicle["id"] == 'X':
                x, y, length = vehicle["x"], vehicle["y"], vehicle["length"]
                distance_to_exit = self.state.board_width - (x + length)
                obstacles = 0
                for col in range(x + length, self.state.board_width):
                    if self.state.board[y][col] != ' ':
                        obstacles += 1
                return distance_to_exit + obstacles
        return 0

    # ---- Méthode pour définir f ----
    def setF(self, heuristic):
        heuristics = {
            1: self.heuristic1(),
            2: self.heuristic2(),
            3: self.heuristic3()
        }
        h_value = heuristics.get(heuristic, self.heuristic1())
        self.h = h_value
        self.f = self.g + self.h

    # ---- Fonctions de chemin ----
    def getPath(self):
        states = []
        node = self
        while node is not None:
            states.append(node.state)
            node = node.parent
        return states[::-1]

    def getSolution(self):
        actions = []
        node = self
        while node is not None:
            actions.append(node.action)
            node = node.parent
        return actions[::-1]
