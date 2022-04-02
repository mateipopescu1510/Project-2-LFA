cin = open("input.txt")


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
            if edge[1] not in self.graph:
                self.graph[edge[1]] = [False]
            self.graph[edge[0]].append((edge[1], edge[2]))
            self.alphabet |= {edge[2]}

        if "#" in self.alphabet:
            self.alphabet -= {"#"}

        self.initialState = cin.readline()[:-1]
        self.finalStates = cin.readline().split()
        self.finalStates.pop(0)
        for q in self.finalStates:
            self.graph[q][0] = True

    def lambdaClosure(self, state):
        superState = list(state)
        for q in superState:
            for edge in range(1, len(self.graph[q])):
                if self.graph[q][edge][1] == "#":
                    superState += self.lambdaClosure(self.graph[q][edge][0])
        return "".join(sorted(list(set(superState))))

    def conversionToDFA(self):
        newInitialState = self.lambdaClosure(self.initialState)
        newGraph = {}
        newFinalStates = []
        newGraph.update(
            self.subsetConstruction([newInitialState], {newInitialState: [False]}, 0)
        )
        for superState in newGraph:
            for q in superState:
                if q in self.finalStates:
                    newFinalStates.append(superState)
                    newGraph[superState][0] = True
        self.graph = newGraph
        self.initialState = newInitialState
        self.finalStates = list(set(newFinalStates))
        # TODO edges can appear more than once

    def subsetConstruction(self, newStates, newGraph, lastLength):
        if lastLength == len(newStates):
            return newGraph
        newLastLength = len(newStates)
        for superState in newStates[(lastLength - 1) :]:
            for letter in self.alphabet:
                newSuperState = []
                for q in superState:
                    for edge in range(1, len(self.graph[q])):
                        if self.graph[q][edge][1] == letter:
                            newSuperState.append(self.graph[q][edge][0])
                newSuperState = "".join(
                    sorted(list(set(self.lambdaClosure(newSuperState))))
                )
                if newSuperState not in newStates and len(newSuperState):
                    newStates.append(newSuperState)
                    newGraph[newSuperState] = [False]
                elif len(newSuperState):
                    newGraph[superState].append((newSuperState, letter))
        return self.subsetConstruction(newStates, newGraph, newLastLength)

    def checkNextLetter(self, q, word, path):
        # TODO update this and checkWord so it works for the new format (q's must be strings, self.graph is now a dict)
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
FA = Automaton(numberOfNodes, numberOfEdges)
print(FA.graph)
# print("Initial State:", FA.initialState)
# print("Final States:", *FA.finalStates)
# print("Alphabet:", *FA.alphabet)
FA.conversionToDFA()
print(FA.graph)
print(FA.finalStates)
