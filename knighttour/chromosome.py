import random
import math

# ============================================
# CONSTANTES
# ============================================
MOVES = [(2,1), (1,2), (-1,2), (-2,1), (-2,-1), (-1,-2), (1,-2), (2,-1)]
BOARD_SIZE = 8
TARGET_FITNESS = 64

# ============================================
# FONCTIONS UTILITAIRES
# ============================================
def count_onward_moves(pos, visited):
    """Compte les mouvements futurs possibles (heuristique Warnsdorff)."""
    x, y = pos
    count = 0
    for dx, dy in MOVES:
        nx, ny = x + dx, y + dy
        if 0 <= nx < BOARD_SIZE and 0 <= ny < BOARD_SIZE and (nx, ny) not in visited:
            count += 1
    return count

def get_smart_moves(pos, visited):
    """Retourne les mouvements triés par Warnsdorff (moins de choix futurs = prioritaire)."""
    x, y = pos
    valid_moves = []
    
    for dx, dy in MOVES:
        nx, ny = x + dx, y + dy
        if 0 <= nx < BOARD_SIZE and 0 <= ny < BOARD_SIZE and (nx, ny) not in visited:
            score = count_onward_moves((nx, ny), visited)
            valid_moves.append((score, (nx, ny)))
    
    valid_moves.sort()
    return [move for _, move in valid_moves]

# ============================================
# CHROMOSOME
# ============================================
class Chromosome:
    def __init__(self, genes=None, use_heuristic=False):
        if genes:
            self.genes = genes
        elif use_heuristic:
            self.genes = self._generate_smart_path()
        else:
            self.genes = self._generate_guided_path()
    
    def _generate_smart_path(self):
        """Génère un chemin avec l'heuristique de Warnsdorff."""
        position = (0, 0)
        visited = {position}
        genes = []
        
        for _ in range(BOARD_SIZE * BOARD_SIZE - 1):
            smart_moves = get_smart_moves(position, visited)
            if not smart_moves:
                genes.extend([random.randint(0, 7) for _ in range(TARGET_FITNESS - 1 - len(genes))])
                break
            
            next_pos = smart_moves[0]
            dx = next_pos[0] - position[0]
            dy = next_pos[1] - position[1]
            gene = MOVES.index((dx, dy))
            
            genes.append(gene)
            position = next_pos
            visited.add(position)
        
        return genes if len(genes) == 63 else genes + [random.randint(0, 7) for _ in range(63 - len(genes))]
    
    def _generate_guided_path(self):
        """Génère un chemin random mais guidé."""
        position = (0, 0)
        visited = {position}
        genes = []
        
        for _ in range(BOARD_SIZE * BOARD_SIZE - 1):
            x, y = position
            valid = []
            for i, (dx, dy) in enumerate(MOVES):
                nx, ny = x + dx, y + dy
                if 0 <= nx < BOARD_SIZE and 0 <= ny < BOARD_SIZE and (nx, ny) not in visited:
                    valid.append(i)
            
            if valid:
                gene = random.choice(valid)
                genes.append(gene)
                dx, dy = MOVES[gene]
                position = (position[0] + dx, position[1] + dy)
                visited.add(position)
            else:
                genes.extend([random.randint(0, 7) for _ in range(63 - len(genes))])
                break
        
        return genes if len(genes) == 63 else genes + [random.randint(0, 7) for _ in range(63 - len(genes))]
    
    def crossover(self, partner):
        """Crossover en deux points."""
        if len(self.genes) < 3:
            return Chromosome(self.genes[:]), Chromosome(partner.genes[:])
        
        p1, p2 = sorted(random.sample(range(1, len(self.genes)), 2))
        
        child1 = self.genes[:p1] + partner.genes[p1:p2] + self.genes[p2:]
        child2 = partner.genes[:p1] + self.genes[p1:p2] + partner.genes[p2:]
        
        return Chromosome(child1), Chromosome(child2)
    
    def mutation(self, mutation_rate=0.10):
        """Mutation intelligente."""
        for i in range(len(self.genes)):
            if random.random() < mutation_rate:
                if random.random() < 0.3:
                    self.genes[i] = random.randint(0, 7)
                else:
                    self.genes[i] = (self.genes[i] + random.choice([-1, 1])) % 8
