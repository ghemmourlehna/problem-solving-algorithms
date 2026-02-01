from Nodebfs import Node
from queue import Queue
from RushHourPuzzle import RushHourPuzzle

class Search:

    """ Uninformed/Blind Search """
    @staticmethod
    def breadthFirst(initial_state):
        
        initial_node = Node(initial_state)   
        # Check if the start element is the goal
        if initial_node.state.isGoal():
            return initial_node, 0

        # Create the OPEN FIFO queue and the CLOSED list
        open = Queue() # A FIFO queue
        open.put(initial_node)
        closed = list()
       
        explored_count = 0
        while True:
            print (f' explored_count {explored_count} ')
            # Check if the OPEN queue is empty => goal not found 
            if open.empty():
                return None,  explored_count          
            # Get the first element of the OPEN queue
            current = open.get()            
            # Put the current node in the CLOSED list
            closed.append(current)
            explored_count +=1 
            # Generate the successors of the current node
            for (action, successor) in current.state.successorFunction():                
                child = Node(successor, current, action)
                # Check if the child is not in the OPEN queue and the CLOSED list
                if (child.state.board not in [node.state.board for node in closed] and \
                    child.state.board not in [node.state.board for node in list(open.queue)]):
                    # Check if the child is the goal
                    if child.state.isGoal():
                        print ("Goal reached")
                        return child,  explored_count
                    # Put the child in the OPEN queue 
                    open.put(child)     
            
def main():

    initial_state = RushHourPuzzle('2-b.csv')
    RushHourPuzzle.printRushHourBoard(initial_state.board)   
    goal_node, explored_count = Search.breadthFirst(initial_state)
    print(f"Path cost: {goal_node.g}")
    print(f"Number of explored_counts: {explored_count}")
    print("Moves: {}".format(" ".join(map(str, goal_node.getSolution()))))

if __name__ == "__main__":
    main()
