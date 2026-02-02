from knight import Knight
from chromosome import Chromosome
import random
class Population:
    def __init__(self, population_size=100):
        self.population_size = population_size
        self.generation = 0
        
        # 40% avec heuristique Warnsdorff, 60% random guidé
        smart_count = (population_size * 40) // 100
        self.knights = [Knight(Chromosome(use_heuristic=True)) for _ in range(smart_count)]
        self.knights += [Knight(Chromosome()) for _ in range(population_size - smart_count)]
        
        self.best_fitness_ever = 0
        self.best_path_ever = None
        self.stagnation = 0
    
    def evaluate(self):
        """Évaluation de la population."""
        best_knight = None
        best_fitness = 0
        
        for knight in self.knights:
            fitness = knight.evaluate_fitness()
            if fitness > best_fitness:
                best_fitness = fitness
                best_knight = knight
        
        if best_fitness > self.best_fitness_ever:
            self.best_fitness_ever = best_fitness
            self.best_path_ever = best_knight.path
            self.stagnation = 0
            print(f"🎯 Gen {self.generation}: NEW RECORD = {best_fitness}/{TARGET_FITNESS}")
        else:
            self.stagnation += 1
            if self.generation % 100 == 0:
                print(f"   Gen {self.generation}: Best = {best_fitness}/{TARGET_FITNESS} (stagnation: {self.stagnation})")
        
        return best_knight, best_fitness
    
    def tournament_selection(self, tournament_size=5):
        """Sélection par tournoi."""
        selected = random.sample(self.knights, min(tournament_size, len(self.knights)))
        selected.sort(key=lambda k: k.evaluate_fitness(), reverse=True)
        return selected[0], selected[1] if len(selected) > 1 else selected[0]
    
    def create_new_generation(self):
        """Nouvelle génération avec pression sélective adaptative."""
        # Élitisme : garde les 15% meilleurs
        elite_size = max(3, self.population_size // 7)
        sorted_knights = sorted(self.knights, key=lambda k: k.evaluate_fitness(), reverse=True)
        new_population = sorted_knights[:elite_size]
        
        # Mutation adaptative selon la stagnation
        base_mutation = 0.10
        mutation_rate = base_mutation + (self.stagnation * 0.005)
        mutation_rate = min(mutation_rate, 0.30)
        
        # Remplir avec crossover
        while len(new_population) < self.population_size:
            p1, p2 = self.tournament_selection()
            c1, c2 = p1.chromosome.crossover(p2.chromosome)
            
            c1.mutation(mutation_rate)
            c2.mutation(mutation_rate)
            
            new_population.append(Knight(c1))
            if len(new_population) < self.population_size:
                new_population.append(Knight(c2))
        
        # Injecter 10% de nouveaux individus si stagnation
        if self.stagnation > 50:
            injection_count = max(2, self.population_size // 10)
            for i in range(injection_count):
                if i < len(new_population):
                    new_population[-(i+1)] = Knight(Chromosome(use_heuristic=random.random() < 0.5))
        
        self.knights = new_population[:self.population_size]
        self.generation += 1

