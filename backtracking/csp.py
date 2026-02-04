from utils import successor_fct, MRV_LCV


def backtracking(assignment):
    if len(assignment) == 64:
        return assignment
    
    x, y = assignment[-1]
    visited = set(assignment)
    successors = successor_fct(x, y, visited)
    
    successors = MRV_LCV(successors, visited)

    
    
    for nx, ny in successors:
        assignment.append((nx, ny))
        result = backtracking(assignment)
        if result is not None:
            return result
        assignment.pop()
    
    return None
