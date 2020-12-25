# -*- coding: utf-8 -*-
"""
Created on Wed April   6 12:55:29 2020

@author: JABRANE,LAHLOU,DAHBI
"""
from os import popen
import time
from NFAfromRegex import *
import sys

"""methode pour dessiner un graphique"""
def drawGraph(automata, file = ""):
    """From https://github.com/max99x/automata-editor/blob/master/util.py"""
    f = popen(r"dot -Tpng -o graph%s.png" % file, 'w')
    try:
        f.write(automata.getDotFile()) 
    except:
        raise BaseException("Error creating graph")
    finally:
        f.close()
    
"""methode pour tester l'existence de dot.exe(tester si GraphViz est exist dansl'envirenment variable )"""
def isInstalled(program):
    """From http://stackoverflow.com/questions/377017/test-if-executable-exists-in-python"""
    import os
    def is_exe(fpath):
        return os.path.isfile(fpath) and os.access(fpath, os.X_OK)
    fpath, fname = os.path.split(program)
    if fpath:
        if is_exe(program) or is_exe(program+".exe"):
            return True
    else:
        for path in os.environ["PATH"].split(os.pathsep):
            exe_file = os.path.join(path, program)
            if is_exe(exe_file) or is_exe(exe_file+".exe"):
                return True
    return False
