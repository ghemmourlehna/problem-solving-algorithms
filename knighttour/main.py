from population import Population
from chromosome import TARGET_FITNESS
 #============================================
# ALGORITHME GÉNÉTIQUE
# ============================================
def run_genetic_algorithm(population_size=150, max_generations=1000):
    """Exécute l'AG optimisé."""
    print("🧬 Initialisation de la population...")
    population = Population(population_size)
    
    for gen in range(max_generations):
        best_knight, best_fitness = population.evaluate()
        
        # Solution trouvée !
        if best_fitness >= TARGET_FITNESS:
            print(f"\n🎉 SOLUTION COMPLÈTE trouvée à la génération {gen}!")
            return best_fitness, gen, best_knight.path
        
        population.create_new_generation()
        
        # Arrêt prématuré si stagnation trop longue
        if population.stagnation > 200:
            print(f"\n⚠️ Stagnation détectée. Redémarrage avec nouvelle population...")
            population = Population(population_size)
    
    # Retourner la meilleure solution partielle
    print(f"\n⚠️ Max générations atteintes. Meilleur : {population.best_fitness_ever}/{TARGET_FITNESS}")
    return population.best_fitness_ever, max_generations, population.best_path_ever

# ============================================
# POINT D'ENTRÉE
# ============================================
def main():
    """Point d'entrée principal."""
    print("=" * 60)
    print("🧬 KNIGHT'S TOUR - ALGORITHME GÉNÉTIQUE OPTIMISÉ")
    print("=" * 60)
    
    result = run_genetic_algorithm(
        population_size=150,      # Population plus grande = convergence plus rapide
        max_generations=1000
    )
    
    return result

if __name__ == "__main__":
    fitness, gen, path = main()
    print(f"\n📊 Résultat final :")
    print(f"   Fitness : {fitness}/{TARGET_FITNESS}")
    print(f"   Générations : {gen}")
    if path:
        print(f"   Chemin : {path[:10]}...")