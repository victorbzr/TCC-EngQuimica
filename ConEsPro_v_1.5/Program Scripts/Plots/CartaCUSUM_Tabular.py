import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
import pandas as pd
import matplotlib.pyplot as plt

class CartaCUSUM_Tabular:
    def __init__(self, master, path, header):
        self.master = master
        self.path = path
        self.header = header
        self.master.title('Carta CUSUM Tabular')
        self.master.wm_iconbitmap('Imagens\Logo.ico')
        Labels_Title = tk.Label(self.master, text= 'Selecione as colunas que contenham\nos dados para plotagem da carta CUSUM Tabular')
        Labels_Title.grid(row=0)
        self.frame = tk.Frame(self.master)
        self.frame.grid(row=1)
        self.CBcontents = { i : 0 for i in self.header }

        i=0
        for h in self.CBcontents:
            self.CBcontents[h] = tk.IntVar()
            l = tk.Checkbutton(self.frame, text=h, variable=self.CBcontents[h], onvalue=1, offvalue=0, activebackground='#ffffff', indicatoron='false').grid(row=0, column=i)
            i=i+1

        self.tipo = ["Superior", "Inferior", "Completa"]
        select = tk.Label(self.master, text='Selecione o tipo de carta CUSUM tabular').grid(row=2, column=0)
        self.frame1 = tk.Frame(self.master)
        self.frame1.grid(row=3)
        self.tkvar = tk.StringVar()
        self.tkvar.set('Tipo de gráfico CUSUM')  # set the default option

        self.PlotType = tk.OptionMenu(self.frame1, self.tkvar, *self.tipo).grid(row=3, column=0)

        self.tipo1 = ["Dispersão", "Barras"]
        select1 = tk.Label(self.frame1, text='Selecione o tipo de plotagem').grid(row=4, column=0)
        self.tkvar1 = tk.StringVar()
        self.tkvar1.set('Tipo de plotagem')  # set the default option

        self.PlotType1 = tk.OptionMenu(self.frame1, self.tkvar1, *self.tipo1).grid(row=5, column=0)

        lopt = tk.Label(self.master, text='Selecione os valores de entrada').grid(row=6)

        l1 = tk.Label(self.master,text='Valor alvo:').grid(row=7, column=0)
        self.frame2 = tk.Frame(self.master)
        self.frame2.grid(row=8)

        self.var = tk.StringVar()
        self.var.set("0")
        self.value1 = tk.DoubleVar()
        self.e1 = tk.Entry(self.frame2, state="disabled",textvariable=self.value1)
        rdb1 = tk.Radiobutton(self.frame2,text="Default (Média Geral)", variable=self.var, value="0", command=lambda:self.disableEntry(self.e1))
        rdb1.grid(row=0, column=0)
        rdb2 = tk.Radiobutton(self.frame2, text="Personalizado:", variable=self.var, value="1",
                              command=lambda:self.enableEntry(self.e1))
        rdb2.grid(row=1,column=0)
        self.e1.grid(row=1, column=1)

        l2 = tk.Label(self.master,text='Sigma:').grid(row=9, column=0)

        self.frame3 = tk.Frame(self.master)
        self.frame3.grid(row=10)

        self.var1 = tk.StringVar()
        self.var1.set("0")
        self.value2 = tk.DoubleVar()
        self.e2 = tk.Entry(self.frame3, state="disabled", textvariable=self.value2)
        rdb3 = tk.Radiobutton(self.frame3, text="Default (Desvio Padrão da Amostra)", variable=self.var1, value="0",
                              command=lambda:self.disableEntry(self.e2))
        rdb3.grid(row=0, column=0)
        rdb4 = tk.Radiobutton(self.frame3, text="Personalizado:", variable=self.var1, value="1",
                              command=lambda:self.enableEntry(self.e2))
        rdb4.grid(row=1, column=0)
        self.e2.grid(row=1, column=1)

        l3 = tk.Label(self.master, text='Valor de tolerância (K):').grid(row=11, column=0)

        self.frame4 = tk.Frame(self.master)
        self.frame4.grid(row=12)

        self.var2 = tk.StringVar()
        self.var2.set("0")
        self.value3 = tk.DoubleVar()
        self.e3 = tk.Entry(self.frame4, state="disabled", textvariable=self.value3)
        rdb5 = tk.Radiobutton(self.frame4, text="Default (Sigma/2)", variable=self.var2, value="0",
                              command=lambda: self.disableEntry(self.e3))
        rdb5.grid(row=0, column=0)
        rdb6 = tk.Radiobutton(self.frame4, text="Personalizado:", variable=self.var2, value="1",
                              command=lambda: self.enableEntry(self.e3))
        rdb6.grid(row=1, column=0)
        self.e3.grid(row=1, column=1)

        l4 = tk.Label(self.master, text='Intervalo de decisão (H):').grid(row=13, column=0)

        self.frame5 = tk.Frame(self.master)
        self.frame5.grid(row=14)

        self.var3 = tk.StringVar()
        self.var3.set("0")
        self.value4 = tk.DoubleVar()
        self.e4 = tk.Entry(self.frame5, state="disabled", textvariable=self.value4)
        rdb7 = tk.Radiobutton(self.frame5, text="Default (5*Sigma)", variable=self.var3, value="0",
                              command=lambda: self.disableEntry(self.e4))
        rdb7.grid(row=0, column=0)
        rdb8 = tk.Radiobutton(self.frame5, text="Personalizado:", variable=self.var3, value="1",
                              command=lambda: self.enableEntry(self.e4))
        rdb8.grid(row=1, column=0)
        self.e4.grid(row=1, column=1)

        b = tk.Button(self.master, text='Mostrar Resultados', command=lambda: self.Plot()).grid(row=15)
        save = tk.Button(self.master, text='Salvar', command=lambda: self.Salvar()).grid(row=16, pady=5)

        self.master.mainloop()

    def Salvar(self):
        from .Salvar import SalvarDados
        data=self.CartaCUSUM()
        app = SalvarDados(data[0])

    def enableEntry(self, entry):
        entry.configure(state="normal")
        entry.update()

    def disableEntry(self, entry):
        entry.configure(state="disabled")
        entry.update()

    def CartaCUSUM(self):
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

        if self.var1.get() == "0":
            Sigma = SigmaGlob
        elif self.var1.get() == "1":
            Sigma = self.value2.get()

        if self.var2.get() == "0":
            K = Sigma/2
        elif self.var2.get() == "1":
            K = self.value3.get()

        if self.var3.get() == "0":
            H = 5*Sigma
        elif self.var3.get() == "1":
            H = self.value4.get()


        dados["ValorMenosAlvoMaisK"] = dados["MédiaAmostra"] - (ValorAlvo+K)  # criando nova coluna com desvios do alvo
        dados["AlvoMenosKMenosValor"] = (ValorAlvo-K) - dados["MédiaAmostra"]  # criando nova coluna com desvios do alvo

        pd.options.mode.chained_assignment = None  # opção para evitar o aviso SettingWithCopyWarning, ao fazer cópias das colunas do dataframe

        C_0 = 0.0
        dados["C_Mais"] = C_0
        dados["C_Menos"] = C_0
        dados["H"] = H
        for i in range(len(dados)):
            if dados["ValorMenosAlvoMaisK"][i] > 0:
                dados["C_Mais"][i] = dados["ValorMenosAlvoMaisK"][i]  # criando nova coluna no dataframe original
            if dados["AlvoMenosKMenosValor"][i] >0:
                dados["C_Menos"][i] = dados["AlvoMenosKMenosValor"][i]  # criando nova coluna no dataframe original

        dados_aux = dados.cumsum()  # criar um dataframe auxiliar em que as colunas representam as somas acumuladas
        dados['C_Mais'] = dados_aux['C_Mais']
        dados['C_Menos'] = dados_aux['C_Menos']
        dados["C_MenosCompleto"] = dados_aux['C_Menos'] * (-1)

        return (dados, H)

    def Plot(self):
        SaidaCUSUM = self.CartaCUSUM()
        print(SaidaCUSUM[0])
        if self.tkvar.get() == "Superior":
            if self.tkvar1.get() == "Dispersão":
                plt.plot(SaidaCUSUM[0].index, SaidaCUSUM[0]["C_Mais"], label='C+', color="blue")
                plt.plot(SaidaCUSUM[0].index, SaidaCUSUM[0]['H'], label='H', color="red")
                plt.ylabel('Ci+')
                plt.xlabel('Média Amostral')
                plt.title('Carta CUSUM Tabular Superior')
                plt.grid(True)
                self.master.destroy()
                plt.show()
            elif self.tkvar1.get() == "Barras":
                plt.bar(SaidaCUSUM[0].index, SaidaCUSUM[0]["C_Mais"], label='C+', color="blue")
                plt.plot(SaidaCUSUM[0].index, SaidaCUSUM[0]['H'], label='H', color="red")
                plt.ylabel('Ci+')
                plt.xlabel('Média Amostral')
                plt.title('Carta CUSUM Tabular Superior')
                plt.grid(True)
                self.master.destroy()
                plt.show()
            else:
                tk.messagebox.showerror(title="Erro", message='Tipo de plotagem não selecionada!')
        elif self.tkvar.get() == "Inferior":
            if self.tkvar1.get() == "Dispersão":
                plt.plot(SaidaCUSUM[0].index, SaidaCUSUM[0]["C_Menos"], label='C-', color="blue")
                plt.plot(SaidaCUSUM[0].index, SaidaCUSUM[0]['H'], label='H', color="red")
                plt.ylabel('Ci-')
                plt.xlabel('Média Amostral')
                plt.title('Carta CUSUM Tabular Inferior')
                plt.grid(True)
                self.master.destroy()
                plt.show()
            elif self.tkvar1.get() == "Barras":
                plt.bar(SaidaCUSUM[0].index, SaidaCUSUM[0]["C_Menos"], label='C-', color="blue")
                plt.plot(SaidaCUSUM[0].index, SaidaCUSUM[0]['H'], label='H', color="red")
                plt.ylabel('Ci-')
                plt.xlabel('Média Amostral')
                plt.title('Carta CUSUM Tabular Inferior')
                plt.grid(True)
                self.master.destroy()
                plt.show()
            else:
                tk.messagebox.showerror(title="Erro", message='Tipo de plotagem não selecionada!')
        elif self.tkvar.get() == "Completa":
            if self.tkvar1.get() == "Dispersão":
                plt.plot(SaidaCUSUM[0].index, SaidaCUSUM[0]["C_Mais"], label='C+', color="grey")
                plt.plot(SaidaCUSUM[0].index, SaidaCUSUM[0]["C_MenosCompleto"], label='C-', color="blue")
                plt.plot(SaidaCUSUM[0].index, SaidaCUSUM[0]['H'], label='H', color="orange")
                plt.plot(SaidaCUSUM[0].index, -SaidaCUSUM[0]['H'], label='-H', color="green")
                plt.ylabel('Ci')
                plt.xlabel('Média Amostral')
                plt.title('Carta CUSUM Tabular Completa')
                plt.grid(True)
                self.master.destroy()
                plt.show()
            elif self.tkvar1.get() == "Barras":
                plt.bar(SaidaCUSUM[0].index, SaidaCUSUM[0]["C_Mais"], label='C+', color="grey")
                plt.bar(SaidaCUSUM[0].index, SaidaCUSUM[0]["C_MenosCompleto"], label='C-', color="blue")
                plt.plot(SaidaCUSUM[0].index, SaidaCUSUM[0]['H'], label='H', color="orange")
                plt.plot(SaidaCUSUM[0].index, -SaidaCUSUM[0]['H'], label='-H', color="green")
                plt.ylabel('Ci')
                plt.xlabel('Média Amostral')
                plt.title('Carta CUSUM Tabular Completa')
                plt.grid(True)
                self.master.destroy()
                plt.show()
            else:
                tk.messagebox.showerror(title="Erro", message='Tipo de plotagem não selecionada!')
        else:
            tk.messagebox.showerror(title="Erro", message='Tipo de gráfico CUSUM não selecionado!')


# root = tk.Tk()
# header = ["a","b"]
# path = "/"
# app=CartaCUSUM_Tabular(root,path,header)