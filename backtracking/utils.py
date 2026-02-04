MOVES = [
    (2, 1), (1, 2), (-1, 2), (-2, 1),
    (-2, -1), (-1, -2), (1, -2), (2, -1)
]


SUCCESSORS_CACHE = {}

def _build_cache():
    
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
    return [pos for pos in SUCCESSORS_CACHE[(x, y)] if pos not in visited]


def MRV_LCV(successors, visited):
    
    mrv_scores = {
        pos: len([p for p in SUCCESSORS_CACHE[pos] if p not in visited])
        for pos in successors
    }
    
    
    min_val = min(mrv_scores.values())
    mrv_candidates = [pos for pos in successors if mrv_scores[pos] == min_val]
    
    def lcv_score(pos):
        
        total = 0
        for neighbor in SUCCESSORS_CACHE[pos]:
            if neighbor not in visited:
                
                total += len([p for p in SUCCESSORS_CACHE[neighbor] 
                             if p not in visited and p != pos])
        return total

    return sorted(mrv_candidates, key=lcv_score, reverse=True)
    