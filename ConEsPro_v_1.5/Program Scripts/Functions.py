import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import pandas as pd



class GUIFunctions:
    def __init__(self, path):
        self.path = path

    def Fileopen(self,txt):
        from tkinter import filedialog
        self.path = filedialog.askopenfilename(initialdir="/", title="Procurar local do arquivo", filetypes=(
        ("Comma Separated Values CSV", "*.csv"),('Excel','.xlsx')))
        print(self.path)
        try:
            self.df = pd.read_csv(self.path)
        except:
            self.df = pd.read_excel(self.path, engine='openpyxl')
            self.df = self.df.dropna(1,how='all')
            self.df = self.df.dropna(0,how='all')
        print(self.df)
        self.header = self.df.columns.tolist()
        self.lista = self.df.values.tolist()
        print(self.header)
        print(self.lista)
        if self.path == "" or self.path == "/":
            txt.set("Nenhum arquivo selecionado")
        else:
            txt.set(self.path)
    def runPlotMenu(self, tipo, master):
        if tipo == 0:
            import Plots.CartaAtributoC as CAC
            self.app = CAC.CartaAtributoC(master,self.path,self.header)
        elif tipo == 1:
            import Plots.Carta_Xbarra as CXB
            self.app = CXB.CartaXbarra(master,self.path,self.header)
        elif tipo == 2:
            import Plots.CartaR as CR
            self.app = CR.CartaR(master,self.path,self.header)
        elif tipo == 3:
            import EstatisticaBasica.AndersonDarling as AD
            self.app = AD.NormAndersonDarling(master, self.path, self.header)
        elif tipo == 4:
            import EstatisticaBasica.KolmogorovSmirnov as KS
            self.app = KS.NormKolmogorovSmirnov(master, self.path, self.header)
        elif tipo == 5:
            import EstatisticaBasica.ShapiroWilk as SW
            self.app = SW.NormShapiroWilk(master, self.path, self.header)
        elif tipo == 6:
            import FerramentasGraficas.GraficoCUSUM as CUSUM
            self.app = CUSUM.GraficoCUSUM(master, self.path, self.header)
        elif tipo == 7:
            import Plots.CartaCUSUM_Tabular as CUSUMT
            self.app = CUSUMT.CartaCUSUM_Tabular(master, self.path, self.header)
        elif tipo == 8:
            import Plots.CartaAtributoU as CAU
            self.app = CAU.CartaAtributoU(master, self.path, self.header)
        elif tipo == 9:
            import Plots.CartaMMEP as CMMEP
            self.app = CMMEP.CartaMMEP(master, self.path, self.header)
        elif tipo == 10:
            import FerramentasGraficas.Histograma as Hist
            self.app = Hist.Histograma(master, self.path, self.header)
        elif tipo == 11:
            import EstatisticaBasica.Pareto as PRT
            self.app = PRT.Pareto(master, self.path, self.header)
        elif tipo == 12:
            import EstatisticaBasica.Dispersao as DISP
            self.app = DISP.DiagramaDispersao(master, self.path, self.header)
        elif tipo == 13:
            import Plots.Carta_p as CP
            self.app = CP.CartaP(master, self.path, self.header)
        elif tipo == 14:
            import Plots.Carta_np as CNP
            self.app = CNP.CartaNP(master, self.path, self.header)
        else:
            print('Não implementado')