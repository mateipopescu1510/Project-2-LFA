# Project-2-LFA
#-NFA to DFA conversion (still in progress)
Changes from the first project:
* instead of a list, the graph/FA is now a dictionary of the form:
* {state: [bool, (nextNode1, letter), (nextNode2, letter), ...]}
* cleaner constructor for the automaton 
* lambda closure method for a state 
* conversion to DFA (not done)
* updated word accepting method (not done)
 
