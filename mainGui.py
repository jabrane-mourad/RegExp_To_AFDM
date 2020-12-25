# -*- coding: utf-8 -*-
"""
Created on Wed April   6 11:49:24 2020

@author: JABRANE,LAHLOU,DAHBI
"""


#import toutes les composantes de la bibliotheque "tkinter"
try:
    from Tkinter import *
    import tkFont
    from tkinter import messagebox
except ImportError as err:
    print ("error: %s. La bibliothèque Tkinter est requise pour utiliser l'interface graphique.") % err.message
    os.sys.exit(1)

from methods import *
dotFound = isInstalled("dot") #tester si GraphViz est exist
if dotFound:
    try:
        from PIL import Image, ImageTk
    except ImportError as err:
        print ("Notice: %s. La bibliothèque PIL est nécessaire pour afficher les graphiques.") % err.message
        dotFound = False
else:
    print "le logiciel GraphViz est requis pour afficher les graphiques."




#class d'initialisation de l interface graphique
class AutomataGUI:

    def __init__(self, root, dotFound):
        self.root = root
        self.initUI()
        self.selectedButton = 0
        self.dotFound = dotFound
        startRegex = "ab*"
        self.regexVar.set(startRegex)
        self.handleBuildRegexButton()

    def initUI(self):
      
        
        self.root.title("Automates à partir d'expressions régulières")
        ScreenSizeX = self.root.winfo_screenwidth()
        ScreenSizeY = self.root.winfo_screenheight()
        ScreenRatioX = 0.7
        ScreenRatioY = 0.8
        self.FrameSizeX  = int(ScreenSizeX * ScreenRatioX)
        self.FrameSizeY  = int(ScreenSizeY * ScreenRatioY)
        print self.FrameSizeY, self.FrameSizeX
        FramePosX   = (ScreenSizeX - self.FrameSizeX)/2
        FramePosY   = (ScreenSizeY - self.FrameSizeY)/2
        padX = 10
        padY = 10
        self.root.geometry("%sx%s+%s+%s" % (self.FrameSizeX,self.FrameSizeY,FramePosX,FramePosY))
        self.root.resizable(width=False, height=False)
        self.root.iconbitmap('img\\ensa_log1.ico')
        self.root.configure(background='aquamarine')
        
       
        parentFrame = Frame(self.root, width = int(self.FrameSizeX - 2*padX), height = int(self.FrameSizeY - 2*padY))
        parentFrame.grid(padx=padX, pady=padY, stick=E+W+N+S)
        parentFrame.configure(background='aquamarine')
        

        regexFrame = Frame(parentFrame)
        enterRegexLabel = Label(regexFrame, text="Entrez l'expression régulière :", bg="aquamarine",font=("Helvetica", 14))
        self.regexVar = StringVar()
        self.regexField = Entry(regexFrame, width=50, textvariable=self.regexVar,justify='center')
        buildRegexButton = Button(regexFrame, text="Construire", width=10, command=self.handleBuildRegexButton,bg='green2')
        enterRegexLabel.grid(row=1, column=0, sticky=W)
        self.regexField.grid(row=1, column=1, sticky=W)
        buildRegexButton.grid(row=1, column=5, padx=10)
        regexFrame.configure(background='aquamarine')

        testStringFrame = Frame(parentFrame)
        testStringLabel = Label(testStringFrame, text="Entrez la chaîne de test: ", bg="aquamarine",font=("Helvetica", 14))
        self.testVar = StringVar()
        self.testStringField = Entry(testStringFrame, width=40, textvariable=self.testVar,justify='center')
        testStringButton = Button(testStringFrame, text="Tester", width=10, command=self.handleTestStringButton,bg='green2')
        testStringLabel.grid(row=1, column=0, sticky=W)
        self.testStringField.grid(row=1, column=1, sticky=W)
        testStringButton.grid(row=1, column=2, padx=10)
        testStringFrame.configure(background='aquamarine')



        buttonGroup = Frame(parentFrame)
        nfaButton = Button(buttonGroup, text="Automate Fini Non Déterministe", width=47, command=self.handlenfaButton,bg='plum2')
        dfaButton = Button(buttonGroup, text="Automate Fini Déterministee", width=47, command=self.handledfaButton,bg='hot pink')
        minDFAButton = Button(buttonGroup, text="AFD minimiser", width=47, command=self.handleminDFAButton,bg='oliveDrab1')
        nfaButton.grid(row=0, column=1,padx=(0,5))
        dfaButton.grid(row=0, column=2,padx=(5,5))
        minDFAButton.grid(row=0, column=3,padx=(5,10))
        buttonGroup.configure(background='aquamarine')

        automataCanvasFrame = Frame(parentFrame, height=100, width=100)
        self.cwidth = int(self.FrameSizeX - (2*padX + 20))
        self.cheight = int(self.FrameSizeY * 0.6)
        self.automataCanvas = Canvas(automataCanvasFrame, bg='#FFFFFF', width= self.cwidth, height = self.cheight,scrollregion=(0,0,self.cwidth,self.cheight))
        hbar=Scrollbar(automataCanvasFrame,orient=HORIZONTAL)
        hbar.pack(side=BOTTOM,fill=X)
        hbar.config(command=self.automataCanvas.xview)
        vbar=Scrollbar(automataCanvasFrame,orient=VERTICAL)
        vbar.pack(side=RIGHT,fill=Y)
        vbar.config(command=self.automataCanvas.yview)
        self.automataCanvas.config(xscrollcommand=hbar.set, yscrollcommand=vbar.set)
        self.canvasitems = []
        self.automataCanvas.pack()
        

        regexFrame.grid(row=0, column=0, sticky=W, padx=(160,0),pady=(10,25))
        testStringFrame.grid(row=6, column=0, sticky=W, padx=(220,0),pady=(20,20))
        
        buttonGroup.grid(row=3, column=0)
        automataCanvasFrame.grid(row=4, column=0, pady=(5,20),sticky=E+W+N+S)
        
       
    def handleBuildRegexButton(self):
        t = time.time()
        try:
            inp = self.regexVar.get().replace(' ','')
            if inp == '':
                messagebox.showinfo("Échec", "l'expression régulière est vide!")
                return
            self.createAutomata(inp)
        except BaseException as e:
            messagebox.showinfo("Échec", "Échec :  %s" % e)
        self.displayAutomata()

    def handleTestStringButton(self):
        t = time.time()
        inp = self.testVar.get().replace(' ','')
        if inp == '':
            inp = [':e:']
        if self.dfaObj.acceptsString(inp):
            messagebox.showinfo("message","le mot : { " + inp + " } est ACCEPTÉ")
        else:
            messagebox.showinfo("message","le mot : { " + inp + " } est REJETÉ")

    def handlenfaButton(self):
        self.selectedButton = 0
        self.displayAutomata()

    def handledfaButton(self):
        self.selectedButton = 1
        self.displayAutomata()

    def handleminDFAButton(self):
        self.selectedButton = 2
        self.displayAutomata()

    def createAutomata(self, inp):
        nfaObj = NFAfromRegex(inp)
        self.nfa = nfaObj.getNFA()
        self.dfaObj = DFAfromNFA(self.nfa)
        self.dfa = self.dfaObj.getDFA()
        self.minDFA = self.dfaObj.getMinimisedDFA()
        if self.dotFound:
            drawGraph(self.dfa, "dfa")
            drawGraph(self.nfa, "nfa")
            drawGraph(self.minDFA, "mdfa")
            dfafile = "graphdfa.png"
            nfafile = "graphnfa.png"
            mindfafile = "graphmdfa.png"
            self.nfaimagefile = Image.open(nfafile)
            self.dfaimagefile = Image.open(dfafile)
            self.mindfaimagefile = Image.open(mindfafile)
            self.nfaimg = ImageTk.PhotoImage(self.nfaimagefile)
            self.dfaimg = ImageTk.PhotoImage(self.dfaimagefile)
            self.mindfaimg = ImageTk.PhotoImage(self.mindfaimagefile)

    def displayAutomata(self):
        for item in self.canvasitems:
            self.automataCanvas.delete(item)
        if self.selectedButton == 0:
            header = "\t \t \t Automate Fini Non Déterministe"
            automata = self.nfa
            if self.dotFound:
                image = self.nfaimg
                imagefile = self.nfaimagefile
        elif self.selectedButton == 1:
            header = "\t \t \t Automate Fini Déterministe"
            automata = self.dfa
            if self.dotFound:
                image = self.dfaimg
                imagefile = self.dfaimagefile
        elif self.selectedButton == 2:
            header = "\t \t \t Automate Fini Déterministe Minimiser"
            automata = self.minDFA
            if self.dotFound:
                image = self.mindfaimg
                imagefile = self.mindfaimagefile
        font = tkFont.Font(family="times", size=20)
        (w,h) = (font.measure(header),font.metrics("linespace"))
        headerheight = h + 10
        itd = self.automataCanvas.create_text(10,10,text=header, font=font, anchor=NW)
        self.canvasitems.append(itd)
        [text, linecount] = automata.getPrintText()
        font = tkFont.Font(family="times", size=13)
        (w,h) = (font.measure(text),font.metrics("linespace"))
        textheight = headerheight + linecount * h + 20
        itd = self.automataCanvas.create_text(10, headerheight + 10,text=text, font=font, anchor=NW)
        self.canvasitems.append(itd)
        if self.dotFound:
            itd = self.automataCanvas.create_image(10, textheight, image=image, anchor=NW)
            self.canvasitems.append(itd)
            totalwidth = imagefile.size[0] + 10
            totalheight = imagefile.size[1] + textheight + 10
        else:
            totalwidth = self.cwidth + 10
            totalheight = textheight + 10
        if totalheight < self.cheight:
            totalheight = self.cheight
        if totalwidth < self.cwidth:
            totalwidth = self.cwidth
        self.automataCanvas.config(scrollregion=(0,0,totalwidth,totalheight))

def main():
    global dotFound
    root = Tk()
    app = AutomataGUI(root, dotFound)
    root.mainloop()

if __name__ == '__main__':
    main()

