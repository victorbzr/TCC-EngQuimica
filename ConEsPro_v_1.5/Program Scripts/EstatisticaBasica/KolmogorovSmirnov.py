import tkinter as tk
import scipy.stats as stats
import pandas as pd
import numpy as np
from tkinter import filedialog
from tkinter import messagebox

class NormKolmogorovSmirnov:
    def __init__(self, master, path, header):
        self.master = master
        self.path = path
        self.header = header
        self.master.title('Kolmogorov Smirnov')
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

    def KolmogorovSmirnov(self):
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

        DadosEmListaNP = np.array(DadosEmLista)
        media = np.mean(DadosEmListaNP)
        std = np.std(DadosEmListaNP, ddof=1)
        KS_stat, p_valor = stats.kstest(DadosEmListaNP, cdf='norm', args=(media, std), N=len(DadosEmListaNP))
        # testa se a distribuição é normal por KS
        # https://docs.scipy.org/doc/scipy/reference/stats.html
        NumeroDados = len(DadosEmListaNP)
        if NumeroDados <= 40:
            # valores entre 1 e 40
            kolmogorov_critico = [0.97500, 0.84189, 0.70760, 0.62394, 0.56328, 0.51926, 0.48342, 0.45427, 0.43001,
                                  0.40925,
                                  0.39122, 0.37543, 0.36143, 0.34890, 0.33760, 0.32733, 0.31796, 0.30936, 0.30143,
                                  0.29408,
                                  0.28724, 0.28087, 0.27490, 0.26931, 0.26404, 0.25907, 0.25438, 0.24993, 0.24571,
                                  0.24170,
                                  0.23788, 0.23424, 0.23076, 0.22743, 0.22425, 0.22119, 0.21826, 0.21544, 0.21273,
                                  0.21012]
            ks_critico = kolmogorov_critico[NumeroDados - 1]
        elif NumeroDados > 40:
            # valores acima de 40:
            kolmogorov_critico = 1.36 / (np.sqrt(NumeroDados))
            ks_critico = kolmogorov_critico
        else:
            pass

        return (KS_stat, p_valor, ks_critico)

    def Plot(self):
        SaidaKS = self.KolmogorovSmirnov()

        # table of critical values for the kolmogorov-smirnov test - 95% confidence
        # Source: https://www.soest.hawaii.edu/GG/FACULTY/ITO/GG413/K_S_Table_one_Sample.pdf
        # Source: http://www.real-statistics.com/statistics-tables/kolmogorov-smirnov-table/
        # alpha = 0.05 (95% confidential level)

        ValorDaEstat = SaidaKS[0]
        P_valor = SaidaKS[1]
        KS_critico = SaidaKS[2]

        print("O valor calculado do teste de Kolmogorov-Smirnov foi de  " + str(ValorDaEstat))
        print("O valor calculado do teste de Kolmogorov-Smirnov foi de  " + str(KS_critico))

        if KS_critico >= ValorDaEstat:
            print("Com 95% de confiança, não temos evidências para rejeitar a hipótese de normalidade dos dados, "
                  "segundo o teste de Kolmogorov-Smirnov. Ou seja, os dados seguem uma distribuição normal.")
            tk.messagebox.showinfo(title='Resultados do teste de Kolmogorov-Smirnov', message="O valor calculado do teste de Kolmogorov-Smirnov foi de  " + str(ValorDaEstat) + "\n\nO valor calculado do teste de Kolmogorov-Smirnov foi de  " + str(KS_critico) + "\n\nCom 95% de confiança, não temos evidências para rejeitar a hipótese de normalidade dos dados, "
                  "segundo o teste de Kolmogorov-Smirnov. Ou seja, os dados seguem uma distribuição normal.")
        else:
            print("Com 95% de confianca, temos evidências para rejeitar a hipótese de normalidade dos dados, "
                  "segundo o teste de Kolmogorov-Smirnov. Ou seja, os dados não seguem uma distribuição normal.")
            tk.messagebox.showinfo(title='Resultados do teste de Kolmogorov-Smirnov',
                                   message="O valor calculado do teste de Kolmogorov-Smirnov foi de  " + str(ValorDaEstat) + "\n\nO valor calculado do teste de Kolmogorov-Smirnov foi de  " + str(KS_critico) + "\n\nCom 95% de confianca, temos evidências para rejeitar a hipótese de normalidade dos dados, "
                  "segundo o teste de Kolmogorov-Smirnov. Ou seja, os dados não seguem uma distribuição normal.")
        self.master.destroy()