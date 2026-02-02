import pygame
import sys
import os
import threading
import time
import random

# ============================================
# CONSTANTES
# ============================================
WIDTH, HEIGHT = 900, 600
FPS = 60
BG_COLOR = (20, 30, 20)
WELCOME_BG = (10, 60, 30)
BOARD_LIGHT = (200, 230, 200)
BOARD_DARK = (80, 140, 90)
PANEL_BG = (30, 30, 30)
TEXT_COLOR = (242, 244, 195)
HIGHLIGHT = (200, 60, 60)
TRACE_COLOR = (255, 215, 0, 180)
PATH_LINE_COLOR = (255, 140, 0)
SUCCESS_COLOR = (100, 255, 100)

STATE_WELCOME = "welcome"
STATE_RUNNING = "running"
STATE_SOLUTION = "solution_found"

BOARD_SIZE = 8
MOVES = [(2,1), (1,2), (-1,2), (-2,1), (-2,-1), (-1,-2), (1,-2), (2,-1)]

# ============================================
# ALGORITHME GÉNÉTIQUE PUISSANT
# ============================================

def count_degree(pos, visited):
    """Compte les voisins accessibles (Warnsdorff)."""
    x, y = pos
    count = 0
    for dx, dy in MOVES:
        nx, ny = x + dx, y + dy
        if 0 <= nx < 8 and 0 <= ny < 8 and (nx, ny) not in visited:
            count += 1
    return count

def get_warnsdorff_moves(pos, visited):
    """Retourne les mouvements triés par Warnsdorff."""
    x, y = pos
    candidates = []
    for dx, dy in MOVES:
        nx, ny = x + dx, y + dy
        if 0 <= nx < 8 and 0 <= ny < 8 and (nx, ny) not in visited:
            degree = count_degree((nx, ny), visited)
            candidates.append((degree, (nx, ny)))
    candidates.sort()
    return [pos for _, pos in candidates]

class SmartChromosome:
    """Chromosome avec génération intelligente."""
    def __init__(self, genes=None, use_warnsdorff=False):
        if genes:
            self.genes = genes
        elif use_warnsdorff:
            self.genes = self._generate_warnsdorff()
        else:
            self.genes = self._generate_guided()
    
    def _generate_warnsdorff(self):
        """Génère avec heuristique Warnsdorff."""
        pos = (0, 0)
        visited = {pos}
        genes = []
        
        for _ in range(63):
            moves = get_warnsdorff_moves(pos, visited)
            if not moves:
                # Bloqué, remplir random
                genes.extend([random.randint(0, 7) for _ in range(63 - len(genes))])
                break
            
            # Prendre le meilleur move
            next_pos = moves[0]
            dx, dy = next_pos[0] - pos[0], next_pos[1] - pos[1]
            gene = MOVES.index((dx, dy))
            genes.append(gene)
            pos = next_pos
            visited.add(pos)
        
        return genes[:63] + [random.randint(0, 7) for _ in range(max(0, 63 - len(genes)))]
    
    def _generate_guided(self):
        """Génère avec mouvements valides aléatoires."""
        pos = (0, 0)
        visited = {pos}
        genes = []
        
        for _ in range(63):
            x, y = pos
            valid = []
            for i, (dx, dy) in enumerate(MOVES):
                nx, ny = x + dx, y + dy
                if 0 <= nx < 8 and 0 <= ny < 8 and (nx, ny) not in visited:
                    valid.append(i)
            
            if valid:
                gene = random.choice(valid)
                genes.append(gene)
                dx, dy = MOVES[gene]
                pos = (pos[0] + dx, pos[1] + dy)
                visited.add(pos)
            else:
                genes.extend([random.randint(0, 7) for _ in range(63 - len(genes))])
                break
        
        return genes[:63] + [random.randint(0, 7) for _ in range(max(0, 63 - len(genes)))]
    
    def crossover(self, other):
        """Crossover deux points."""
        p1, p2 = sorted(random.sample(range(1, 63), 2))
        c1 = SmartChromosome(self.genes[:p1] + other.genes[p1:p2] + self.genes[p2:])
        c2 = SmartChromosome(other.genes[:p1] + self.genes[p1:p2] + other.genes[p2:])
        return c1, c2
    
    def mutate(self, rate=0.12):
        """Mutation adaptative."""
        for i in range(len(self.genes)):
            if random.random() < rate:
                if random.random() < 0.2:
                    self.genes[i] = random.randint(0, 7)
                else:
                    self.genes[i] = (self.genes[i] + random.choice([-1, 1])) % 8

class Knight:
    """Évaluation du chemin."""
    def __init__(self, chromo):
        self.chromosome = chromo
        self.fitness = None
        self.path = None
    
    def evaluate(self):
        """Calcule la fitness."""
        if self.fitness is not None:
            return self.fitness
        
        pos = (0, 0)
        path = [pos]
        visited = {pos}
        
        for gene in self.chromosome.genes:
            if 0 <= gene < 8:
                dx, dy = MOVES[gene]
                new_pos = (pos[0] + dx, pos[1] + dy)
                
                if (0 <= new_pos[0] < 8 and 0 <= new_pos[1] < 8 
                    and new_pos not in visited):
                    pos = new_pos
                    path.append(pos)
                    visited.add(pos)
                else:
                    break
        
        self.fitness = len(path)
        self.path = path
        return self.fitness

def run_powerful_ga(callback=None):
    """AG ultra-puissant avec forte pression sélective."""
    POP_SIZE = 200  # Population grande
    MAX_GEN = 2000
    
    # Initialisation : 50% Warnsdorff, 50% random guidé
    pop = []
    for i in range(POP_SIZE):
        use_w = random.random() < 0.5
        pop.append(Knight(SmartChromosome(use_warnsdorff=use_w)))
    
    best_ever = None
    best_fitness_ever = 0
    stagnation = 0
    
    for gen in range(MAX_GEN):
        # Évaluation
        for k in pop:
            k.evaluate()
        
        # Sort
        pop.sort(key=lambda k: k.fitness, reverse=True)
        best = pop[0]
        
        # Nouveau record
        if best.fitness > best_fitness_ever:
            best_fitness_ever = best.fitness
            best_ever = best
            stagnation = 0
            
            if callback:
                callback(gen, best.fitness, best.path)
        else:
            stagnation += 1
        
        # Solution trouvée !
        if best.fitness >= 64:
            return 64, gen, best.path
        
        # Mutation adaptative
        base_mut = 0.08
        extra_mut = min(0.20, stagnation * 0.002)
        mutation_rate = base_mut + extra_mut
        
        # Élitisme fort
        elite_ratio = 0.25 if best.fitness >= 50 else 0.15
        elite_size = max(10, int(POP_SIZE * elite_ratio))
        new_pop = pop[:elite_size]
        
        # Remplissage avec crossover + mutation
        while len(new_pop) < POP_SIZE:
            # Tournoi
            tourney = random.sample(pop[:50], min(8, 50))
            tourney.sort(key=lambda k: k.fitness, reverse=True)
            p1, p2 = tourney[0], tourney[1]
            
            # Crossover
            c1, c2 = p1.chromosome.crossover(p2.chromosome)
            c1.mutate(mutation_rate)
            c2.mutate(mutation_rate)
            
            new_pop.append(Knight(c1))
            if len(new_pop) < POP_SIZE:
                new_pop.append(Knight(c2))
        
        # Injection de diversité
        if stagnation > 100 and stagnation % 40 == 0:
            inject_count = max(5, POP_SIZE // 20)
            for i in range(inject_count):
                idx = -(i + 1)
                if idx >= -len(new_pop):
                    new_pop[idx] = Knight(SmartChromosome(use_warnsdorff=random.random() < 0.7))
        
        pop = new_pop
        
        # Arrêt si stagnation extrême
        if stagnation > 400:
            # Réinitialiser
            pop = []
            for i in range(POP_SIZE):
                use_w = random.random() < 0.7  # Plus d'heuristique
                pop.append(Knight(SmartChromosome(use_warnsdorff=use_w)))
            stagnation = 0
    
    return best_fitness_ever, MAX_GEN, best_ever.path if best_ever else [(0,0)]

# ============================================
# INTERFACE PYGAME
# ============================================

def load_knight_image(square_size):
    path = os.path.join(os.path.dirname(__file__), "knight.png")
    if os.path.exists(path):
        try:
            img = pygame.image.load(path).convert_alpha()
            return pygame.transform.smoothscale(img, (square_size, square_size))
        except:
            return None
    return None

def draw_centered_text(surface, text, font, color, center):
    s = font.render(text, True, color)
    surface.blit(s, s.get_rect(center=center))

def draw_button(surface, rect, text, font, base_color, hover_color, mouse_pos, active=False):
    hovered = rect.collidepoint(mouse_pos)
    color = hover_color if hovered else base_color
    pygame.draw.rect(surface, color, rect, border_radius=8)
    border_col = (60, 60, 60) if not active else (180, 140, 90)
    pygame.draw.rect(surface, border_col, rect, width=2, border_radius=8)
    s = font.render(text, True, TEXT_COLOR)
    surface.blit(s, s.get_rect(center=rect.center))
    return hovered

def draw_welcome(screen, fonts):
    screen.fill(WELCOME_BG)
    title_font, sub_font = fonts
    draw_centered_text(screen, "KNIGHT'S TOUR", title_font, TEXT_COLOR, (WIDTH // 2, HEIGHT // 2 - 110))
    draw_centered_text(screen, "Algorithme Génétique Optimisé", sub_font, TEXT_COLOR, (WIDTH // 2, HEIGHT // 2 - 50))
    
    info_font = pygame.font.SysFont(None, 20)
    draw_centered_text(screen, "Solution complète en ~30-120 secondes", info_font, (180, 180, 180), (WIDTH // 2, HEIGHT // 2 - 10))
    
    bw, bh = 320, 64
    button_rect = pygame.Rect((WIDTH - bw) // 2, (HEIGHT // 2) + 40, bw, bh)
    mouse_pos = pygame.mouse.get_pos()
    draw_button(screen, button_rect, "Lancer l'AG", sub_font, (112, 66, 20), (150, 100, 40), mouse_pos)
    return button_rect

def compute_board_layout(panel_width=300, margin=20):
    avail_w = WIDTH - panel_width - 2 * margin
    avail_h = HEIGHT - 2 * margin
    board_pixels = min(avail_w, avail_h)
    square_size = board_pixels // BOARD_SIZE
    board_pixels = square_size * BOARD_SIZE
    board_left = margin + (avail_w - board_pixels) // 2
    board_top = margin + (avail_h - board_pixels) // 2
    panel_left = WIDTH - panel_width
    return board_left, board_top, square_size, panel_left, panel_width

def draw_board(surface, top_left, square_size):
    bx, by = top_left
    for r in range(BOARD_SIZE):
        for c in range(BOARD_SIZE):
            color = BOARD_LIGHT if (r + c) % 2 == 0 else BOARD_DARK
            rect = pygame.Rect(bx + c * square_size, by + r * square_size, square_size, square_size)
            pygame.draw.rect(surface, color, rect)

def draw_knight(surface, top_left, square_size, position, knight_img=None):
    bx, by = top_left
    r, c = position
    x = bx + c * square_size
    y = by + r * square_size
    rect = pygame.Rect(x, y, square_size, square_size)
    
    if knight_img:
        surface.blit(knight_img, rect.topleft)
    else:
        # Dessiner un cavalier stylisé
        cx, cy = rect.centerx, rect.centery
        size = square_size // 3
        # Corps
        pygame.draw.circle(surface, (255, 200, 100), (cx, cy), size)
        pygame.draw.circle(surface, (0, 0, 0), (cx, cy), size, 2)
        # Tête
        pygame.draw.circle(surface, (255, 200, 100), (cx, cy - size), size // 2)
        pygame.draw.circle(surface, (0, 0, 0), (cx, cy - size), size // 2, 2)

def draw_solution(surface, top_left, square_size, path, current_index):
    """Dessine la solution."""
    if not path:
        return
    
    bx, by = top_left
    number_font = pygame.font.SysFont(None, max(14, square_size // 3))
    
    # Lignes
    for i in range(min(current_index, len(path) - 1)):
        r1, c1 = path[i]
        r2, c2 = path[i + 1]
        x1 = bx + c1 * square_size + square_size // 2
        y1 = by + r1 * square_size + square_size // 2
        x2 = bx + c2 * square_size + square_size // 2
        y2 = by + r2 * square_size + square_size // 2
        pygame.draw.line(surface, PATH_LINE_COLOR, (x1, y1), (x2, y2), 3)
    
    # Traces et numéros
    for i in range(current_index + 1):
        if i >= len(path):
            break
        r, c = path[i]
        rect = pygame.Rect(bx + c * square_size, by + r * square_size, square_size, square_size)
        trace_surf = pygame.Surface((square_size, square_size), pygame.SRCALPHA)
        pygame.draw.circle(trace_surf, TRACE_COLOR, (square_size // 2, square_size // 2), square_size // 3)
        surface.blit(trace_surf, rect.topleft)
        
        txt = number_font.render(str(i + 1), True, (0, 0, 0))
        surface.blit(txt, txt.get_rect(center=rect.center))
    
    # Cavalier
    if 0 <= current_index < len(path):
        draw_knight(surface, top_left, square_size, path[current_index])

def draw_panel(surface, panel_left, panel_width, generation, best_fit, status, elapsed, current_index=None, total=None, auto_play=False):
    pygame.draw.rect(surface, PANEL_BG, (panel_left, 0, panel_width, HEIGHT))
    
    title_font = pygame.font.SysFont(None, 24, bold=True)
    info_font = pygame.font.SysFont(None, 20)
    
    x = panel_left + 20
    y = 20
    
    surface.blit(title_font.render("AG - Knight's Tour", True, TEXT_COLOR), (x, y))
    y += 40
    
    surface.blit(info_font.render(f"Génération: {generation}", True, TEXT_COLOR), (x, y))
    y += 28
    
    color = SUCCESS_COLOR if best_fit >= 64 else TEXT_COLOR
    surface.blit(info_font.render(f"Fitness: {best_fit}/64", True, color), (x, y))
    y += 28
    
    surface.blit(info_font.render(f"Temps: {elapsed:.1f}s", True, TEXT_COLOR), (x, y))
    y += 28
    
    surface.blit(info_font.render(f"Statut: {status}", True, color), (x, y))
    y += 35
    
    if current_index is not None and total:
        surface.blit(info_font.render(f"Coup: {current_index + 1}/{total}", True, TEXT_COLOR), (x, y))

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Knight's Tour - AG Optimisé")
    clock = pygame.time.Clock()
    
    title_font = pygame.font.SysFont("serif", 56, bold=True)
    sub_font = pygame.font.SysFont("serif", 24, bold=True)
    fonts = (title_font, sub_font)
    
    state = STATE_WELCOME
    generation = 0
    best_fit = 0
    status = "En attente..."
    
    panel_width = 300
    board_left, board_top, square_size, panel_left, panel_width = compute_board_layout(panel_width)
    knight_img = load_knight_image(square_size)
    globals()['knight_img'] = knight_img
    
    solution_path = None
    current_step_index = 0
    ga_thread = None
    is_solving = False
    start_time = 0
    elapsed_time = 0
    
    auto_play = False
    auto_delay = 100
    last_auto_time = 0
    
    running = True
    while running:
        mouse_pos = pygame.mouse.get_pos()
        
        btn_w = panel_width - 40
        btn_h = 45
        spacing = 15
        btn_x = panel_left + (panel_width - btn_w) // 2
        start_y = HEIGHT - 230
        
        prev_btn = pygame.Rect(btn_x, start_y, btn_w, btn_h)
        next_btn = pygame.Rect(btn_x, start_y + btn_h + spacing, btn_w, btn_h)
        auto_btn = pygame.Rect(btn_x, start_y + 2 * (btn_h + spacing), btn_w, btn_h)
        restart_btn = pygame.Rect(btn_x, start_y + 3 * (btn_h + spacing), btn_w, btn_h)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mx, my = event.pos
                
                if state == STATE_WELCOME:
                    start_rect = pygame.Rect((WIDTH - 320) // 2, (HEIGHT // 2) + 40, 320, 64)
                    if start_rect.collidepoint((mx, my)) and not is_solving:
                        state = STATE_RUNNING
                        is_solving = True
                        start_time = time.time()
                        
                        def update_progress(gen, fitness, path):
                            nonlocal generation, best_fit, solution_path
                            generation = gen
                            best_fit = fitness
                            solution_path = path
                        
                        def run_solver():
                            nonlocal is_solving, status, state, solution_path, elapsed_time
                            fitness, gen, path = run_powerful_ga(callback=update_progress)
                            elapsed_time = time.time() - start_time
                            is_solving = False
                            solution_path = path
                            status = "Solution complète!" if fitness >= 64 else f"Partielle ({fitness})"
                            state = STATE_SOLUTION
                        
                        ga_thread = threading.Thread(target=run_solver, daemon=True)
                        ga_thread.start()
                
                elif state == STATE_SOLUTION:
                    if prev_btn.collidepoint((mx, my)) and not auto_play:
                        current_step_index = max(current_step_index - 1, 0)
                    elif next_btn.collidepoint((mx, my)) and not auto_play:
                        current_step_index = min(current_step_index + 1, len(solution_path) - 1)
                    elif auto_btn.collidepoint((mx, my)):
                        auto_play = not auto_play
                        last_auto_time = pygame.time.get_ticks()
                        if auto_play and current_step_index >= len(solution_path) - 1:
                            current_step_index = 0
                    elif restart_btn.collidepoint((mx, my)):
                        state = STATE_WELCOME
                        solution_path = None
                        current_step_index = 0
                        auto_play = False
                        generation = 0
                        best_fit = 0
                        status = "En attente..."
                        elapsed_time = 0
        
        if state == STATE_SOLUTION and auto_play and solution_path:
            now = pygame.time.get_ticks()
            if now - last_auto_time >= auto_delay:
                if current_step_index < len(solution_path) - 1:
                    current_step_index += 1
                    last_auto_time = now
                else:
                    auto_play = False
        
        if is_solving:
            elapsed_time = time.time() - start_time
            status = "Résolution..."
        
        screen.fill(BG_COLOR)
        
        if state == STATE_WELCOME:
            draw_welcome(screen, fonts)
        else:
            draw_board(screen, (board_left, board_top), square_size)
            if solution_path:
                draw_solution(screen, (board_left, board_top), square_size, solution_path, current_step_index)
            
            draw_panel(screen, panel_left, panel_width, generation, best_fit, status, elapsed_time,
                      current_step_index if solution_path else None,
                      len(solution_path) if solution_path else None,
                      auto_play)
            
            if state == STATE_SOLUTION:
                draw_button(screen, prev_btn, "◀ PRÉCÉDENT", sub_font, (100, 100, 100), (140, 140, 140), mouse_pos)
                draw_button(screen, next_btn, "SUIVANT ▶", sub_font, (100, 100, 100), (140, 140, 140), mouse_pos)
                auto_label = "⏸ STOP" if auto_play else "▶ AUTO"
                draw_button(screen, auto_btn, auto_label, sub_font, (80, 120, 200), (110, 150, 230), mouse_pos, active=auto_play)
                draw_button(screen, restart_btn, "🔄 RECOMMENCER", sub_font, (200, 80, 60), (230, 110, 90), mouse_pos)
        
        pygame.display.flip()
        clock.tick(FPS)
    
    pygame.quit()

if __name__ == "__main__":
    main()