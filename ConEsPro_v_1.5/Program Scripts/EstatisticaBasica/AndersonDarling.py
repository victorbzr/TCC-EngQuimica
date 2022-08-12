import tkinter as tk
import pandas as pd
import scipy.stats as stats
from tkinter import filedialog
from tkinter import messagebox

class NormAndersonDarling:
    def __init__(self, master, path, header):
        self.master = master
        self.path = path
        self.header = header
        self.master.title('Anderson Darling')
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

        Conf = tk.Label(self.master, text='Selecione o nível de significância').grid(row=2)

        self.frame1 = tk.Frame(self.master)
        self.frame1.grid(row=3)

        self.var = tk.IntVar()
        self.Confianca = ['15%', '10%', '5%', '2.5%', '1%']
        i = 0
        for h in self.Confianca:
            l = tk.Radiobutton(self.frame1, text=h, variable=self.var, value=i).grid(row=i, column=0, sticky='W')
            i = i + 1

        b = tk.Button(self.master, text='Mostrar Resultados', command=lambda: self.Plot()).grid(row=4)

        self.master.mainloop()

    def AndersonDarling(self):
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
        # testa se a distribuição é normal por AD
        AD_stat, AD_critico, AD_teorico = stats.anderson(DadosEmLista, 'norm')
        return (dados, AD_stat, AD_critico, AD_teorico)

    def Plot(self):
        SaidaAD = self.AndersonDarling()

        Alfa = SaidaAD[3][
            self.var.get()]  # nível de significância. O algoritmo retorna o seguinte array array([15. , 10. ,  5. ,  2.5,  1. ])
        # [self.var.get()] indica o item da lista que foi selecionado pelo usuário
        ValorCritico = SaidaAD[2][self.var.get()]  # Utiliza elemento da lista relacionado ao alfa definido pelo usuário.
        # O algoritmo retorna um vetor de valores críticos.
        ValorCalculado = SaidaAD[1]  # Somente um valor A é calculado

        print("Com " + str(100 - Alfa) +
              "% de confianca, o valor teórico do teste de Anderson-Darling é " + str(ValorCritico))

        print("O valor calculado para o teste de Anderson-Darling foi " + str(ValorCalculado))

        if ValorCalculado < ValorCritico:
            print("Com " + str(100 - Alfa) +
                  "% de confiança, não há evidências para rejeitar a hipótese de normalidade dos dados."
                  "Ou seja, os dados seguem uma distribuição normal.")
            tk.messagebox.showinfo(title='Resultados do teste de Anderson-Darling',message="Com " + str(100 - Alfa) +
              "% de confianca, o valor teórico do teste de Anderson-Darling é " + str(ValorCritico)+"\n\nO valor calculado para o teste de Anderson-Darling foi " + str(ValorCalculado)+"\n\nCom " + str(100 - Alfa) +
                  "% de confiança, não há evidências para rejeitar a hipótese de normalidade dos dados."
                  "Ou seja, os dados seguem uma distribuição normal.")
        else:
            print("Com " + str(100 - Alfa) +
                  "% de confiança, há evidências para rejeitar a hipótese de normalidade dos dados."
                  "Ou seja, os dados não seguem uma distribuição normal.")
            tk.messagebox.showinfo(title='Resultados do teste de Anderson-Darling', message="Com " + str(100 - Alfa) +
              "% de confianca, o valor teórico do teste de Anderson-Darling é " + str(ValorCritico)+"\n\nO valor calculado para o teste de Anderson-Darling foi " + str(ValorCalculado)+"\n\nCom " + str(100 - Alfa) +
                  "% de confiança, há evidências para rejeitar a hipótese de normalidade dos dados."
                  "Ou seja, os dados não seguem uma distribuição normal.")
        self.master.destroy()