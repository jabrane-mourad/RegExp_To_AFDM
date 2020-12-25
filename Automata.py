# -*- coding: utf-8 -*-
"""
Created on Wed April  8 11:58:05 2020

@author: JABRANE,LAHLOU,DAHBI
"""

class Automata:
    """class represente un automate fini"""

    def __init__(self, language = set(['0', '1'])):
        self.states = set()     # l’ensemble des états
        self.startstate = None  # l’état initial
        self.finalstates = []   #l'ensemble des etats  finaux
        self.transitions = dict() # fonction de transition
        self.language = language    # l’alphabet de l’entrée. 
        
    """methode statique retourner epsilon (char)"""
    @staticmethod
    def epsilon():
        return "ε"
    
    """ fonction pour definir l etat initial """
    def setstartstate(self, state):
        self.startstate = state
        self.states.add(state)
        
    """ fonction pour ajouter les etats finaux """
    def addfinalstates(self, state):
        if isinstance(state, int):
            state = [state]
        for s in state:
            if s not in self.finalstates:
                self.finalstates.append(s)

    """fonction pour definir la fonction de transition """
    def addtransition(self, fromstate, tostate, inp):
        if isinstance(inp, str):
            inp = set([inp])
        self.states.add(fromstate)
        self.states.add(tostate)
        if fromstate in self.transitions:
            if tostate in self.transitions[fromstate]:
                self.transitions[fromstate][tostate] = self.transitions[fromstate][tostate].union(inp)
            else:
                self.transitions[fromstate][tostate] = inp
        else:
            self.transitions[fromstate] = {tostate : inp}
            
    """fonction pour ajouter la def de fonction de transition  """
    def addtransition_dict(self, transitions):
        for fromstate, tostates in transitions.items():
            for state in tostates:
                self.addtransition(fromstate, state, tostates[state])
    """fonction retourner une transition  """
    def gettransitions(self, state, key):
        if isinstance(state, int):
            state = [state]
        trstates = set()
        for st in state:
            if st in self.transitions:
                for tns in self.transitions[st]:
                    if key in self.transitions[st][tns]:
                        trstates.add(tns)
        return trstates
    
    """fonction retourner tous les états"""
    def getEClose(self, findstate):
        allstates = set()
        states = set([findstate])
        while len(states)!= 0:
            state = states.pop()
            allstates.add(state)
            if state in self.transitions:
                for tns in self.transitions[state]:
                    if Automata.epsilon() in self.transitions[state][tns] and tns not in allstates:
                        states.add(tns)
        return allstates
    
    """fonctin d'afichage pour le console"""
    def display(self):
        print "états:", self.states
        print "état initial : ", self.startstate
        print "états finaux :", self.finalstates
        print "transition:"
        for fromstate, tostates in self.transitions.items():
            for state in tostates:
                for char in tostates[state]:
                    print "δ(S",fromstate,",",char,")=S",state

    """fonctin d'afichage pour le l'interface graphique"""
    def getPrintText(self):
        text = "L’alphabet de l’entrée: {" + ", ".join(self.language) + "}\n"
        text +="L’ensemble des états: {" + ", ".join(map(str,self.states)) + "}\n"
        text += "L’état initial: " + str(self.startstate) + "\n"
        text += "L’ensemble des états finaux: {" + ", ".join(map(str,self.finalstates)) + "}\n"
        text += "Fonction de transition:\n"
        linecount = 5
        for fromstate, tostates in self.transitions.items():
            for state in tostates:
                for char in tostates[state]:
                    text +="     δ( s"+ str(fromstate) +" , "+ char +" ) = s"+str(state)+"\n"
                    linecount +=1
        return [text, linecount]

    def newBuildFromNumber(self, startnum):
        translations = {}
        for i in list(self.states):
            translations[i] = startnum
            startnum += 1
        rebuild = Automata(self.language)
        rebuild.setstartstate(translations[self.startstate])
        rebuild.addfinalstates(translations[self.finalstates[0]])
        for fromstate, tostates in self.transitions.items():
            for state in tostates:
                rebuild.addtransition(translations[fromstate], translations[state], tostates[state])
        return [rebuild, startnum]

    def newBuildFromEquivalentStates(self, equivalent, pos):
        rebuild = Automata(self.language)
        for fromstate, tostates in self.transitions.items():
            for state in tostates:
                rebuild.addtransition(pos[fromstate], pos[state], tostates[state])
        rebuild.setstartstate(pos[self.startstate])
        for s in self.finalstates:
            rebuild.addfinalstates(pos[s])
        return rebuild
    
    """fonction retourner un fichier'chaine de car.' de syntaxe de dotFile"""
    def getDotFile(self):
        dotFile = "digraph DFA {\nrankdir=LR\n"
        if len(self.states) != 0:
            dotFile += "root=s1\nstart [shape=point]\nstart->s%d\n" % self.startstate
            for state in self.states:
                if state in self.finalstates:
                    dotFile += "s%d [shape=doublecircle]\n" % state
                else:
                    dotFile += "s%d [shape=circle]\n" % state
            for fromstate, tostates in self.transitions.items():
                for state in tostates:
                    for char in tostates[state]:
                        dotFile += 's%d->s%d [label="%s"]\n' % (fromstate, state, char)
        dotFile += "}"
        return dotFile
