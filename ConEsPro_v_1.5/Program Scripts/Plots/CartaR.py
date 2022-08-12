import tkinter as tk
import pandas as pd
from tkinter import messagebox
import matplotlib.pyplot as plt
from Tables import D3,D4
class CartaR:
    def __init__(self, master, path, header):
        self.master = master
        self.path = path
        self.header = header
        self.master.title('Carta R')
        self.master.wm_iconbitmap('Imagens\Logo.ico')
        Labels_Title = tk.Label(self.master, text='Selecione as colunas que contém\nas réplicas das amostras')
        Labels_Title.grid(row=0)
        self.frame = tk.Frame(self.master)
        self.frame.grid(row=1)

        self.CBcontents = {i: 0 for i in self.header}

        i = 0
        for h in self.CBcontents:
            self.CBcontents[h] = tk.IntVar()
            l = tk.Checkbutton(self.frame, text=h, variable=self.CBcontents[h], onvalue=1, offvalue=0,
                               activebackground='#ffffff', indicatoron='false').grid(row=0, column=i)
            i = i + 1
        l1 = tk.Label(self.master, text='Entre com o tamanho das amostras:').grid(row=2)

        self.frame2 = tk.Frame(self.master)
        self.frame2.grid(row=3)
        self.value1 = tk.IntVar()
        self.e1 = tk.Entry(self.frame2, textvariable=self.value1).grid(row=0)

        b = tk.Button(self.master, text='Mostrar Resultados', command=lambda: self.Plot()).grid(row=4)
        save = tk.Button(self.master, text='Salvar', command=lambda: self.Salvar()).grid(row=5, pady=5)

        self.master.mainloop()

    def Salvar(self):
        from .Salvar import SalvarDados
        app = SalvarDados(self.Carta_R())

    def Carta_R(self):
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
        print(replicas)
        TamanhoAmostra = self.value1.get()
        dados['n'] = [self.value1.get()] * len(dados)
        print(dados)
        if TamanhoAmostra==1:
            dados['AmplitAmost'] = replicas.max(axis=1)
        else:
            dados['AmplitAmost'] = replicas.max(axis=1) - replicas.min(axis=1)
        dados['AmplitMed'] = dados["AmplitAmost"].mean() #amplitude média
        dados['LSC'] = D4[TamanhoAmostra]*dados['AmplitMed']
        dados['LIC'] = D3[TamanhoAmostra]*dados['AmplitMed']
        dados["ResiduoSuperior"] = dados['LSC'] - dados['AmplitAmost']
        dados["ResiduoInferior"] = dados['LIC'] - dados['AmplitAmost']
        return dados

    def Plot(self):
        SaidaCartaR = self.Carta_R()
        MaiorValor = SaidaCartaR["AmplitAmost"].max()
        MenorValor = SaidaCartaR["AmplitAmost"].min()
        if MaiorValor>SaidaCartaR['LSC'][0] or MenorValor<SaidaCartaR['LIC'][0]:
            messagebox.showwarning("Aviso", "Sistema fora de controle")
            print ('Sistema fora de controle!')
        else:
            messagebox.showinfo("Aviso", "Sistema sob controle")
            print ('Sistema sob controle!')

        plt.plot(SaidaCartaR.index,SaidaCartaR["AmplitAmost"],marker="o")
        plt.plot(SaidaCartaR.index,SaidaCartaR["AmplitMed"],'--',label = 'Média')
        plt.plot(SaidaCartaR.index,SaidaCartaR['LIC'],'--',label = 'LIC')
        plt.plot(SaidaCartaR.index,SaidaCartaR['LSC'],'--',label = 'LSC')
        plt.ylabel('Amplitudes Amostrais')
        plt.xlabel('Amostra')
        plt.title('Gráfico R')
        teste = (SaidaCartaR['AmplitMed'][0]-SaidaCartaR['LSC'][0])
        plt.annotate('LIC', xy=(1, SaidaCartaR['LIC'][0]), xytext=(1, SaidaCartaR['LIC'][0]+teste/3),
                     arrowprops = dict(facecolor='black'))
        plt.annotate('LSC', xy=(1, SaidaCartaR['LSC'][0]), xytext=(1, SaidaCartaR['LSC'][0]-teste/3),
                     arrowprops = dict(facecolor='black'))
        plt.annotate('Média', xy=(1, SaidaCartaR['AmplitMed'][0]), xytext=(1, SaidaCartaR['AmplitMed'][0]-teste/3),
                     arrowprops = dict(facecolor='black'))
        plt.grid(True)
        plt.show()