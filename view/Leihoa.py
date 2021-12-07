import tkinter as tk
from tkinter import ttk, messagebox

from PIL import ImageTk, Image

from view.Ekipamendu_Leihoa import Ekipamendu_Leihoa
from view.Entrenamendu_Datuak import Entrenamendu_Datuak
from controllers.DBKudeatzailea.DBKudeatzailea import DBKudeatzailea

dbk=DBKudeatzailea()

class Leihoa():

    def __init__(self):

        self.window = tk.Tk()
        self.window.geometry('1050x562')
        self.window.resizable(False,False)
        self.window.title("Strava Hasiera")
        self.taula=None

        #Strava-ko logoa pantailaratzeko
        path = "view/strava.png"
        img = ImageTk.PhotoImage(Image.open(path))
        panel = tk.Label(self.window, image=img)
        panel.pack()
        panel.place(width=220, height=250)

        # -------------------------------------------------------------#
        #                           FRAMEAK                            #
        # -------------------------------------------------------------#

        # Filtraketa aukerak dituen frame-a
        self.filtraketaframe = tk.LabelFrame(self.window, text="Filtraketa Eremua:")
        self.filtraketaframe.pack(side=tk.LEFT)
        self.filtraketaframe.config(relief="ridge")
        self.filtraketaframe.config(bd=5)

        # Eragiketen aukerak dituen frame-a
        self.eragiketaframe = tk.LabelFrame(self.window, text="Eragiketa Eremua:")
        self.eragiketaframe.pack(side=tk.TOP)

        #Eragiketa framean Kurtsorea aldatzeko kodea
        self.eragiketaframe.config(relief="ridge")
        self.eragiketaframe.config(bd=5)

        # Leihoa erakusteko erabiliko den frame-a
        self.main_frame = tk.Frame(self.window)
        self.main_frame.pack()

        # -------------------------------------------------------------#
        def limitSizeDay(*args):
            value = dayValue.get()
            value2 = dayValue2.get()
            if len(value) > 10: dayValue.set(value[:10])
            if len(value2) > 10: dayValue2.set(value2[:10])




        #Noiztik eremuaren formatua definitzen duen metodoa
        def noiztikFormatua(event):
            if event.char.isdigit():
                testua = noiztikEntry.get()
                letrak = 0
                for i in testua:
                    letrak += 1

                if letrak == 4:
                    noiztikEntry.insert(4, "-")
                elif letrak == 7:
                    noiztikEntry.insert(7, "-")
            else:
                return "break"

        # -------------------------------------------------------------#

        # Nora eremuaren formatua definitzen duen metodoa
        def noraFormatua(event):
            if event.char.isdigit():
                testua = noraEntry.get()
                letrak = 0
                for i in testua:
                    letrak += 1

                if letrak == 4:
                    noraEntry.insert(4, "-")
                elif letrak == 7:
                    noraEntry.insert(7, "-")
            else:
                return "break"

        # -------------------------------------------------------------#
        #                   Entrenamendu Taula                         #
        # -------------------------------------------------------------#

        #Entrenamenduen filtraketa gauzatzen duen metodoaren deia (1.Deia, entrenamendu guztiak inprimatu)
        self.filtraketaErakutsi('','',"Guztiak")

        # -------------------------------------------------------------#
        #                   Entrenamendu Taula                         #
        # -------------------------------------------------------------#

        #Entrenamendu desberdinen mota lortu
        motak=dbk.motakLortu()
        motak.append("Guztiak")
        dayValue = tk.StringVar()
        dayValue.trace('w', limitSizeDay)
        dayValue2 = tk.StringVar()
        dayValue2.trace('w', limitSizeDay)

        #Entrenamenduko filtraketen noiztik eremua sortu
        noiztikLabel = tk.Label(self.filtraketaframe, text="Noiztik: ", borderwidth=10)
        noiztikEntry = tk.Entry( self.filtraketaframe, justify=tk.LEFT, textvariable=dayValue)

        #Noiztik formatua zehazteko metodoaren deia
        noiztikEntry.bind("<Key>", noiztikFormatua)
        noiztikEntry.bind("<BackSpace>", lambda _: noiztikEntry.delete(tk.END))

        #Entrenamenduko filtraketen nora eremua sortu
        noraLabel = tk.Label(self.filtraketaframe, text="Nora: ", borderwidth=10)
        noraEntry = tk.Entry( self.filtraketaframe, justify=tk.LEFT, textvariable=dayValue2)

        #Nora formatua zehazteko metodoaren deia
        noraEntry.bind("<Key>", noraFormatua)
        noraEntry.bind("<BackSpace>", lambda _: noraEntry.delete(tk.END))

        #Entrenamenduko filtraketen mota eremua sortu
        motaLabel = tk.Label(self.filtraketaframe, text="Mota: ", borderwidth=10)
        motaEntry = ttk.Combobox( self.filtraketaframe, values=motak, textvariable='motaEntry', state="readonly")
        motaEntry.current(len(motak)-1)

        #Entrenamenduko filtraketarako botoia sortu
        bilatuBotoia = tk.Button( self.filtraketaframe, text="Bilatu", command=lambda: self.filtraketaErakutsi(noiztikEntry.get(), noraEntry.get(), motaEntry.get()))

        #Widget-ak pantailaratu
        noiztikLabel.grid(row=0, column=0)
        noiztikEntry.grid(row=0, column=1)
        noraLabel.grid(row=1, column=0)
        noraEntry.grid(row=1, column=1)
        motaLabel.grid(row=2, column=0)
        motaEntry.grid(row=2, column=1)
        bilatuBotoia.grid(row=3, column=1)

        # -------------------------------------------------------------#
        #      Eguneratu eta Ekipamenduak erakusteko botoiak           #
        # -------------------------------------------------------------#

        tk.Label(self.eragiketaframe,text='            ').grid(row=0, column=0)

        #DB-ko taulen datuak eguneratzen dituen botoia sortu
        eguneratuBotoia = tk.Button(self.eragiketaframe, text="Datuak eguneratu", command=lambda: self.mezuDatuakKargatu())
        eguneratuBotoia.grid(row=5, column=1)

        # Ekipamenduen informazioa erakusteko botoia sortu
        ekipamenduBotoia = tk.Button(self.eragiketaframe, text="Ekipamenduak ikusi", command=lambda: Ekipamendu_Leihoa())
        ekipamenduBotoia.grid(row=5, column=3)

        tk.Label(self.eragiketaframe, text='            ').grid(row=0, column=4)

        self.window.mainloop()

    # -------------------------------------------------------------#
    #                         FUNTZIOAK                            #
    # -------------------------------------------------------------#

    #Datuak eguneratuko ditu eta mezu bat aterako du amaitzean
    def mezuDatuakKargatu(self):
        dbk.datuakKargatu()
        print(messagebox.showinfo(message="Tupla eguneratuak: 30", title="Eguneraketa"))

    # -------------------------------------------------------------#

    #Entrenamenduen filtraketan zehaztutako balioak betetzen dituzten entrenamenduak inprimatu
    def filtraketaErakutsi(self,noiztik, nora, mota):

        #Entrenamenduko zutabeen goiburuak zehaztu
        goiburuak = ["Izena", "Data", "Iraupena", "Mota"]
        datuak = []

        #Entrenamenduen objektuen zerrenda lortu
        entrenamenduLista=dbk.bilaketaErakutsi(noiztik, nora, mota)

        #Entrenamenduen zerrenda hutsik badago ez inprimatu ezer
        if (len(entrenamenduLista)<=0):
           datuak = []
        else:
            #Entrenamenduen datuak lortu
            for lerro in range(len(entrenamenduLista)):
                izena = entrenamenduLista[lerro].izena
                noiz = entrenamenduLista[lerro].noiz
                mugimenduDenb = entrenamenduLista[lerro].mugimenduDenb
                mota = entrenamenduLista[lerro].mota

                #Entrenamenduen datuen egitura lortu TreeView-ean txertatzeko
                datuak2 = []
                for zutabe in range(4):
                        if zutabe ==0:
                            datuak2.append(izena)
                        if zutabe == 1:
                           datuak2.append(noiz)
                        if zutabe == 2:
                            # Denborak inprimatzeko min eta s moduan
                            min = int(mugimenduDenb) // 60
                            s = int(mugimenduDenb) % 60
                            h=0
                            if min >= 60:
                                h = int(min) // 60
                                min = int(min) % 60
                            datuak2.append(str(h) + "h "+str(min) + "min " + str(s) + "s")
                        if zutabe ==3:
                            datuak2.append(mota)
                datuak.append(datuak2)


        if (self.taula!=None):   #Treeview ezabatzeko
            self.taula.destroy()

        #TreeView-a sortu
        self.taula = ttk.Treeview(self.main_frame, columns=(0, 1, 2, 3), show='headings')

        #Goiburuak TreeView-an txertatu
        for i, g in enumerate(goiburuak):
            self.taula.column(f"#{i}", minwidth=0, width=200)
            self.taula.heading(i, text=g)

        #Entrenamenduen datuak TreeView-an txertatu
        for i, d in enumerate(datuak):
            self.taula.insert(parent='', index=i, iid=i, values=d)
        self.taula.grid(row=0, column=0)

        #TreeView-eko estetika aldatu
        s=ttk.Style()
        s.configure('Treeview', rowheight=45)
        s.configure("Treeview.Heading", font=('Helvetica', 9))
        s.configure("Treeview", font=('Helvetica', 9))

        #TreeView-an entrenamenduren bat aukeratzean laranjaz margozteko
        s.configure("Treeview", background="#E1E1E1",foreground="#000000", fieldbackground="#E1E1E1")
        s.map('Treeview', background=[('selected', "DARKORANGE1")])

        #Lerro batean doble klik egiterakoan aukeratutako entrenamenduaren datuak atera
        if (len(datuak)>0):
            self.taula.bind("<Double-1>", lambda ev: Entrenamendu_Datuak(entrenamenduLista[int(self.taula.selection()[0])]))