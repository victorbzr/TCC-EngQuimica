import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
import pandas as pd
import matplotlib.pyplot as plt

class CartaMMEP:
    def __init__(self, master, path, header):
        self.master = master
        self.path = path
        self.header = header
        self.master.title('Carta MMEP')
        self.master.wm_iconbitmap('Imagens\Logo.ico')
        Labels_Title = tk.Label(self.master, text= 'Selecione as colunas que contenham\nos dados para plotagem da carta MMEP')
        Labels_Title.grid(row=0)
        self.frame = tk.Frame(self.master)
        self.frame.grid(row=1)
        self.CBcontents = { i : 0 for i in self.header }

        i=0
        for h in self.CBcontents:
            self.CBcontents[h] = tk.IntVar()
            l = tk.Checkbutton(self.frame, text=h, variable=self.CBcontents[h], onvalue=1, offvalue=0, activebackground='#ffffff', indicatoron='false').grid(row=0, column=i)
            i=i+1

        lopt = tk.Label(self.master, text='Selecione os valores dos parâmetros r e L').grid(row=6)

        l1 = tk.Label(self.master,text='r (0.05<Usual<0.25):').grid(row=7, column=0)
        self.frame2 = tk.Frame(self.master)
        self.frame2.grid(row=8)

        self.var = tk.StringVar()
        self.var.set("0")
        self.value1 = tk.DoubleVar()
        self.e1 = tk.Entry(self.frame2, state="disabled",textvariable=self.value1)
        rdb1 = tk.Radiobutton(self.frame2,text="0.05", variable=self.var, value="0", command=lambda:self.disableEntry(self.e1))
        rdb1.grid(row=0, column=0)
        rdb2 = tk.Radiobutton(self.frame2, text="0.1", variable=self.var, value="1",
                              command=lambda: self.disableEntry(self.e1))
        rdb2.grid(row=1, column=0)
        rdb3 = tk.Radiobutton(self.frame2, text="0.2", variable=self.var, value="2",
                              command=lambda: self.disableEntry(self.e1))
        rdb3.grid(row=2, column=0)
        rdb4 = tk.Radiobutton(self.frame2, text="Personalizado:", variable=self.var, value="3",
                              command=lambda:self.enableEntry(self.e1))
        rdb4.grid(row=3,column=0)
        self.e1.grid(row=3, column=1)

        l2 = tk.Label(self.master,text='L:').grid(row=9, column=0)

        self.frame3 = tk.Frame(self.master)
        self.frame3.grid(row=10)

        self.var1 = tk.StringVar()
        self.var1.set("0")
        self.value2 = tk.DoubleVar()
        self.e2 = tk.Entry(self.frame3, state="disabled", textvariable=self.value2)
        rdb5 = tk.Radiobutton(self.frame3, text="Default (L=2.7)", variable=self.var1, value="0",
                              command=lambda:self.disableEntry(self.e2))
        rdb5.grid(row=0, column=0)
        rdb6 = tk.Radiobutton(self.frame3, text="Personalizado:", variable=self.var1, value="1",
                              command=lambda:self.enableEntry(self.e2))
        rdb6.grid(row=1, column=0)
        self.e2.grid(row=1, column=1)

        l3 = tk.Label(self.master, text='Valor Alvo:').grid(row=11, column=0)

        self.frame4 = tk.Frame(self.master)
        self.frame4.grid(row=12)

        self.var2 = tk.StringVar()
        self.var2.set("0")
        self.value3 = tk.DoubleVar()
        self.e3 = tk.Entry(self.frame4, state="disabled", textvariable=self.value3)
        rdb7 = tk.Radiobutton(self.frame4, text="Default (Média Global)", variable=self.var2, value="0",
                              command=lambda: self.disableEntry(self.e3))
        rdb7.grid(row=0, column=0)
        rdb8 = tk.Radiobutton(self.frame4, text="Personalizado:", variable=self.var2, value="1",
                              command=lambda: self.enableEntry(self.e3))
        rdb8.grid(row=1, column=0)
        self.e3.grid(row=1, column=1)

        l4 = tk.Label(self.master, text='Sigma:').grid(row=13, column=0)

        self.frame5 = tk.Frame(self.master)
        self.frame5.grid(row=14)

        self.var3 = tk.StringVar()
        self.var3.set("0")
        self.value4 = tk.DoubleVar()
        self.e4 = tk.Entry(self.frame5, state="disabled", textvariable=self.value4)
        rdb9 = tk.Radiobutton(self.frame5, text="Default (Desvio Padrão global)", variable=self.var3, value="0",
                              command=lambda: self.disableEntry(self.e4))
        rdb9.grid(row=0, column=0)
        rdb10 = tk.Radiobutton(self.frame5, text="Personalizado:", variable=self.var3, value="1",
                              command=lambda: self.enableEntry(self.e4))
        rdb10.grid(row=1, column=0)
        self.e4.grid(row=1, column=1)

        b = tk.Button(self.master, text='Mostrar Resultados', command=lambda: self.Plot()).grid(row=15)
        save = tk.Button(self.master, text='Salvar', command=lambda: self.Salvar()).grid(row=16, pady=5)

        self.master.mainloop()

    def Salvar(self):
        from .Salvar import SalvarDados
        app = SalvarDados(self.CartaMMEP())

    def enableEntry(self, entry):
        entry.configure(state="normal")
        entry.update()

    def disableEntry(self, entry):
        entry.configure(state="disabled")
        entry.update()

    def CartaMMEP(self):
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
            r = 0.05
        elif self.var.get() == "1":
            r = 0.1
        elif self.var.get() == "2":
            r = 0.2
        elif self.var.get() == "3":
            r = self.value1.get()

        if self.var1.get() == "0":
            L = 2.7
        elif self.var1.get() == "1":
            L = self.value2.get()

        if self.var2.get() == "0":
            ValorAlvo = MediaGlob
        elif self.var2.get() == "1":
            ValorAlvo = self.value3.get()

        if self.var3.get() == "0":
            Sigma = SigmaGlob
        elif self.var3.get() == "1":
            Sigma = self.value4.get()

        dados["ValorAlvo"] = [ValorAlvo] * len(dados)
        dados["MediaGlobal"] = [MediaGlob] * len(dados)
        dados["SigmaGlobal"] = [Sigma] * len(dados)

        # dados["ValorMenosAlvoMaisK"] = dados["MédiaAmostra"] - (ValorAlvo+K)  # criando nova coluna com desvios do alvo
        # dados["AlvoMenosKMenosValor"] = (ValorAlvo-K) - dados["MédiaAmostra"]  # criando nova coluna com desvios do alvo

        pd.options.mode.chained_assignment = None  # opção para evitar o aviso SettingWithCopyWarning, ao fazer cópias das colunas do dataframe

        dados["z_i"] = ""
        dados["LSC"] = ""
        dados["LIC"] = ""  # criando uma coluna vazia
        z_0 = r * dados["MédiaAmostra"][0] + (1.0 - r) * ValorAlvo
        dados["z_i"][0] = z_0

        cont = 0
        Num_Linhas = dados.shape[0]
        while (cont < Num_Linhas - 1):
            cont = cont + 1
            dados["z_i"][cont] = r * dados["MédiaAmostra"][cont] + (1.0 - r) * dados["z_i"][cont - 1]
        cont = -1
        while (cont < Num_Linhas):
            cont = cont + 1
            dados["LSC"][cont] = ValorAlvo + L * Sigma * (
                        r / (2.0 - r) * (1.0 - (1.0 - r) ** (2.0 * (cont + 1)))) ** 0.5
            dados["LIC"][cont] = ValorAlvo - L * Sigma * (
                        r / (2.0 - r) * (1.0 - (1.0 - r) ** (2.0 * (cont + 1)))) ** 0.5

        dados["ResiduoSuperior"] = dados["LSC"] - dados["z_i"]
        dados["ResiduoInferior"] = dados["LIC"] - dados["z_i"]

        return (dados)

    def Plot(self):
        SaidaMMEP = self.CartaMMEP()
        print(SaidaMMEP)
        plt.plot(SaidaMMEP.index, SaidaMMEP["z_i"], label='z_i', color="blue")
        plt.plot(SaidaMMEP.index, SaidaMMEP["ValorAlvo"], '--', label='ValorAlvo')
        plt.plot(SaidaMMEP.index, SaidaMMEP["LIC"], '--', label='LIC')
        plt.plot(SaidaMMEP.index, SaidaMMEP["LSC"], '--', label='LSC')
        plt.ylabel('Média Móvel')
        plt.xlabel('Observação')
        plt.title('Gráfico MMEP')
        plt.legend(loc="best")  # https://matplotlib.org/api/pyplot_api.html#matplotlib.pyplot.legend
        teste = (SaidaMMEP['ValorAlvo'][0] - SaidaMMEP['LIC'][0])
        plt.annotate('LIC', xy=(1, SaidaMMEP['LIC'][0]), xytext=(3, SaidaMMEP['LIC'][0] + teste/3),
                     arrowprops=dict(facecolor='black'))
        plt.annotate('LSC', xy=(1, SaidaMMEP['LSC'][0]), xytext=(3, SaidaMMEP['LSC'][0] - teste/3),
                     arrowprops=dict(facecolor='black'))
        plt.annotate('ValorAlvo', xy=(1, SaidaMMEP['ValorAlvo'][0]), xytext=(3, SaidaMMEP['ValorAlvo'][0] - teste/3),
                     arrowprops=dict(facecolor='black'))
        plt.grid(True)
        plt.show()

# root = tk.Tk()
# header = ["a","b"]
# path = "/"
# app=CartaMMEP(root,path,header)