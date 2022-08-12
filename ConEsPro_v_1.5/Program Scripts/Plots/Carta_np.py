import pandas as pd
import tkinter as tk
import matplotlib.pyplot as plt

class CartaNP:
    def __init__(self, master, path, header):
        self.path = path
        self.master = master
        self.header = header
        self.master.title('Carta np')
        self.master.wm_iconbitmap('Imagens\Logo.ico')
        Labels_Title = tk.Label(self.master, text='Selecione a(s) coluna(s) que\ncontém o número defeituosos por amostra:')
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

        l1 = tk.Label(self.master, text='Tamanho das amostras:').grid(row=2)

        self.frame2 = tk.Frame(self.master)
        self.frame2.grid(row=3)
        self.value1 = tk.IntVar()
        self.e1 = tk.Entry(self.frame2, textvariable=self.value1).grid(row=4)

        Plot = tk.Button(self.master, text='Mostrar resultados', command=self.Plot).grid(row=5)
        save = tk.Button(self.master, text='Salvar', command=lambda: self.Salvar()).grid(row=6, pady=5)

        self.master.mainloop()

    def Salvar(self):
        from .Salvar import SalvarDados
        app = SalvarDados(self.CartaNP())

    def enableEntry(self, entry):
        entry.configure(state="normal")
        entry.update()

    def disableEntry(self, entry):
        entry.configure(state="disabled")
        entry.update()

    def CartaNP(self):
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

        dados["UnidNConf"] = replicas.mean(axis=1)  # fazendo a média por linha
        # media amostral (por linha). Se não existirem réplicas, a média será o próprio valor medido


        TamanhoAmostra = [self.value1.get()] * len(dados)
        dados["TamanhoAmostra"]=TamanhoAmostra

        dados['p_barraAmostra'] = dados['UnidNConf'] / dados["TamanhoAmostra"]
        dados['p_barra'] = dados["p_barraAmostra"].mean()
        dados['np']=dados["TamanhoAmostra"]*dados['p_barra']
        dados['Sigma']=(dados['p_barra']*(1-dados['p_barra']) * dados["TamanhoAmostra"]) ** 0.5
        dados['LSC'] = dados["TamanhoAmostra"]*dados['p_barra'] + 3 * dados['Sigma']
        dados['LIC'] = dados["TamanhoAmostra"]*dados['p_barra'] - 3 * dados['Sigma']
        for i in range(len(dados['LIC'])):
            if dados['LIC'][i]<0:
                dados['LIC'][i]=0
        dados["ResiduoSuperior"] = dados['LSC'] - dados['UnidNConf']
        dados["ResiduoInferior"] = dados['LIC'] - dados['UnidNConf']
        print(dados)
        return (dados)

    def Plot(self):
        SaidaCartaNP = self.CartaNP()

        cont = 0
        for i in range(len(SaidaCartaNP['LSC'])):
            if SaidaCartaNP["UnidNConf"][i] > SaidaCartaNP['LSC'][i] or SaidaCartaNP["UnidNConf"][
                i] < SaidaCartaNP["LIC"][i]:
                cont = 1
        if cont == 1:
            print('Sistema fora de controle!')
            tk.messagebox.showinfo(title='Resultados Carta NP', message='Sistema fora de controle!')
        else:
            print('Sistema sob controle!')
            tk.messagebox.showinfo(title='Resultados Carta NP', message='Sistema sob controle!')

        plt.plot(SaidaCartaNP.index, SaidaCartaNP["UnidNConf"], '-o', label='Número de defeituosos(di)')
        plt.plot(SaidaCartaNP.index, SaidaCartaNP["np"], '--', label='Média Geral(np)')
        plt.plot(SaidaCartaNP.index, SaidaCartaNP["LIC"], '--', label='LIC')
        plt.plot(SaidaCartaNP.index, SaidaCartaNP["LSC"], '--', label='LSC')
        plt.ylabel('Números de defeituosos')
        plt.xlabel('Amostra')
        plt.title('Gráfico NP - Número de Defeituosos')
        plt.legend(loc="best")
        teste = (SaidaCartaNP['np'][0] - SaidaCartaNP['LIC'][0])
        plt.annotate('LIC', xy=(1, SaidaCartaNP['LIC'][0]), xytext=(3, SaidaCartaNP['LIC'][0] + teste/3),
                     arrowprops=dict(facecolor='black'))
        plt.annotate('LSC', xy=(1, SaidaCartaNP['LSC'][0]), xytext=(3, SaidaCartaNP['LSC'][0] - teste/3),
                     arrowprops=dict(facecolor='black'))
        plt.annotate('Média', xy=(1, SaidaCartaNP['np'][0]), xytext=(3, SaidaCartaNP['np'][0] - teste/3),
                     arrowprops=dict(facecolor='black'))
        plt.grid(True)
        plt.show()

#root = tk.Tk()
#header = ["a","b",'c','d','e','f','g','h','i','j','k']
#path = "/"
#app=CartaP(root,path,header)