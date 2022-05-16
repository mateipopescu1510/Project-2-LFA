cin = open("input.txt")

# {state: [bool, (nextNode1, letter), (nextNode2, letter), ...]}
class Automaton:
    def __init__(self, numberOfNodes, numberOfEdges):
        self.graph = {}
        self.alphabet = set()
        self.numberOfNodes = numberOfNodes
        self.numberOfEdges = numberOfEdges

        for e in range(numberOfEdges):
            edge = cin.readline().split()
            if edge[0] not in self.graph:
                self.graph[edge[0]] = [False]
                # edge[0] = initialNode
            if edge[1] not in self.graph:
                self.graph[edge[1]] = [False]
                # edge[1] = nextNode
            self.graph[edge[0]].append((edge[1], edge[2]))  # edge[2] = letter
            # {state: [bool, (nextNode, letter)]}
            self.alphabet |= {edge[2]}

        if "#" in self.alphabet:
            self.alphabet -= {"#"}

        self.initialState = cin.readline()[:-1]
        self.finalStates = cin.readline().split()
        self.finalStates.pop(0)
        for q in self.finalStates:
            self.graph[q][0] = True
            # {state: [False, ...]} -> {state: [True, ...]}

    def lambdaClosure(self, state):
        superState = list(state)  # convert from string to list
        for q in superState:  # for all nodes in the superState
            for edge in range(1, len(self.graph[q])):  # for all edges of the nodes
                if self.graph[q][edge][1] == "#":
                    superState += self.lambdaClosure(self.graph[q][edge][0])
                    # lambdaClosure for nextNode when letter is #
        return "".join(sorted(list(set(superState))))
        # return string of the list of the set of the final result

    def conversionToDFA(self):
        # initialize new data
        newInitialState = self.lambdaClosure(self.initialState)
        # newInitialState becomes lambdaClosure of the old initial state
        newGraph = {}
        newFinalStates = []
        newGraph.update(
            self.subsetConstruction([newInitialState], {newInitialState: [False]}, 0)
        )  #                       newStates,          newGraph,                lastLength
        for superState in newGraph:
            # make any new superState final if it contains a final state from the inital graph
            for q in superState:
                if q in self.finalStates:
                    newFinalStates.append(superState)
                    newGraph[superState][0] = True
        for superState in newGraph:
            # bring newGraph to the same template
            updatedList = list(set(newGraph[superState][1:]))
            updatedList.insert(0, newGraph[superState][0])
            newGraph[superState] = updatedList
        # update everything else
        self.numberOfNodes = len(newGraph)
        newNumberOfEdges = 0
        for superState in newGraph:
            newNumberOfEdges += len(newGraph[superState]) - 1
        self.numberOfEdges = newNumberOfEdges
        self.graph = newGraph
        self.initialState = newInitialState
        self.finalStates = list(set(newFinalStates))

    def subsetConstruction(self, newStates, newGraph, lastLength):
        # lastLength stores how many newStates there are after the last recursion
        if lastLength == len(newStates):  # if there are no new states, exit
            return newGraph
        newLastLength = len(newStates)
        for superState in newStates[(lastLength - 1) :]:
            # only for the new superStates, as they are appended at the end of the list
            for letter in self.alphabet:  # for each letter
                newSuperState = []
                for q in superState:  # for each node in the superState
                    for edge in range(1, len(self.graph[q])):
                        # for each edge coming out of that state
                        if self.graph[q][edge][1] == letter:
                            # check if the letters are the same
                            newSuperState.append(self.graph[q][edge][0])
                            # append nextNode to newSuperState

                newSuperState = "".join(
                    sorted(list(set(self.lambdaClosure(newSuperState))))
                )  # newSuperState becomes a string of its lambda closure
                if len(newSuperState):
                    if newSuperState not in newStates:
                        # create the list for the newSuperState
                        newStates.append(newSuperState)
                        newGraph[newSuperState] = [False]  # by default
                    newGraph[superState].append((newSuperState, letter))
                    # finally, newSuperState becomes a nextNode for superState
        return self.subsetConstruction(newStates, newGraph, newLastLength)

    def checkNextLetter(self, q, word, path):
        if not word:
            if self.graph[q][0]:  # if current state is final
                path.append(q)
                return path
            return False
        if len(self.graph[q]) == 1:
            # if the word still has letters but there are no more next edges
            return False
        for edge in range(1, len(self.graph[q])):  # for all edges
            if word[0] == self.graph[q][edge][1]:
                newPath = path
                newPath.append(q)
                return self.checkNextLetter(self.graph[q][edge][0], word[1:], newPath)
        return False

    def checkWord(self, word):
        result = self.checkNextLetter(self.initialState, word, [self.initialState])
        print(word, end=": ")
        if result:
            print(True, *result[1:])
        else:
            print(result)


init = cin.readline().split()
numberOfNodes = int(init[0])
numberOfEdges = int(init[1])
FA = Automaton(numberOfNodes, numberOfEdges)
print("Alphabet:", FA.alphabet)
print("Initial State:", FA.initialState)
print("Final States:", *FA.finalStates)
print()
print("Graph before conversion:", FA.graph)
print()
FA.conversionToDFA()
print("Updated Alphabet:", FA.alphabet)
print("Updated Initial State:", FA.initialState)
print("Updated Final States:", *FA.finalStates)
print()
print("Graph converted to DFA:", FA.graph)
print()
numberOfWords = int(cin.readline())
for i in range(numberOfWords):
    word = cin.readline()[:-1]
    FA.checkWord(word)
