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
        return ''.join(sorted(list(set(superState))))

# TODO #-nfa to dfa transition; steps for each node:
# step 1: initial state of dfa becomes the superState given by #-closure of initial #-nfa state
# *step 2: for each letter, a new superState is created such that it holds all indexes in which
#         *that letter points from all the indexes of the initial superState
# *step 3: update the new superStates to their #-closure
# *step 4: repeat for each new superState until there are no new ones being created
# reminders: 1. superStates which contain the indexes of the #-nfa's final states become the new
#               final states of the dfa
#            2. don't forget to stop the algorithm when the superStates are empty
#            3. create a new graph in the conversion method for these steps and update the old
#               graph with the new one


    def conversionToDFA(self):
        newInitialState = self.lambdaClosure(self.initialState)
        newStates = []
        newStates += self.subsetConstruction([newInitialState], 0)
        print(newStates)

# ! must add some sort of while loop to do this until there are no new superStates, also must put them in the new graph
# ! conversion *SEEMS* to work for creating the DFA states, still must update them in the new graph
# [023456, 23456, 0123456]
# lastLength = 1
# newStates[lastLength:] = newStates[1:] = [23456, 0123456] 

    def subsetConstruction(self, newStates, lastLength):
        if lastLength == len(newStates):
            return newStates
        newLastLength = len(newStates)
        for superState in newStates[lastLength:]:
            for letter in self.alphabet:
                newSuperState = []
                for q in superState:
                    for edge in range(1, len(self.graph[q])):
                        if self.graph[q][edge][1] == letter:
                            newSuperState.append(self.graph[q][edge][0])
                newSuperState = ''.join(sorted(list(set(self.lambdaClosure(newSuperState)))))
                if newSuperState not in newStates and len(newSuperState):
                    newStates.append(newSuperState)
        return self.subsetConstruction(newStates, newLastLength)
        

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
#print(FA.graph)
#print("Initial State:", FA.initialState)
#print("Final States:", *FA.finalStates) 
#print("Alphabet:", *FA.alphabet)
FA.conversionToDFA()
