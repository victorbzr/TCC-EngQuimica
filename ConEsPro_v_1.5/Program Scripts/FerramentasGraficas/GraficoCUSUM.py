import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
import pandas as pd
import matplotlib.pyplot as plt

class GraficoCUSUM:
    def __init__(self, master, path, header):
        self.master = master
        self.path = path
        self.header = header
        self.master.title('CUSUM')
        self.master.wm_iconbitmap('Imagens\Logo.ico')
        Labels_Title = tk.Label(self.master,text= 'Selecione as colunas que contenham\nos dados para plotagem do gráfico CUSUM')
        Labels_Title.grid(row=0)
        self.frame = tk.Frame(self.master)
        self.frame.grid(row=1)
        self.CBcontents = { i : 0 for i in self.header }

        i=0
        for h in self.CBcontents:
            self.CBcontents[h] = tk.IntVar()
            l = tk.Checkbutton(self.frame, text=h, variable=self.CBcontents[h], onvalue=1, offvalue=0, activebackground='#ffffff', indicatoron='false').grid(row=0,column=i)
            i=i+1

        lopt = tk.Label(self.master, text='Selecione os valores de entrada').grid(row=2)

        l1 = tk.Label(self.master,text='Valor alvo:').grid(row=3, column=0)
        self.frame1 = tk.Frame(self.master)
        self.frame1.grid(row=4)

        self.var = tk.StringVar()
        self.var.set("0")
        self.value1 = tk.DoubleVar()
        self.e1 = tk.Entry(self.frame1, state="disabled", textvariable=self.value1)
        rdb1 = tk.Radiobutton(self.frame1,text="Default (Média Geral)", variable=self.var, value="0", command=lambda:self.disableEntry(self.e1))
        rdb1.grid(row=0, column=0)
        rdb2 = tk.Radiobutton(self.frame1, text="Personalizado:", variable=self.var, value="1",
                              command=lambda:self.enableEntry(self.e1))
        rdb2.grid(row=1,column=0)
        self.e1.grid(row=1, column=1)

        b = tk.Button(self.master, text='Mostrar Resultados', command=lambda: self.Plot()).grid(row=7)
        save=tk.Button(self.master, text='Salvar', command=lambda: self.Salvar()).grid(row=8, pady=5)

        self.master.mainloop()

    def Salvar(self):
        from .Salvar import SalvarDados
        app=SalvarDados(self.GraficoCUSUM())

    def enableEntry(self, entry):
        entry.configure(state="normal")
        entry.update()

    def disableEntry(self, entry):
        entry.configure(state="disabled")
        entry.update()

    def GraficoCUSUM(self):
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

        dados["MédiaAmostra"] = replicas.mean(axis=1)  # fazendo a média por linha
        # media amostral (por linha). Se não existirem réplicas, a média será o próprio valor medido
        MediaGlob = dados.MédiaAmostra.mean()  # linha para calcular a média global caso o valor alvo não seja informado
        SigmaGlob = dados.MédiaAmostra.std()  # linha para calcular desvio padrão caso o valor não seja informado

        if self.var.get() == "0":
            ValorAlvo = MediaGlob
        elif self.var.get() == "1":
            ValorAlvo = self.value1.get()

        dados["ValorMenosAlvo"] = dados["MédiaAmostra"] - ValorAlvo  # criando nova coluna com desvios do alvo
        dados_aux = dados.cumsum()  # criar um dataframe auxiliar em que as colunas representam as somas acumuladas
        dados["SomaAcumulada"] = dados_aux["ValorMenosAlvo"]  # criando nova coluna no dataframe original
        return (dados)

    def Plot(self):

        SaidaCUSUM = self.GraficoCUSUM()


        plt.plot(SaidaCUSUM.index, SaidaCUSUM["SomaAcumulada"], marker="o")
        plt.ylabel('Soma Acumulada')
        plt.xlabel('Média Amostral')
        plt.title('Gráfico CUSUM')
        plt.grid(True)
        self.master.destroy()
        plt.show()



# root = tk.Tk()
# header = ["a","b"]
# path = "/"
# app=GraficoCUSUM(root,path,header)