import tkinter as tk
from tkinter import messagebox
import pandas as pd
import matplotlib.pyplot as plt
from Tables import A2


class CartaXbarra:
    def __init__(self, master, path, header):
        self.master = master
        self.path = path
        self.header = header
        self.master.title('Carta X\u0304')
        self.master.wm_iconbitmap('Imagens\Logo.ico')
        Labels_Title = tk.Label(self.master,text= 'Selecione as colunas que contém\nas réplicas das amostras')
        Labels_Title.grid(row=0)
        self.frame = tk.Frame(self.master)
        self.frame.grid(row=1)
        self.CBcontents = { i : 0 for i in self.header }

        i=0
        for h in self.CBcontents:
            self.CBcontents[h] = tk.IntVar()
            l = tk.Checkbutton(self.frame, text=h, variable=self.CBcontents[h], onvalue=1, offvalue=0, activebackground='#ffffff', indicatoron='false').grid(row=0,column=i)
            i=i+1

        l1 = tk.Label(self.master, text='Entre com o tamanho das amostras:').grid(row=2)

        self.frame2 = tk.Frame(self.master)
        self.frame2.grid(row=3)
        self.value1 = tk.IntVar()
        self.e1 = tk.Entry(self.frame2, textvariable=self.value1).grid(row=0)

        b = tk.Button(self.master, text='Mostrar Resultados', command=lambda:self.Plot()).grid(row=4)
        save = tk.Button(self.master, text='Salvar', command=lambda: self.Salvar()).grid(row=5, pady=5)

        self.master.mainloop()

    def Salvar(self):
        from .Salvar import SalvarDados
        app = SalvarDados(self.CartaX())

    def CartaX(self):
        try:
            dados = pd.read_csv(self.path)
        except:
            dados = pd.read_excel(self.path, engine='openpyxl')
            dados = dados.dropna(1, how='all')
            dados = dados.dropna(0, how='all')
        droplist = []
        x=0
        for i in self.header:
            if not self.CBcontents[i].get() == 1:
                print(self.CBcontents[i].get())
                droplist.append(i)
        replicas = dados.drop(droplist, axis=1).copy()
        print(replicas)

        TamanhoAmostra = self.value1.get()
        dados['n']=[self.value1.get()]*len(dados)

        dados["MédiaAmostra"] = replicas.mean(axis=1)
        # media amostral (por linha) das replicas das amostras
        if TamanhoAmostra == 1:
            dados["AmplitAmost"] = replicas.max(axis=1)
        else:
            dados["AmplitAmost"] = replicas.max(axis=1) - replicas.min(axis=1)
        # Amplitude amostral (maior menos menor valor por amostra)
        # as colunas MédiaAmostra e AmplitAmostra foram incluídas no DataFrame
        # neste programa, não se faz necessário renomear as colunas pois seus nomes são coletados automaticamente

        dados['MediaGlob'] = dados['MédiaAmostra'].mean()  # média global (média das média ou média de tudo)
        dados['AmplitGlob'] = dados['AmplitAmost'].mean()  # amplitude média

        dados['LSC'] = dados['MediaGlob'] + A2[TamanhoAmostra] * dados['AmplitGlob']
        dados['LIC'] = dados['MediaGlob'] - A2[TamanhoAmostra] * dados['AmplitGlob']
        dados["ResiduoSuperior"] = dados['LSC'] - dados['MédiaAmostra']
        dados["ResiduoInferior"] = dados['LIC'] - dados['MédiaAmostra']
        return dados

    def Plot(self):

        SaidaCartaXbarra = self.CartaX()
        MaiorValor = SaidaCartaXbarra["MédiaAmostra"].max()
        MenorValor = SaidaCartaXbarra["MédiaAmostra"].min()

        if MaiorValor > SaidaCartaXbarra['LSC'][0] or MenorValor < SaidaCartaXbarra['LIC'][0]:
            messagebox.showwarning("Aviso", "Sistema fora de controle")
            print('Sistema fora de controle!')
        else:
            messagebox.showinfo("Aviso", "Sistema sob controle")
            print('Sistema sob controle!')

        plt.plot(SaidaCartaXbarra.index, SaidaCartaXbarra["MédiaAmostra"], marker="o")
        plt.plot(SaidaCartaXbarra.index, SaidaCartaXbarra["MediaGlob"], '--', label='Média')
        plt.plot(SaidaCartaXbarra.index, SaidaCartaXbarra["LIC"], '--', label='LIC')
        plt.plot(SaidaCartaXbarra.index, SaidaCartaXbarra["LSC"], '--', label='LSC')
        plt.ylabel('Médias Amostrais')
        plt.xlabel('Amostra')
        plt.title('Gráfico X-barra')
        teste = (SaidaCartaXbarra['MediaGlob'][0] - SaidaCartaXbarra['LIC'][0])
        plt.annotate('LIC', xy=(1, SaidaCartaXbarra['LIC'][0]), xytext=(1, SaidaCartaXbarra['LIC'][0] + teste / 3),
                     arrowprops=dict(facecolor='black'))
        plt.annotate('LSC', xy=(1, SaidaCartaXbarra['LSC'][0]), xytext=(1, SaidaCartaXbarra['LSC'][0] - teste / 3),
                     arrowprops=dict(facecolor='black'))
        plt.annotate('Média', xy=(1, SaidaCartaXbarra['MediaGlob'][0]), xytext=(1, SaidaCartaXbarra['MediaGlob'][0] - teste / 3),
                     arrowprops=dict(facecolor='black'))
        plt.grid(True)
        plt.show()