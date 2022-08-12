import tkinter as tk
from tkinter import messagebox
import pandas as pd
import matplotlib.pyplot as plt

class CartaAtributoU:
    def __init__(self, master, path, header):
        self.path = path
        self.master = master
        self.header = header
        self.master.title('Carta U')
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

        l1 = tk.Label(self.master, text = 'Selecione uma opção de tamanho amostral:').grid(row=2)

        self.frame2 = tk.Frame(self.master)
        self.frame2.grid(row=3)
        self.var = tk.StringVar()
        self.var.set("0")
        self.value1 = tk.IntVar()
        self.e1 = tk.Entry(self.frame2, textvariable=self.value1)
        rdb1 = tk.Radiobutton(self.frame2, text="Fixo:", variable=self.var, value="0",
                              command=lambda: self.enableEntry(self.e1))
        rdb1.grid(row=0, column=0)
        rdb2 = tk.Radiobutton(self.frame2, text="Variável:", variable=self.var, value="1",
                              command=lambda: self.disableEntry(self.e1))
        rdb2.grid(row=1, column=0)
        self.e1.grid(row=0, column=1)

        l2 = tk.Label(self.master, text='Selecione a coluna que contém\nos tamanhos amostrais(Caso variáveis):').grid(row=4)
        self.frame3 = tk.Frame(self.master)
        self.frame3.grid(row=5)

        i = 0
        j = 0
        k = 0
        self.var1 = tk.IntVar()
        self.var1.set(0)
        for h in self.header:
            l = tk.Radiobutton(self.frame3, text=h, variable=self.var1, value = k).grid(row=i, column=j)
            i = i + 1
            k = k + 1
            if i == 10:
                i = 0
                j = j + 1

        Plot = tk.Button(self.master, text='Mostrar resultados', command=self.Plot).grid(row=6)
        save = tk.Button(self.master, text='Salvar', command=lambda: self.Salvar()).grid(row=7, pady=5)

        self.master.mainloop()

    def Salvar(self):
        from .Salvar import SalvarDados
        app = SalvarDados(self.CartaU())

    def enableEntry(self, entry):
        entry.configure(state="normal")
        entry.update()

    def disableEntry(self, entry):
        entry.configure(state="disabled")
        entry.update()

    def CartaU(self):
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

        if self.var.get() == '0':
            TamanhoAmostra = [self.value1.get()] * len(dados)
            dados['ni']=TamanhoAmostra
        else:
            TamanhoAmostra = dados[self.header[self.var1.get()]].copy()
            dados['ni'] = TamanhoAmostra

        dados["Ui"] = dados["Ci"] / dados['ni']
        dados['U'] = dados["Ui"].mean()
        dados['LSC'] = dados['U'] + 3 * (dados['U'] / dados['ni']) ** 0.5
        dados['LIC'] = dados['U'] - 3 * (dados['U'] / dados['ni']) ** 0.5
        for i in range(len(dados['LIC'])):
            if dados['LIC'][i]<0:
                dados['LIC'][i]=0
        dados["ResiduoSuperior"] = dados['LSC'] - dados['Ui']
        dados["ResiduoInferior"] = dados['LIC'] - dados['Ui']
        print(dados)
        return (dados)

    def Plot(self):
        SaidaCartaU = self.CartaU()

        MaiorValor = SaidaCartaU["Ui"].max()
        MenorValor = SaidaCartaU["Ui"].min()

        cont=0
        for i in range(len(SaidaCartaU['LSC'])):
            if SaidaCartaU["Ui"][i] > SaidaCartaU['LSC'][i] or SaidaCartaU["Ui"][i] < SaidaCartaU["LIC"][i]:
                cont = 1
        if cont == 1:
            print('Sistema fora de controle!')
            tk.messagebox.showinfo(title='Resultados Carta Atributo U', message='Sistema fora de controle!')
        else:
            print('Sistema sob controle!')
            tk.messagebox.showinfo(title='Resultados Carta Atributo U', message='Sistema sob controle!')


        plt.plot(SaidaCartaU.index, SaidaCartaU["Ui"], '-o', label='Defeitos por amostra')
        plt.plot(SaidaCartaU.index, SaidaCartaU["U"], '--', label='Média Geral (U)')
        plt.plot(SaidaCartaU.index, SaidaCartaU["LIC"], '--', label='LIC')
        plt.plot(SaidaCartaU.index, SaidaCartaU["LSC"], '--', label='LSC')
        plt.ylabel('Número de defeitos por amostra')
        plt.xlabel('Amostra')
        plt.title('Gráfico U - Número Médio de Não-Conformidades por Amostra')
        plt.legend(loc="best")
        teste = (SaidaCartaU['U'][0] - SaidaCartaU['LIC'][0])
        plt.annotate('LIC', xy=(1, SaidaCartaU['LIC'][0]), xytext=(3, SaidaCartaU['LIC'][0] + teste/3),
                     arrowprops=dict(facecolor='black'))
        plt.annotate('LSC', xy=(1, SaidaCartaU['LSC'][0]), xytext=(3, SaidaCartaU['LSC'][0] - teste/3),
                     arrowprops=dict(facecolor='black'))
        plt.annotate('Média', xy=(1, SaidaCartaU['U'][0]), xytext=(3, SaidaCartaU['U'][0] - teste/3),
                     arrowprops=dict(facecolor='black'))
        plt.grid(True)
        plt.show()

# root = tk.Tk()
# header = ["a","b",'c','d','e','f','g','h','i','j','k']
# path = "/"
# app=CartaAtrubutoU(root,path,header)