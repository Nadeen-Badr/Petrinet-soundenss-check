from collections import defaultdict

# define Transaction class
class Marking:
    def __init__(self, i):
        self.id = i

        self.reqPlaces = set()
        self.nextP = set()
        # Boolean flag to indicate if this marking has been executed(visited) or not
        self.excuted = False

    def fire(self, current):
         # Method that fires the marking transition by removing tokens from required places and adding tokens to next places
        self.excuted = True
        new = set(current)
        for place in self.reqPlaces:
            new.remove(place)
        for place in self.nextP:
            new.add(place)
        return new

    def add_required_place(self, place):
       
        self.reqPlaces.add(place)

    def add_next_place(self, place):
         
        self.nextP.add(place)
        
class Exe:
    # method that initializes an execution object with a list of marking transitions, an initial state and a goal place
    def __init__(self, t: list[Marking], initState, goalP):
        self.transitions = t
        self.goalPlace = goalP
        self.initiState = initState
        self.visitedStates = set()
        self.reachabilityGraph = defaultdict(list)
        self.reachabilityGraph[tuple(sorted(initState))] = []

    def is_sound(self):
        return self.vaild(self.initiState)

    def vaild(self, state, prevState=None, prevTran=None):
         #Recursive method to check if a given state is valid
        stateTuple = tuple(sorted(state))
         # If there is a previous state and transition then add the current state as a successor to the previous state in the reachability graph
        if prevState is not None and prevTran is not None:
            prevStateTuple = tuple(sorted(prevState))
            self.reachabilityGraph[prevStateTuple].append((prevTran, stateTuple))
         # If the goal place is present in the current state, check if it is the only place in the state
        if self.goalPlace in state:
            return len(state) == 1
      
        self.visitedStates.add(stateTuple)
         # Get the list of marking transitions that can be fired from the current state
        shouldFire = self.shouldFire(state)
         # If none , return False
        if len(shouldFire) == 0:
            return False
         # Recursively validate each possible resulting state after firing a marking transition
        for tran in shouldFire:
            new_state = tran.fire(state)
            if new_state not in self.visitedStates:
                if not self.vaild(new_state, state, tran):
        
                    return False
        # If all possible resulting states are valid, return True
        return True

    def is_all_fired(self):
         # Method to check if all marking transitions have been executed(visited)
        return all(transition.excuted for transition in self.transitions)

    def shouldFire(self, currState):
      
        return [transition for transition in self.transitions if not transition.reqPlaces.difference(currState)]
    
def draw_reachability_graph(reachabilityGraph, initialMarking, goalPlace, isSound):
    print('reachabity graph : ')
   
    # Convert the initial marking and goal place to strings
    startState = ",".join(f"P{place}" for place in initialMarking)
    goalState = f"P{goalPlace}"

    # Define ASCII symbols to represent initial, goal, and other nodes
    startSymbol = "+"
    goalSymbol = "*"
    otherSymbol = "o"

    # Iterate through each state in the reachability graph
    for state, transitions in reachabilityGraph.items():
        # Convert the state to a string and print it as a node
        stateStr = ",".join(f"P{place}" for place in state)

        # Use different symbols to represent initial, goal, and other nodes
        if stateStr == startState:
            print(startSymbol, end=' ')
        elif stateStr == goalState:
            print(goalSymbol, end=' ')
        else:
            print(otherSymbol, end=' ')

        # Iterate through each transition and its successor state in the state's list of transitions
        for tran, nextState in transitions:
            # Convert the successor state to a string and print an edge between the current state and the successor state,
            # labeled with the ID of the transition
            next_state_str = ",".join(f"P{place}" for place in nextState)
            print(f"->T{tran.id}->{next_state_str}", end=' ')

        # Print a new line after printing all edges for the current state
        print()

    # Add a text annotation indicating whether the execution is sound or not
    soundText = "Sound" if isSound else "Not sound"
    print(soundText)

    # Set the title and axis options for the graph
    
def input_data(choice):
    if choice != 1 and choice != 2 and choice != 3 and choice != 4:
        return None, None, None , None
    #first example in the lecture
    if choice == 1:
        initial_marking = {0}
        goal_place = 6
        edges = [('P0', 'T1'), ('T1', 'P1'), ('P1', 'T2'),
                 ('T2', 'P2'), ('P2', 'T3'), ('T3', 'P3'), ('P3', 'T5'), ('T5', 'P6'),
                 ('T2', 'P4'), ('P4', 'T4'), ('T4', 'P5'), ('P5', 'T6'), ('T6', 'P6')]
    #second example in the lecture
    elif choice == 2:
        initial_marking = {0}
        goal_place = 8
        edges = [('P0', 'T1'), ('T1', 'P1'), ('P1', 'T2'), ('P1', 'T3'), ('T2', 'P2'), ('P2', 'T4'), ('T4', 'P3'),
                 ('P3', 'T6'),
                 ('P4', 'T8'), ('T8', 'P8'), ('T3', 'P5'), ('P5', 'T5'), ('T5', 'P6'), ('P6', 'T7'), ('T7', 'P7'), ('P7', 'T8'), ('T8', 'P8')]
    #third example in the lecture
    elif choice == 3:
        initial_marking = {1}
        goal_place = 6
        edges = [('P1', 'T1'), ('T1', 'P2'), ('T1', 'P3'), ('P2', 'T2'), ('P2', 'T5'), ('P3', 'T3'), ('T2', 'P4'),
                 ('T3', 'P5'),
                 ('P4', 'T4'), ('P5', 'T4'), ('P5', 'T5'), ('T4', 'P6'), ('T5', 'P6')]
    #dynamic input
    elif choice == 4:
        initial_marking = {int(input("- Initial place number: "))}
        goal_place = int(input("- Goal place number: "))
        edge_count = int(input("- Number of edges: "))
        edges = []
        print("Enter the edges (in this format P1 T2 or T2 P1(a space between the 2 nodes)):")
        for _ in range(edge_count):
            edge = tuple(input().split())
            edges.append(edge)

    return initial_marking, goal_place, edges


  

if __name__ == '__main__':
            print("1-For using lecture first example p.35")
            print("2-For using lecture second example p.38")
            print("3-For using third example ")
            print("4-For dynamic input")
            cho = int(input("Enter a number"))
            initial_marking, goal_place, edges = input_data(cho)

            transactions = defaultdict(Marking)
            for e in edges:
                # If first element starts with 'T', create a new transaction keyed by second letter of the first element
                if e[0][0] == 'T':
                    transactions[e[0][1]] = Marking(e[0][1])
                else:
                    # Otherwise, create a new place keyed by the second letter of the second element
                    transactions[e[1][1]] = Marking(e[1][1])
            # Link required places to each transaction and next places to each place
            for e in edges:
                if e[0][0] == 'T':
                     # If first element starts with 'T', add the second letter of the second element as a next place for the transaction
                    transactions[e[0][1]].add_next_place(int(e[1][1]))
                else:
                     # Otherwise, add the second letter of the first element as a required place for the place
                    transactions[e[1][1]].add_required_place(int(e[0][1]))
            # Convert transactions dictionary to list of Marking objects
            transactions = [value for key, value in transactions.items()]

            excute = Exe(transactions, initial_marking, goal_place)
            
            
            is_sound = excute.is_sound()
                
            draw_reachability_graph(excute.reachabilityGraph, initial_marking, goal_place, is_sound)
        

