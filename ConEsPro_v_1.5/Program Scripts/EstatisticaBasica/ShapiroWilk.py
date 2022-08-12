import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import scipy.stats as stats
import pandas as pd

class NormShapiroWilk:
    def __init__(self, master, path, header):
        self.master = master
        self.path = path
        self.header = header
        self.master.title('Shapiro Wilk')
        self.master.wm_iconbitmap('Imagens\Logo.ico')
        Labels_Title = tk.Label(self.master,text= 'Selecione as colunas que contenham\nos dados a serem testados')
        Labels_Title.grid(row=0)
        self.frame = tk.Frame(self.master)
        self.frame.grid(row=1)
        self.CBcontents = { i : 0 for i in self.header }

        i=0
        for h in self.CBcontents:
            self.CBcontents[h] = tk.IntVar()
            l = tk.Checkbutton(self.frame, text=h, variable=self.CBcontents[h], onvalue=1, offvalue=0, activebackground='#ffffff', indicatoron='false').grid(row=0,column=i)
            i=i+1

        b = tk.Button(self.master, text='Mostrar Resultados', command=lambda: self.Plot()).grid(row=4)

        self.master.mainloop()

    def ShapiroWilk(self):
        try:
            dados = pd.read_csv(self.path)
        except:
            dados = pd.read_excel(self.path, engine='openpyxl')
            dados = dados.dropna(1, how='all')
            dados = dados.dropna(0, how='all')
        droplist = []
        x = 0
        for i in self.header:
            if not self.CBcontents[i].get() == 1:
                print(self.CBcontents[i].get())
                droplist.append(i)
        replicas = dados.drop(droplist, axis=1).copy()
        NumeroColunas = replicas.shape[1]
        Lista = list(range(NumeroColunas))
        cont = 0
        if NumeroColunas == 1:
            print('\n')
            DadosEmLista = [item for sublist in replicas.values.tolist() for item in sublist]
        else:
            for i in replicas.columns.tolist():  # loop para transformar as colunas das réplicas em lista.
                Lista[cont] = replicas[i].values.tolist()
                if cont == 0:
                    ListaAnterior = Lista[cont]
                else:
                    DadosEmLista = Lista[cont] + ListaAnterior
                    ListaAnterior = DadosEmLista
                cont = cont + 1
        SW_stat, p_valor = stats.shapiro(DadosEmLista)  # testa se a distribuição é normal por SW
        # https://docs.scipy.org/doc/scipy/reference/stats.html
        return (SW_stat, p_valor)

    def Plot(self):
        SaidaSW = self.ShapiroWilk()

        ValorDaEstat = SaidaSW[0]
        P_valor = SaidaSW[1]

        print("O valor calculado do teste de Shapiro-Wilk foi de = " + str(ValorDaEstat))
        print("O p-valor calculado para o teste de Shapiro-Wilk foi de = " + str(P_valor))

        if P_valor >= 0.05:
            print("Com 95% de confiança, não temos evidências para rejeitar a hipótese de normalidade dos dados, "
                  "segundo o teste de Shapiro-Wilk. Ou seja, os dados seguem uma distribuição normal.")
            tk.messagebox.showinfo(title='Resultados do teste de Shapiro-Wilk',
                                   message="O valor calculado do teste de Shapiro-Wilk foi de = " + str(ValorDaEstat) + "\n\nO p-valor calculado para o teste de Shapiro-Wilk foi de = " + str(P_valor) + "\n\nCom 95% de confiança, não temos evidências para rejeitar a hipótese de normalidade dos dados, "
                  "segundo o teste de Shapiro-Wilk. Ou seja, os dados seguem uma distribuição normal.")
        else:
            print("Com 95% de confianca, temos evidências para rejeitar a hipótese de normalidade dos dados, "
                  "segundo o teste de Shapiro-Wilk. Ou seja, os dados não seguem uma distribuição normal.")
            tk.messagebox.showinfo(title='Resultados do teste de Shapiro-Wilk',
                                   message="O valor calculado do teste de Shapiro-Wilk foi de = " + str(
                                       ValorDaEstat) + "\n\nO p-valor calculado para o teste de Shapiro-Wilk foi de = " + str(
                                       P_valor) + "\n\nCom 95% de confianca, temos evidências para rejeitar a hipótese de normalidade dos dados, "
                  "segundo o teste de Shapiro-Wilk. Ou seja, os dados não seguem uma distribuição normal.")
        self.master.destroy()