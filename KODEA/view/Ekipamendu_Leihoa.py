import tkinter as tk
from tkinter import ttk
from controllers.DBKudeatzailea.DBKudeatzailea import DBKudeatzailea

dbk = DBKudeatzailea()

class Ekipamendu_Leihoa:

    def __init__(self):

        self.window = tk.Toplevel()
        self.window.title("Ekipamendu leihoa")
        self.window.geometry("400x250")
        self.window.resizable(False, False)

        #Ekipamenduko taula sortzen duen metodoaren deia
        self.ekipamenduTaulaSortu()
    # -------------------------------------------------------------#
    #Ekipamenduko taula sortuko duen metodoa
    def ekipamenduTaulaSortu(self):

        goiburuak=["Izena", "Distantzia totala"]
        self.ekiptaula = ttk.Treeview(self.window, columns=(0, 1), show='headings')

        #Aurretik zehaztutako goiburuak TreeView-ra gehitu
        for i, g in enumerate(goiburuak):
            self.ekiptaula.column(f"#{i}", minwidth=0, width=200)
            self.ekiptaula.heading(i, text=g)

        #Ekipamenduak klaseko objektuak bueltatzen dituen metodoaren deia
        datuak= dbk.ekipamenduakSortu()

        ekipamendua=[]
        for i in range(len(datuak)):
            e = []
            izena=datuak[i].izena

            #Ekipamenduak egindako kilometro kopurua lortu
            guztira= str(float(datuak[i].guztira/1000))  + "km"

            e.append(izena)
            e.append(guztira)
            ekipamendua.append(e)

        #Ekipamenduko datuak TreeView-ra gehitu
        for i, d in enumerate(ekipamendua):
            self.ekiptaula.insert(parent='', index=i, iid=i, values=d)
        self.ekiptaula.grid(row=0, column=0)

        #TreeView-eko bista aldatu
        s = ttk.Style()
        s.configure('Treeview', rowheight=45)
        s.configure("Treeview.Heading", font=('Helvetica', 9))
        s.configure("Treeview", font=('Helvetica', 9))

        self.window.mainloop()