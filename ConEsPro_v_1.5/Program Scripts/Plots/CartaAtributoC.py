import tkinter as tk
from tkinter import messagebox
import pandas as pd
import matplotlib.pyplot as plt

class CartaAtributoC:
    def __init__(self, master, path, header):
        self.path = path
        self.master = master
        self.header = header
        self.master.title('Carta C')
        self.master.wm_iconbitmap('Imagens\Logo.ico')
        Labels_Title = tk.Label(self.master, text='Selecione a(s) coluna(s) que\ncontém o número total de erros por amostra:')
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

        Plot = tk.Button(self.master, text='Mostrar resultados', command=self.Plot).grid(row=6)
        save = tk.Button(self.master, text='Salvar', command=lambda: self.Salvar()).grid(row=7, pady=5)

        self.master.mainloop()

    def Salvar(self):
        from .Salvar import SalvarDados
        app = SalvarDados(self.CartaC())

    def CartaC(self):
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

        dados["Ci"] = replicas.mean(axis=1)  # fazendo a média por linha
        # media amostral (por linha). Se não existirem réplicas, a média será o próprio valor medido

        dados['C'] = dados["Ci"].mean()
        dados['LSC'] = dados['C'] + 3 * (dados['C']) ** 0.5
        dados['LIC'] = dados['C'] - 3 * (dados['C']) ** 0.5
        for i in range(len(dados['LIC'])):
            if dados['LIC'][i]<0:
                dados['LIC'][i]=0
        dados["ResiduoSuperior"] = dados['LSC'] - dados['Ci']
        dados["ResiduoInferior"] = dados['LIC'] - dados['Ci']
        print(dados)
        return (dados)

    def Plot(self):
        SaidaCartaC = self.CartaC()

        MaiorValor = SaidaCartaC["Ci"].max()
        MenorValor = SaidaCartaC["Ci"].min()

        cont=0
        for i in range(len(SaidaCartaC['LSC'])):
            if SaidaCartaC["Ci"][i] > SaidaCartaC['LSC'][i] or SaidaCartaC["Ci"][i] < SaidaCartaC["LIC"][i]:
                cont = 1
        if cont == 1:
            print('Sistema fora de controle!')
            tk.messagebox.showinfo(title='Resultados Carta Atributo C', message='Sistema fora de controle!')
        else:
            print('Sistema sob controle!')
            tk.messagebox.showinfo(title='Resultados Carta Atributo C', message='Sistema sob controle!')


        plt.plot(SaidaCartaC.index, SaidaCartaC["Ci"], '-o', label='Defeitos por unidade')
        plt.plot(SaidaCartaC.index, SaidaCartaC["C"], '--', label='Média Geral (C)')
        plt.plot(SaidaCartaC.index, SaidaCartaC["LIC"], '--', label='LIC')
        plt.plot(SaidaCartaC.index, SaidaCartaC["LSC"], '--', label='LSC')
        plt.ylabel('Número de Defeitos')
        plt.xlabel('Amostra')
        plt.title('Gráfico C - Número de Não-Conformidades')
        plt.legend(loc="best")
        teste = (SaidaCartaC['C'][0] - SaidaCartaC['LIC'][0])
        plt.annotate('LIC', xy=(1, SaidaCartaC['LIC'][0]), xytext=(3, SaidaCartaC['LIC'][0] + teste/3),
                     arrowprops=dict(facecolor='black'))
        plt.annotate('LSC', xy=(1, SaidaCartaC['LSC'][0]), xytext=(3, SaidaCartaC['LSC'][0] - teste/3),
                     arrowprops=dict(facecolor='black'))
        plt.annotate('Média', xy=(1, SaidaCartaC['C'][0]), xytext=(3, SaidaCartaC['C'][0] - teste/3),
                     arrowprops=dict(facecolor='black'))
        plt.grid(True)
        plt.show()

# root = tk.Tk()
# header = ["a","b",'c','d','e','f','g','h','i','j','k']
# path = "/"
# app=CartaAtrubutoC(root,path,header)