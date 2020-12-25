# -*- coding: utf-8 -*-
"""
---
Created on Sat April  11 09:00:05 2020

@author: JABRANE,LAHLOU,DAHBI
"""


from DFAfromNFA import *
class NFAfromRegex:
    """classe pour construire AFND à partir d'expressions régulières"""

    def __init__(self, regex):
        self.star = '*'
        self.plus = '+' #ou '|'
        self.dot = '.'
        self.openingBracket = '('
        self.closingBracket = ')'
        self.operators = [self.plus, self.dot]
        self.regex = regex
        self.alphabet = [chr(i) for i in range(65,91)] #maj
        self.alphabet.extend([chr(i) for i in range(97,123)]) #min
        self.alphabet.extend([chr(i) for i in range(48,58)]) #nbr 0-->9
        self.buildNFA()
        
    """fonction retourner AFND"""
    def getNFA(self):
        return self.nfa
    
    """Fonction d'afichage de AFDN"""
    def displayNFA(self):
        self.nfa.display()
        
    """fonction pour construire AFND"""
    def buildNFA(self):
        language = set()
        self.stack = []
        self.automata = []
        previous = "::e::"
        for char in self.regex:
            if char=="|":
                char="+"
            if char in self.alphabet:
                language.add(char)
                if previous != self.dot and (previous in self.alphabet or previous in [self.closingBracket,self.star]):
                    self.addOperatorToStack(self.dot)
                self.automata.append(BuildAutomata.basicstruct(char))
            elif char  ==  self.openingBracket:
                if previous != self.dot and (previous in self.alphabet or previous in [self.closingBracket,self.star]):
                    self.addOperatorToStack(self.dot)
                self.stack.append(char)
            elif char  ==  self.closingBracket:
                if previous in self.operators:
                    raise BaseException("Error processing '%s' after '%s'" % (char, previous))
                while(1):
                    if len(self.stack) == 0:
                        raise BaseException("Error processing '%s'. Empty stack" % char)
                    o = self.stack.pop()
                    if o == self.openingBracket:
                        break
                    elif o in self.operators:
                        self.processOperator(o)
            elif char == self.star:
                if previous in self.operators or previous  == self.openingBracket or previous == self.star:
                    raise BaseException("Error processing '%s' after '%s'" % (char, previous))
                self.processOperator(char)
            elif char in self.operators:
                if previous in self.operators or previous  == self.openingBracket:
                    raise BaseException("Error processing '%s' after '%s'" % (char, previous))
                else:
                    self.addOperatorToStack(char)
            else:
                raise BaseException("Symbole '%s' n'est pas autorisé" % char)
            previous = char
        while len(self.stack) != 0:
            op = self.stack.pop()
            self.processOperator(op)
        if len(self.automata) > 1:
            print self.automata
            raise BaseException("Regex n'a pas pu être analysé avec succès")
        self.nfa = self.automata.pop()
        self.nfa.language = language
        
    """methode pour ajouter un opérateur à la pile"""
    def addOperatorToStack(self, char):
        while(1):
            if len(self.stack) == 0:
                break
            top = self.stack[len(self.stack)-1]
            if top == self.openingBracket:
                break
            if top == char or top == self.dot:
                op = self.stack.pop()
                self.processOperator(op)
            else:
                break
        self.stack.append(char)
        
    """methode pour afficher l etat des operation """
    def processOperator(self, operator):
        if len(self.automata) == 0:
            raise BaseException("erreur de traitement '%s'. La pile est vide" % operator)
        if operator == self.star:
            a = self.automata.pop()
            self.automata.append(BuildAutomata.starstruct(a))
        elif operator in self.operators:
            if len(self.automata) < 2:
                raise BaseException("erreur de traitement '%s'. Opérande inadéquats" % operator)
            a = self.automata.pop()
            b = self.automata.pop()
            if operator == self.plus:
                self.automata.append(BuildAutomata.plusstruct(b,a))
            elif operator == self.dot:
                self.automata.append(BuildAutomata.dotstruct(b,a))
