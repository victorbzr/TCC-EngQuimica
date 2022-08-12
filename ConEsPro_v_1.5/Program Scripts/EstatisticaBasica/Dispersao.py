import tkinter as tk
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression # pacote de regressão linear
import matplotlib.pyplot as plt

class DiagramaDispersao:
    def __init__(self, master, path, header):
        self.master = master
        self.path = path
        self.header = header
        self.master.title('Diagrama de Dispersão')
        self.master.wm_iconbitmap('Imagens\Logo.ico')
        Labels_Title = tk.Label(self.master, text='Selecione as colunas que contenham\nas variáveis para o teste de correlação')
        Labels_Title.grid(row=0)
        Labels_Xaxis = tk.Label(self.master, text='Eixo X:')
        Labels_Xaxis.grid(row=1)
        self.frame = tk.Frame(self.master)
        self.frame.grid(row=2)
        self.xvar = tk.IntVar()
        i = 0
        for h in self.header:
            l = tk.Radiobutton(self.frame, text=h, variable=self.xvar, value=i, activebackground='#ffffff').grid(row=0, column=i)
            i = i + 1

        Labels_Yaxis = tk.Label(self.master, text='Eixo Y:')
        Labels_Yaxis.grid(row=3)
        self.frame1 = tk.Frame(self.master)
        self.frame1.grid(row=4)
        self.yvar = tk.IntVar()
        i = 0
        for h in self.header:
            l = tk.Radiobutton(self.frame1, text=h, variable=self.yvar, value=i, activebackground='#ffffff').grid(row=0, column=i)
            i = i + 1

        b = tk.Button(self.master, text='Mostrar Resultados', command=lambda: self.Plot()).grid(row=5)
        self.master.mainloop()

    def Plot(self):
        try:
            dados = pd.read_csv(self.path)
        except:
            dados = pd.read_excel(self.path, engine='openpyxl')
        dados = dados.dropna(1, how='all')
        dados = dados.dropna(0, how='all')
        droplist = []
        for i in range(len(self.header)):
            if not i == self.xvar.get() and not i == self.yvar.get():
                droplist.append(self.header[i])
        dados = dados.drop(droplist, axis=1).copy()
        replicas = pd.DataFrame()
        replicas['x'] = dados[self.header[self.xvar.get()]]
        replicas['y'] = dados[self.header[self.yvar.get()]]
        replicas = replicas.dropna(0, how='any')
        x = np.array(replicas['x']).reshape((-1, 1))
        y = np.array(replicas['y'])
        model = LinearRegression().fit(x, y)
        r_sq = model.score(x, y)
        print('coefficient of determination:', r_sq)
        print('intercept:', model.intercept_)
        print('slope:', model.coef_)
        aux = str(model.coef_).replace('[', '').replace(']', '')  # tirando o "slope do colchete manipulando como string"
        coeficiente = float(aux)  # escrevendo a string como um número
        replicas["R2"] = r_sq
        replicas["intercept"] = model.intercept_
        replicas["slope"] = coeficiente
        fig, ax = plt.subplots()
        x_max = replicas['x'].max()
        x_min = replicas['x'].min()
        ax.set_xlim(x_min, x_max)
        plt.style.use("classic")
        plt.plot(replicas['x'], replicas['y'], "o", color="gray", ms=5)  # ms tamanho do símbolo
        plt.ylabel(self.header[self.yvar.get()], fontsize=14)
        plt.xlabel(self.header[self.xvar.get()], fontsize=14)
        plt.title('Diagrama de Correlação', fontsize=14, fontweight="bold")
        textstr = '\n'.join((r'$\mathrm{R^2}=%.4f$' % (r_sq,),
                             r'$\mathrm{CoeficienteLinear}=%.4f$' % (model.intercept_,),
                             r'$\mathrm{CoeficienteAngular}=%.4f$' % (coeficiente,)))
        # these are matplotlib.patch.Patch properties
        props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
        # place a text box in upper left in axes coords
        plt.text(0.05, 0.95, textstr, transform=ax.transAxes, fontsize=14,
                 verticalalignment='top', bbox=props)

        x1 = np.arange(x_min-1,x_max+1)
        y1 = coeficiente * x1 + model.intercept_
        plt.plot(x1, y1, "-", color="green")
        plt.show()


# root = tk.Tk()
# header = ["a","b"]
# path = "/"
# app=Dispersao(root,path,header)