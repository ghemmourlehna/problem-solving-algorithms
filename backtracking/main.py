import time
from knight_tour_basic import backtracking as backtrack_basic
from csp import backtracking as backtrack_csp

def visualize_solution(solution):
    if solution is None:
        print(" Pas de solution!")
        return
    
    board = [[0 for _ in range(8)] for _ in range(8)]
    for move_num, (x, y) in enumerate(solution, 1):
        board[y][x] = move_num
    
    print("\n" + "=" * 50)
    print(" ÉCHIQUIER (numéro du coup)")
    print("=" * 50)
    print("  ", end="")
    for col in range(8):
        print(f"{col:3}", end="")
    print()
    print("-" * 35)
    
    for row in range(8):
        print(f"{row}|", end="")
        for col in range(8):
            print(f"{board[row][col]:3}", end="")
        print()
    print()

def print_path(solution):
    
    if solution is None:
        return
    
    print(" CHEMIN PARCOURU:")
    for i, (x, y) in enumerate(solution, 1):
        print(f"Coup {i:2d}: ({x}, {y})", end="  ")
        if i % 8 == 0:
            print()
    print("\n")

print("=" * 60)
print("=== KNIGHT'S TOUR ===")
print("=" * 60)

print("\n*** 1. Backtracking SIMPLE ***")
start = time.time()
sol1 = backtrack_basic([(0, 0)])
elapsed1 = time.time() - start

if sol1:
    print(f" Solution en {elapsed1:.2f}s")
    visualize_solution(sol1)
    print_path(sol1)
else:
    print(f" Pas de solution en {elapsed1:.2f}s")

print("\n*** 2. Backtracking + MRV + LCV ***")
start = time.time()
sol2 = backtrack_csp([(0, 0)])
elapsed2 = time.time() - start

if sol2:
    print(f" Solution en {elapsed2:.2f}s")
    visualize_solution(sol2)
    print_path(sol2)
else:
    print(f" Pas de solution en {elapsed2:.2f}s")

print("=" * 60)
