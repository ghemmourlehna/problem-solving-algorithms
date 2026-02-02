from nodeaetoile import Node
from queue import Queue
from RushHourPuzzle import RushHourPuzzle
import heapq
import itertools 

class Search:
    @staticmethod
    def a_star(initial_state, heuristic_choice=3):
        initial_node = Node(initial_state, heuristic=heuristic_choice)
        if initial_node.state.isGoal():
            return initial_node, 0

        open_list = []
        counter = itertools.count()  
        heapq.heappush(open_list, (initial_node.f, next(counter), initial_node))
        closed_set = set()

        step = 0
        while open_list:
            print(f'*** Step {step} ***')
            step += 1

            _, _, current = heapq.heappop(open_list)
            state_key = str(current.state.board)

            if state_key in closed_set:
                continue
            closed_set.add(state_key)

            if current.state.isGoal():
                print("Goal reached!")
                return current, step

            for (action, successor) in current.state.successorFunction():
                child = Node(successor, current, action, heuristic=heuristic_choice)
                child_key = str(child.state.board)
                print("Heuristique utilisée :", initial_node.heuristic_used)
                if child_key not in closed_set:
                    heapq.heappush(open_list, (child.f, next(counter), child))

        print("No solution found.")
        return None, step


def main():

    initial_state = RushHourPuzzle('2-a.csv')
    RushHourPuzzle.printRushHourBoard(initial_state.board)   
    goal_node, explored_count = Search.a_star(initial_state)
    print(f"Path cost: {goal_node.g}")
    print(f"Number of explored_counts: {explored_count}")
    print("Moves: {}".format(" ".join(map(str, goal_node.getSolution()))))

if __name__ == "__main__":
    main()



