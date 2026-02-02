from chromosome import Chromosome
from chromosome import MOVES, BOARD_SIZE
import random
class Knight:
    def __init__(self, chromosome=None):
        self.chromosome = chromosome if chromosome else Chromosome()
        self.fitness = None
        self.path = None
    
    def evaluate_fitness(self):
        """Évaluation ultra-rapide."""
        if self.fitness is not None:
            return self.fitness
        
        position = (0, 0)
        path = [position]
        visited = {position}
        
        for gene in self.chromosome.genes:
            if gene < 0 or gene >= len(MOVES):
                break
            
            dx, dy = MOVES[gene]
            new_pos = (position[0] + dx, position[1] + dy)
            
            if (0 <= new_pos[0] < BOARD_SIZE and
                0 <= new_pos[1] < BOARD_SIZE and
                new_pos not in visited):
                position = new_pos
                path.append(position)
                visited.add(position)
            else:
                break
        
        self.fitness = len(path)
        self.path = path
        return self.fitness
