cin = open("input.txt")

class automaton:
    def __init__(self, numberOfNodes, numberOfEdges):
        self.graph = {}
        self.alphabet = set()
        self.numberOfNodes = numberOfNodes
        self.numberOfEdges = numberOfEdges
        for e in range(numberOfEdges):
            edge = cin.readline().split()
            if edge[0] not in self.graph:
                self.graph[edge[0]] = [False]
            if edge[1] not in self.graph:
                self.graph[edge[1]] = [False]
            self.graph[edge[0]].append((edge[1], edge[2]))
            self.alphabet |= {edge[2]}
        if "#" in self.alphabet:
            self.alphabet -= {"#"}
        self.initialState = int(cin.readline())
        self.finalStates = cin.readline().split()
        self.finalStates.pop(0)
        for q in self.finalStates:
            self.graph[q][0] = True

    def lambdaClosure(self, q):
        # TODO modify so it also works for superState, something like
        # for q in range(len(superState)): *do #-closure of each one and join the sets*
        superState = [q]
        for edge in range(1, len(self.graph[q])):
            if self.graph[q][edge][1] == "#":
                superState += self.lambdaClosure(self.graph[q][edge][0])
        return ''.join(sorted(list(set(superState))))

    def checkNextLetter(self, q, word, path):
        # TODO update this and checkWord so it works for the new format
        if not word:
            if self.graph[q][1]:
                path.append(q)
                return path
            return False
        if len(self.graph[q]) == 2:
            return False
        for edge in range(2, len(self.graph[q])):
            if word[0] == self.graph[q][edge][1]:
                newPath = path
                newPath.append(q)
                return self.checkNextLetter(self.graph[q][edge][0], word[1:], newPath)
                break
        return False

    def checkWord(self, word):
        currentState = self.initialState
        result = self.checkNextLetter(initialState, word, [])
        if result:
            print(True, *result[1:])
        else:
            print(result)


init = cin.readline().split()
numberOfNodes = int(init[0])
numberOfEdges = int(init[1])
FA = automaton(numberOfNodes, numberOfEdges)
print(FA.graph)
print("Initial State:", FA.initialState)
print("Final States:", *FA.finalStates)
print("Alphabet:", *FA.alphabet)
for node in FA.graph:
    print(f"Lambda closure of {node}: {FA.lambdaClosure(node)}")
# TODO #-nfa to dfa transition; steps for each node:
# step 1: initial state of dfa becomes the superState given by #-closure of initial #-nfa state
# step 2: for each letter, a new superState is created such that it holds all indexes in which
#         that letter points from all the indexes of the initial superState
# step 3: update the new superStates to their #-closure
# step 4: repeat for each new superState until there are no new ones being created
# reminders: 1. superStates which contain the indexes of the #-nfa's final states become the new
#               final states of the dfa
#            2. don't forget to stop the algorithm when the superStates are empty
#            3. create a new graph in the conversion method for these steps and update the old
#               graph with the new one
