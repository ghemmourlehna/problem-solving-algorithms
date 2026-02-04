import pygame
import sys
import os
import threading
import time

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
SUCCESS_COLOR = (100, 255, 100)
PATH_LINE_COLOR = (255, 140, 0)

STATE_WELCOME = "welcome"
STATE_ALGORITHM_SELECT = "algorithm_select"
STATE_SOLVING = "solving"
STATE_SOLUTION = "solution"

BOARD_SIZE = 8

# ============================================
# ALGORITHMES KNIGHT'S TOUR
# ============================================
MOVES = [
    (2, 1), (1, 2), (-1, 2), (-2, 1),
    (-2, -1), (-1, -2), (1, -2), (2, -1)
]

SUCCESSORS_CACHE = {}

def _build_cache():
    """Construit le cache des successeurs."""
    for x in range(8):
        for y in range(8):
            valid = []
            for dx, dy in MOVES:
                nx, ny = x + dx, y + dy
                if 0 <= nx < 8 and 0 <= ny < 8:
                    valid.append((nx, ny))
            SUCCESSORS_CACHE[(x, y)] = valid

_build_cache()

def successor_fct(x, y, visited):
    """Retourne les successeurs non visités."""
    return [pos for pos in SUCCESSORS_CACHE[(x, y)] if pos not in visited]

def MRV(successors, visited):
    """Minimum Remaining Values - Trie par nombre de coups futurs."""
    return sorted(
        successors,
        key=lambda pos: len([p for p in SUCCESSORS_CACHE[pos] if p not in visited])
    )

def LCV(successors, visited):
    """Least Constraining Value - Simplifié."""
    return successors

# ============================================
# BACKTRACKING SIMPLE
# ============================================
def backtracking_simple(assignment, callback=None):
    """Backtracking simple sans heuristiques."""
    if callback:
        callback(list(assignment))
    
    if len(assignment) == 64:
        return assignment
    
    x, y = assignment[-1]
    visited = set(assignment)
    successors = successor_fct(x, y, visited)
    
    for nx, ny in successors:
        assignment.append((nx, ny))
        result = backtracking_simple(assignment, callback)
        if result is not None:
            return result
        assignment.pop()
    
    return None

# ============================================
# BACKTRACKING CSP (MRV + LCV)
# ============================================
def backtracking_csp(assignment, callback=None):
    """Backtracking avec heuristiques MRV + LCV."""
    if callback:
        callback(list(assignment))
    
    if len(assignment) == 64:
        return assignment
    
    x, y = assignment[-1]
    visited = set(assignment)
    successors = successor_fct(x, y, visited)
    
    # Appliquer heuristiques
    successors = MRV(successors, visited)
    successors = LCV(successors, visited)
    
    for nx, ny in successors:
        assignment.append((nx, ny))
        result = backtracking_csp(assignment, callback)
        if result is not None:
            return result
        assignment.pop()
    
    return None

# ============================================
# CHARGEMENT DES ASSETS
# ============================================
def load_knight_image(square_size):
    path = os.path.join(os.path.dirname(__file__), "knight.png")
    if os.path.exists(path):
        try:
            img = pygame.image.load(path).convert_alpha()
            img = pygame.transform.smoothscale(img, (square_size, square_size))
            return img
        except Exception:
            return None
    return None

def load_board_image():
    names = ["chess.jpg", "chess.png", "Chess.jpg"]
    base = os.path.dirname(__file__)
    for name in names:
        path = os.path.join(base, name)
        if os.path.exists(path):
            try:
                return pygame.image.load(path).convert()
            except Exception:
                continue
    return None

def load_background_image():
    names = ["background.jpg", "baclground.jpg", "Background.jpg"]
    base = os.path.dirname(__file__)
    for name in names:
        path = os.path.join(base, name)
        if os.path.exists(path):
            try:
                img = pygame.image.load(path).convert()
                return pygame.transform.smoothscale(img, (WIDTH, HEIGHT))
            except Exception:
                continue
    return None

# ============================================
# FONCTIONS DE DESSIN
# ============================================
def draw_centered_text(surface, text, font, color, center):
    s = font.render(text, True, color)
    r = s.get_rect(center=center)
    surface.blit(s, r)

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
    bg = globals().get("BG_IMAGE")
    if bg:
        screen.blit(bg, (0, 0))
    else:
        screen.fill(WELCOME_BG)
    
    title_font, sub_font = fonts
    draw_centered_text(screen, "KNIGHT'S TOUR", title_font, TEXT_COLOR, (WIDTH // 2, HEIGHT // 2 - 110))
    draw_centered_text(screen, "La Randonnée du Cavalier", sub_font, TEXT_COLOR, (WIDTH // 2, HEIGHT // 2 - 50))
    
    bw, bh = 320, 64
    bx = (WIDTH - bw) // 2
    by = (HEIGHT // 2) + 20
    button_rect = pygame.Rect(bx, by, bw, bh)
    mouse_pos = pygame.mouse.get_pos()
    draw_button(screen, button_rect, "Commencer", sub_font, (112, 66, 20), (93, 54, 16), mouse_pos)
    return button_rect

def draw_algorithm_select(screen, fonts):
    bg = globals().get("BG_IMAGE")
    if bg:
        screen.blit(bg, (0, 0))
    else:
        screen.fill(WELCOME_BG)
    
    title_font, sub_font = fonts
    draw_centered_text(screen, "Choisir l'algorithme", title_font, TEXT_COLOR, (WIDTH // 2, 100))
    
    mouse_pos = pygame.mouse.get_pos()
    
    # Bouton Backtracking Simple
    btn1_rect = pygame.Rect(WIDTH // 2 - 200, HEIGHT // 2 - 80, 400, 60)
    draw_button(screen, btn1_rect, "Backtracking Simple", sub_font, (80, 120, 200), (110, 150, 230), mouse_pos)
    
    # Bouton CSP avec heuristiques
    btn2_rect = pygame.Rect(WIDTH // 2 - 200, HEIGHT // 2 + 20, 400, 60)
    draw_button(screen, btn2_rect, "CSP (MRV + LCV)", sub_font, (200, 80, 80), (230, 110, 110), mouse_pos)
    
    # Texte explicatif
    info_font = pygame.font.SysFont(None, 20)
    y = HEIGHT // 2 + 120
    texts = [
        "Backtracking Simple : Exploration basique",
        "CSP avec heuristiques : Plus intelligent et rapide"
    ]
    for text in texts:
        draw_centered_text(screen, text, info_font, (180, 180, 180), (WIDTH // 2, y))
        y += 30
    
    return btn1_rect, btn2_rect

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

def draw_solution(surface, top_left, square_size, path, current_index):
    """Dessine la solution avec chemin qui se construit au fur et à mesure."""
    if not path:
        return
    
    bx, by = top_left
    number_font = pygame.font.SysFont(None, max(18, int(square_size // 2.5)), bold=True)
    
    # 1. Dessiner SEULEMENT les traits jusqu'à current_index (le chemin se construit)
    for i in range(current_index):
        if i >= len(path) - 1:
            break
        x1, y1 = path[i]
        x2, y2 = path[i + 1]
        
        # Convertir en coordonnées écran
        px1 = bx + x1 * square_size + square_size // 2
        py1 = by + y1 * square_size + square_size // 2
        px2 = bx + x2 * square_size + square_size // 2
        py2 = by + y2 * square_size + square_size // 2
        
        # Trait orange vif
        line_color = (255, 165, 0)
        line_width = 6
        
        pygame.draw.line(surface, line_color, (px1, py1), (px2, py2), line_width)
    
    # 2. Dessiner SEULEMENT les cercles jusqu'à current_index (ils se construisent)
    for i in range(current_index + 1):
        if i >= len(path):
            break
        x, y = path[i]
        
        # Convertir en coordonnées écran
        px = bx + x * square_size + square_size // 2
        py = by + y * square_size + square_size // 2
        
        # Rayon du cercle
        radius = int(square_size * 0.3)
        
        # Couleur du cercle (jaune doré riche et élégant)
        circle_color = (255, 215, 0)  # Jaune doré classique
        
        # Dessiner le cercle
        pygame.draw.circle(surface, circle_color, (int(px), int(py)), radius)
        pygame.draw.circle(surface, (50, 50, 50), (int(px), int(py)), radius, 4)  # Bordure grise foncée plus visible
        
        # Numéro de coup
        txt = number_font.render(str(i + 1), True, (0, 0, 0))
        surface.blit(txt, txt.get_rect(center=(int(px), int(py))))
    
    # 3. Dessiner le cavalier
    if path and 0 <= current_index < len(path):
        x, y = path[current_index]
        draw_knight(surface, top_left, square_size, (x, y), knight_img=globals().get("KNIGHT_IMAGE"))

def draw_knight(surface, top_left, square_size, position, knight_img=None):
    bx, by = top_left
    x, y = position
    px = bx + x * square_size
    py = by + y * square_size
    rect = pygame.Rect(px, py, square_size, square_size)
    
    if knight_img:
        img = pygame.transform.smoothscale(knight_img, (square_size, square_size))
        surface.blit(img, rect.topleft)
    else:
        # Dessiner un cavalier stylisé en orange/doré
        cx, cy = rect.centerx, rect.centery
        size = square_size // 3
        # Corps
        pygame.draw.circle(surface, (255, 200, 100), (cx, cy), size)
        pygame.draw.circle(surface, (0, 0, 0), (cx, cy), size, 2)
        # Tête
        pygame.draw.circle(surface, (255, 200, 100), (cx, cy - size), size // 2)
        pygame.draw.circle(surface, (0, 0, 0), (cx, cy - size), size // 2, 2)

def draw_panel(surface, panel_left, panel_width, algorithm, status, elapsed_time, current_index=None, total=None, auto_play=False):
    pygame.draw.rect(surface, PANEL_BG, (panel_left, 0, panel_width, HEIGHT))
    
    title_font = pygame.font.SysFont(None, 24, bold=True)
    info_font = pygame.font.SysFont(None, 20)
    
    x = panel_left + 20
    y = 20
    
    # Titre
    surface.blit(title_font.render("KNIGHT'S TOUR", True, TEXT_COLOR), (x, y))
    y += 40
    
    # Algorithme
    algo_text = "Backtracking Simple" if algorithm == "simple" else "CSP (MRV + LCV)"
    surface.blit(info_font.render(f"Algo: {algo_text}", True, TEXT_COLOR), (x, y))
    y += 30
    
    # Statut
    status_color = SUCCESS_COLOR if "Solution" in status else TEXT_COLOR
    surface.blit(info_font.render(f"Statut:", True, TEXT_COLOR), (x, y))
    y += 25
    lines = status.split('\n')
    for line in lines:
        surface.blit(info_font.render(line, True, status_color), (x, y))
        y += 22
    
    y += 10
    
    # Temps
    surface.blit(info_font.render(f"Temps: {elapsed_time:.2f}s", True, TEXT_COLOR), (x, y))
    y += 30
    
    # Position actuelle
    if current_index is not None and total is not None:
        surface.blit(info_font.render(f"Coup: {current_index + 1}/{total}", True, TEXT_COLOR), (x, y))
        y += 30
    
    # Mode auto
    if auto_play:
        surface.blit(info_font.render("Mode: AUTO", True, HIGHLIGHT), (x, y))
    else:
        surface.blit(info_font.render("Mode: MANUEL", True, TEXT_COLOR), (x, y))

# ============================================
# FONCTION PRINCIPALE
# ============================================
def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Knight's Tour - Backtracking Visualizer")
    clock = pygame.time.Clock()
    
    # Fonts
    cinzel_path = pygame.font.match_font("Cinzel Decorative") or pygame.font.match_font("Cinzel")
    if cinzel_path:
        title_font = pygame.font.Font(cinzel_path, 56)
        sub_font = pygame.font.Font(cinzel_path, 24)
    else:
        title_font = pygame.font.SysFont("serif", 56, bold=True)
        sub_font = pygame.font.SysFont("serif", 24, bold=True)
    fonts = (title_font, sub_font)
    
    # État initial
    state = STATE_WELCOME
    algorithm_choice = None
    status = "En attente..."
    
    # Board
    panel_width = 300
    board_left, board_top, square_size, panel_left, panel_width = compute_board_layout(panel_width)
    knight_img = load_knight_image(square_size)
    globals()["KNIGHT_IMAGE"] = knight_img
    globals()["BG_IMAGE"] = load_background_image()
    globals()["BOARD_IMAGE"] = load_board_image()
    
    # Solution
    solution_path = None
    current_step_index = 0
    solving_thread = None
    is_solving = False
    elapsed_time = 0
    start_time = 0
    
    # Autoplay
    auto_play = False
    auto_delay = 200
    last_auto_time = 0
    
    running = True
    while running:
        mouse_pos = pygame.mouse.get_pos()
        
        # BOUTONS
        btn_w = panel_width - 40
        btn_h = 45
        spacing = 15
        btn_x = panel_left + (panel_width - btn_w) // 2
        start_y = HEIGHT - 220
        
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
                elif state == STATE_SOLUTION and not auto_play:
                    if event.key == pygame.K_RIGHT:
                        current_step_index = min(current_step_index + 1, len(solution_path) - 1)
                    elif event.key == pygame.K_LEFT:
                        current_step_index = max(current_step_index - 1, 0)
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mx, my = event.pos
                
                if state == STATE_WELCOME:
                    start_rect = pygame.Rect((WIDTH - 320) // 2, (HEIGHT // 2) + 20, 320, 64)
                    if start_rect.collidepoint((mx, my)):
                        state = STATE_ALGORITHM_SELECT
                
                elif state == STATE_ALGORITHM_SELECT:
                    btn1, btn2 = draw_algorithm_select(screen, fonts)
                    if btn1.collidepoint((mx, my)):
                        algorithm_choice = "simple"
                        state = STATE_SOLVING
                        
                        def run_solver():
                            nonlocal solution_path, status, state, is_solving, elapsed_time, start_time
                            is_solving = True
                            status = "Résolution en cours..."
                            start_time = time.time()
                            
                            result = backtracking_simple([(0, 0)])
                            
                            elapsed_time = time.time() - start_time
                            is_solving = False
                            
                            if result:
                                solution_path = result
                                status = f"Solution trouvée!\n{len(result)} coups"
                                state = STATE_SOLUTION
                            else:
                                status = "Aucune solution"
                        
                        solving_thread = threading.Thread(target=run_solver, daemon=True)
                        solving_thread.start()
                    
                    elif btn2.collidepoint((mx, my)):
                        algorithm_choice = "csp"
                        state = STATE_SOLVING
                        
                        def run_solver():
                            nonlocal solution_path, status, state, is_solving, elapsed_time, start_time
                            is_solving = True
                            status = "Résolution en cours..."
                            start_time = time.time()
                            
                            result = backtracking_csp([(0, 0)])
                            
                            elapsed_time = time.time() - start_time
                            is_solving = False
                            
                            if result:
                                solution_path = result
                                status = f"Solution trouvée!\n{len(result)} coups"
                                state = STATE_SOLUTION
                            else:
                                status = "Aucune solution"
                        
                        solving_thread = threading.Thread(target=run_solver, daemon=True)
                        solving_thread.start()
                
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
                        state = STATE_ALGORITHM_SELECT
                        solution_path = None
                        current_step_index = 0
                        auto_play = False
                        elapsed_time = 0
        
        # AUTOPLAY
        if state == STATE_SOLUTION and auto_play and solution_path:
            now = pygame.time.get_ticks()
            if now - last_auto_time >= auto_delay:
                if current_step_index < len(solution_path) - 1:
                    current_step_index += 1
                    last_auto_time = now
                else:
                    auto_play = False
        
        # Mise à jour du temps pendant la résolution
        if is_solving:
            elapsed_time = time.time() - start_time
        
        # DRAWING
        screen.fill(BG_COLOR)
        
        if state == STATE_WELCOME:
            draw_welcome(screen, fonts)
        
        elif state == STATE_ALGORITHM_SELECT:
            draw_algorithm_select(screen, fonts)
        
        elif state == STATE_SOLVING or state == STATE_SOLUTION:
            # Board
            board_img = globals().get("BOARD_IMAGE")
            board_rect = pygame.Rect(board_left, board_top, square_size * BOARD_SIZE, square_size * BOARD_SIZE)
            if board_img:
                img = pygame.transform.smoothscale(board_img, (board_rect.width, board_rect.height))
                screen.blit(img, board_rect.topleft)
            else:
                draw_board(screen, (board_left, board_top), square_size)
            
            # Solution
            if state == STATE_SOLUTION and solution_path:
                draw_solution(screen, (board_left, board_top), square_size, solution_path, current_step_index)
            
            # Panel
            draw_panel(screen, panel_left, panel_width, algorithm_choice, status, elapsed_time,
                      current_step_index if solution_path else None,
                      len(solution_path) if solution_path else None,
                      auto_play)
            
            # Boutons (seulement si solution trouvée)
            if state == STATE_SOLUTION:
                draw_button(screen, prev_btn, "◀ PRÉCÉDENT", sub_font, (100, 100, 100), (140, 140, 140), mouse_pos)
                draw_button(screen, next_btn, "SUIVANT ▶", sub_font, (100, 100, 100), (140, 140, 140), mouse_pos)
                auto_label = "⏸ STOP AUTO" if auto_play else "▶ AUTO PLAY"
                draw_button(screen, auto_btn, auto_label, sub_font, (80, 120, 200), (110, 150, 230), mouse_pos, active=auto_play)
                draw_button(screen, restart_btn, "🔄 RECOMMENCER", sub_font, (200, 80, 60), (230, 110, 90), mouse_pos)
        
        pygame.display.flip()
        clock.tick(FPS)
    
    pygame.quit()

if __name__ == "__main__":
    main()