import tkinter as tk
from tkinter import ttk
import urllib.parse
import io
import urllib3
from PIL import ImageTk, Image
from view import ScrollContainer
from controllers.DBKudeatzailea.DBKudeatzailea import DBKudeatzailea
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

dbk=DBKudeatzailea()

class Entrenamendu_Datuak():

    def __init__(self,entrenamendua):

        self.window = tk.Toplevel()
        self.window.geometry('800x700')
        self.window.title("Entrenamendu Datuak")

        #Leihoaren scroll-a sortu
        scroll = ScrollContainer(self.window)
        self.main_frame = scroll.second_frame

        # -------------------------------------------------------------#
        #                           MAPA                               #
        # -------------------------------------------------------------#

        #Entrenamendu batek mapa eskuragarria baldin badu inprimatu
        if not (entrenamendua.mapa=="" or  entrenamendua.mapa==None or entrenamendua.mapa=="None"):
            self.mapaInprimatu(entrenamendua)

        # -------------------------------------------------------------#
        #                  ENTRENAMENDU DATUAK                         #
        # -------------------------------------------------------------#

        #Entrenamendu baten datuak daukan taula
        self.datuGuztiak = tk.Frame(self.main_frame)
        self.datuGuztiak.pack()
        self.datuGuztiak.config(relief="solid")
        self.datuGuztiak.config(bd=3)

        #Entrenamendu baten ID-a gordetzen duen laukia
        self.datuParea1 = tk.Frame(self.datuGuztiak)
        self.datuParea1.grid(row=0, column=0)
        self.datuParea1.config(relief="solid")
        self.datuParea1.config(bd=1)

        idLabel = tk.Label(self.datuParea1, text="Id", borderwidth=10, width=20)
        idLabel.config(bg="DarkOrange1", fg="white")
        idLabel2 = tk.Label(self.datuParea1, text=entrenamendua.id, borderwidth=10, width=20)
        idLabel.pack()
        idLabel2.pack()

        #Entrenamendu baten Izena gordetzen duen laukia
        self.datuParea2 = tk.Frame(self.datuGuztiak)
        self.datuParea2.grid(row=0, column=1)
        self.datuParea2.config(relief="solid")
        self.datuParea2.config(bd=1)

        izenaLabel = tk.Label(self.datuParea2, text="Izena", borderwidth=10, width=20)
        izenaLabel.config(bg="DarkOrange1", fg="white")
        izenaLabel2 = tk.Label(self.datuParea2, text=entrenamendua.izena, borderwidth=10, width=20)
        izenaLabel.pack()
        izenaLabel2.pack()

        #Entrenamendu baten Mugimendu denbora (s) gordetzen duen laukia
        self.datuParea3 = tk.Frame(self.datuGuztiak)
        self.datuParea3.grid(row=0, column=2)
        self.datuParea3.config(relief="solid")
        self.datuParea3.config(bd=1)

        mugimenduDenbLabel = tk.Label(self.datuParea3, text="Mugimendu Denbora (s)", borderwidth=10, width=20)
        mugimenduDenbLabel.config(bg="DarkOrange1", fg="white")
        mugimenduDenbLabel2 = tk.Label(self.datuParea3, text=entrenamendua.mugimenduDenb, borderwidth=10, width=20)
        mugimenduDenbLabel.pack()
        mugimenduDenbLabel2.pack()

        #Entrenamendu baten mota gordetzen duen laukia
        self.datuParea4 = tk.Frame(self.datuGuztiak)
        self.datuParea4.grid(row=1, column=0)
        self.datuParea4.config(relief="solid")
        self.datuParea4.config(bd=1)

        motaLabel = tk.Label(self.datuParea4, text="Mota", borderwidth=10, width=20)
        motaLabel.config(bg="DarkOrange1", fg="white")
        motaLabel2 = tk.Label(self.datuParea4, text=entrenamendua.mota, borderwidth=10, width=20)
        motaLabel.pack()
        motaLabel2.pack()

        #Entrenamendu baten data gordetzen duen laukia
        self.datuParea5 = tk.Frame(self.datuGuztiak)
        self.datuParea5.grid(row=1, column=1)
        self.datuParea5.config(relief="solid")
        self.datuParea5.config(bd=1)

        noizLabel = tk.Label(self.datuParea5, text="Noiz", borderwidth=10, width=20)
        noizLabel.config(bg="DarkOrange1", fg="white")
        noizLabel2 = tk.Label(self.datuParea5, text=entrenamendua.noiz, borderwidth=10, width=20)
        noizLabel.pack()
        noizLabel2.pack()

        #Entrenamendu baten abiadura maximoa gordetzen duen laukia
        self.datuParea6 = tk.Frame(self.datuGuztiak)
        self.datuParea6.grid(row=1, column=2)
        self.datuParea6.config(relief="solid")
        self.datuParea6.config(bd=1)

        abiaduraMaxLabel = tk.Label(self.datuParea6, text="Abiadura Maximoa", borderwidth=10, width=20)
        abiaduraMaxLabel.config(bg="DarkOrange1", fg="white")
        abiaduraMaxLabel2 = tk.Label(self.datuParea6, text=entrenamendua.abiaduraMax, borderwidth=10, width=20)
        abiaduraMaxLabel.pack()
        abiaduraMaxLabel2.pack()

        #Entrenamendu baten bataz besteko abiadura gordetzen duen laukia
        self.datuParea7 = tk.Frame(self.datuGuztiak)
        self.datuParea7.grid(row=2, column=0)
        self.datuParea7.config(relief="solid")
        self.datuParea7.config(bd=1)

        bbAbiaduraLabel = tk.Label(self.datuParea7, text="Batazbesteko Abiadura", borderwidth=10, width=20)
        bbAbiaduraLabel.config(bg="DarkOrange1", fg="white")
        bbAbiaduraLabel2 = tk.Label(self.datuParea7, text=entrenamendua.bbAbiadura, borderwidth=10, width=20)
        bbAbiaduraLabel.pack()
        bbAbiaduraLabel2.pack()

        #Entrenamendu baten distantzia (m) gordetzen duen laukia
        self.datuParea8 = tk.Frame(self.datuGuztiak)
        self.datuParea8.grid(row=2, column=1)
        self.datuParea8.config(relief="solid")
        self.datuParea8.config(bd=1)

        distantziaLabel = tk.Label(self.datuParea8, text="Distantzia (m)", borderwidth=10, width=20)
        distantziaLabel.config(bg="DarkOrange1", fg="white")
        distantziaLabel2 = tk.Label(self.datuParea8, text=entrenamendua.distantzia, borderwidth=10, width=20)
        distantziaLabel.pack()
        distantziaLabel2.pack()

        #Entrenamendu baten erretako kaloriak gordetzen duen laukia
        self.datuParea9 = tk.Frame(self.datuGuztiak)
        self.datuParea9.grid(row=2, column=2)
        self.datuParea9.config(relief="solid")
        self.datuParea9.config(bd=1)

        erreKaloriaLabel = tk.Label(self.datuParea9, text="Kaloria Erreta", borderwidth=10, width=20)
        erreKaloriaLabel.config(bg="DarkOrange1", fg="white")
        erreKaloriaLabel2 = tk.Label(self.datuParea9, text=entrenamendua.erreKaloria, borderwidth=10, width=20)
        erreKaloriaLabel.pack()
        erreKaloriaLabel2.pack()

        # -------------------------------------------------------------#
        #                      GRAFIKOAK                               #
        # -------------------------------------------------------------#

        #Grafikoa eta aukerak dituen Frame-a sortu (Scroll-a duen framearen barruan)
        self.grafikoak = tk.Frame(self.main_frame)
        self.grafikoak.pack()

        #Grafikoaren aukerak dituen Frame-a sortu
        self.grafikoAukerak = tk.LabelFrame(self.grafikoak, text="Aukerak")
        self.grafikoAukerak.pack(side=tk.LEFT)

        #Medizio desberdinak lortzeko metodoaren deia
        nMotak = dbk.neurketaMotakLortu()

        #Aukerako botoien egoera konprobatzeko aldagaiak
        self.radioValue = tk.IntVar()
        self.checkValue = tk.StringVar()

        #Grafikoaren aukerak adierazteko botoiak sortu neurketa mota desberdinen arabera
        i = 0
        while i<len(nMotak):
            mota = nMotak[i][0]
            if mota == "cadence":               #Kadentzia botoia sortu
                kadentziaB=tk.Checkbutton(self.grafikoAukerak, text="Kadentzia", command=lambda:self.grafikoaInprimatu(entrenamendua), variable=self.checkValue, onvalue="cadence")
                kadentziaB.select()
            elif mota == "distance":            #Distantzia botoia sortu
                distantziaB=tk.Radiobutton(self.grafikoAukerak, text="Distantzia", command=lambda:self.grafikoaInprimatu(entrenamendua),variable=self.radioValue, value=0)
            elif mota == "grade_smooth":        #Aldapa leunduta botoia sortu
                aldapaB=tk.Checkbutton(self.grafikoAukerak, text="Aldapa leunduta", command=lambda:self.grafikoaInprimatu(entrenamendua),  variable=self.checkValue, onvalue="grade_smooth")
            elif mota == "heartrate":           #Pultsazioak botoia sortu
                pultsazioakB=tk.Checkbutton(self.grafikoAukerak, text="Pultsazioak", command=lambda:self.grafikoaInprimatu(entrenamendua), variable=self.checkValue, onvalue="heartrate")
            elif mota == "moving":              #Mugitzen botoia sortu
                mugitzenB=tk.Checkbutton(self.grafikoAukerak, text="Mugitzen", command=lambda:self.grafikoaInprimatu(entrenamendua),  variable=self.checkValue, onvalue="moving")
            elif mota == "time":                #Denbora botoia sortu
                denboraB=tk.Radiobutton(self.grafikoAukerak, text="Denbora", command=lambda:self.grafikoaInprimatu(entrenamendua),variable=self.radioValue,value=1)
            elif mota == "velocity_smooth":     #Abiadura leunduta botoia sortu
                abiaduraB=tk.Checkbutton(self.grafikoAukerak, text="Abiadura leunduta", command=lambda:self.grafikoaInprimatu(entrenamendua),  variable=self.checkValue, onvalue="velocity_smooth")
            i=i+1

        #Y ardatzaren Label-a sortu
        y = tk.Label(self.grafikoAukerak, text="Y", borderwidth=10, width=20)
        y.pack()

        #Y ardatzako botoiak jarri
        kadentziaB.pack()
        aldapaB.pack()
        pultsazioakB.pack()
        mugitzenB.pack()
        abiaduraB.pack()

        #X ardatzaren Label-a sortu
        x = tk.Label(self.grafikoAukerak, text="X", borderwidth=10, width=20)
        x.pack()

        #X ardatzako botoiak jarri
        distantziaB.pack()
        denboraB.pack()

        #Denbora aukera defektuz markatu eta distantzia defektuz desmarkatu
        denboraB.select()
        distantziaB.deselect()

        #Grafikoaren irudia eramango duen Frame-a sortu
        self.grafikoIrudia = tk.LabelFrame(self.grafikoak, text="Grafikoa:",width=600, height=300)
        self.grafikoIrudia.pack()

        #Container-aren tamaina ez aldatzeko (Bestela grafikoak gero eta txikiagoak dira eguneratzean)
        self.grafikoIrudia.propagate(0)

        #Grafikoaren irudia pantailaratzen duen metodoaren deia
        self.grafikoaInprimatu(entrenamendua)

        # -------------------------------------------------------------#
        #                      BUELTAK                                 #
        # -------------------------------------------------------------#

        #Entrenamendu baten buelten informazioa eta aukerak eramango duen Frame-a sortu
        self.bueltaktaula=tk.LabelFrame(self.main_frame, text="Bueltak (LAP)")
        self.bueltaktaula.pack()

        #Entrenamendu baten buelten aukerak eramango dituen Frame-a sortu
        self.bueltakAukera = tk.LabelFrame(self.bueltaktaula, text="aukerak")
        self.bueltakAukera.pack()

        #Entrenamendu baten buelten informazioa eramango duen Scroll-a sortu
        scroll2 = ScrollContainer(self.bueltaktaula)
        self.main_frame2 = scroll2.second_frame
        self.main_frame2.pack()

        #Aukerako botoien egoera konprobatzeko aldagaiak
        self.izenaValue = tk.StringVar()
        self.mugimenduValue = tk.StringVar()
        self.distantziaValue = tk.StringVar()
        self.hasiDataValue = tk.StringVar()
        self.abiaduraMaxValue = tk.StringVar()
        self.bbAbiaduraValue = tk.StringVar()

        #Buelten aukeren botoiak sortu eta deitu beharreko funtzioak zehaztu
        izenaCheck = tk.Checkbutton(self.bueltakAukera, text="Izena" , command=lambda: self.bueltakInprimatu(entrenamendua), variable=self.izenaValue, onvalue="izena", offvalue="")
        mugimenduCheck = tk.Checkbutton(self.bueltakAukera, text="Mugimendu Denbora", command=lambda: self.bueltakInprimatu(entrenamendua), variable=self.mugimenduValue, onvalue="mugimenduDenb", offvalue="")
        distantiaCheck = tk.Checkbutton(self.bueltakAukera, text="Distantzia", command=lambda: self.bueltakInprimatu(entrenamendua), var=self.distantziaValue, onvalue="distantzia", offvalue="")
        hasiDataCheck = tk.Checkbutton(self.bueltakAukera, text="HasiData", command=lambda: self.bueltakInprimatu(entrenamendua),variable=self.hasiDataValue, onvalue="hasiData", offvalue="")
        abiaduraMaxCheck = tk.Checkbutton(self.bueltakAukera, text="Abiadura Max", command=lambda: self.bueltakInprimatu(entrenamendua),variable=self.abiaduraMaxValue, onvalue="abiaduraMax", offvalue="")
        bbAbiaduraCheck = tk.Checkbutton(self.bueltakAukera, text="Batazbesteko abiadura", command=lambda: self.bueltakInprimatu(entrenamendua),variable=self.bbAbiaduraValue, onvalue="bbAbiadura", offvalue="")

        #Botoiak jarri eta guztiak defektuz markatu
        izenaCheck.grid(row=0, column=0)
        izenaCheck.select()
        mugimenduCheck.grid(row=0, column=1)
        mugimenduCheck.select()
        distantiaCheck.grid(row=0, column=2)
        distantiaCheck.select()
        hasiDataCheck.grid(row=0, column=3)
        hasiDataCheck.select()
        abiaduraMaxCheck.grid(row=0, column=4)
        abiaduraMaxCheck.select()
        bbAbiaduraCheck.grid(row=0, column=5)
        bbAbiaduraCheck.select()

        self.bueltaInfo = None

        #Buelten informazioa inprimatzen duen metodoaren deia
        self.bueltakInprimatu(entrenamendua)

        self.window.mainloop()

    # -------------------------------------------------------------#
    #                      FUNTZIOAK                               #
    # -------------------------------------------------------------#

    #Entrenamendu konkretu bateko mapa inprimatzen duen funtzioa
    def mapaInprimatu(self, entrenamendua):

        #Mapa eskatzeko access token-a
        token = "pk.eyJ1Ijoic3RyYXZhMTIzIiwiYSI6ImNrd25keThkNzJsM3Eyd21qZHZ2MHRzZWkifQ.eEXCvJISiXh5sQitVVwhrA"

        #Entrenamenduko maparen polylinea lortu
        polyline=entrenamendua.mapa

        #Marraztuko den ibilbidearen lodiera eta kolorea
        strokeWidth = 1
        strokeColor = "f44"

        #Mapa lortzeko HTTP eskaera
        http = urllib3.PoolManager()
        polyline_ = urllib.parse.quote_plus(polyline.encode("utf-8"))
        path = f"path-{strokeWidth}+{strokeColor}({polyline_})"
        host = "https://api.mapbox.com/styles/v1/mapbox/streets-v11/static/"
        tamaina = "/auto/500x300"
        url = f"{host}{path}{tamaina}?access_token={token}"
        em = http.request('GET', url)

        # Irudiaren data irakurri eta argazkia sortu
        self.img = Image.open(io.BytesIO(em.data))

        # Tkinter-en argazkia sortu (oso inportantea self-ekin gordetzea, bestela argazkia ezabatu egingo da)
        self.img2 = ImageTk.PhotoImage(self.img)

        # Argazkia Label batean sartu
        panel = tk.Label(self.main_frame, image=self.img2)
        panel.pack(side=tk.TOP)

    # -------------------------------------------------------------#

    #Grafikoak inprimatuko dituen funtzioa
    def grafikoaInprimatu(self, entrenamendua):

        #Entrenamenduaren id-a lortu
        id=entrenamendua.id

        #X Ardatza lortu (RadioButton-eko balioak hartu)
        if (self.radioValue.get()==0):                  #Distantzia aukeratu da
            xbalioa="Distantzia"

            #Distantzia neurketak lortu
            xZer=dbk.neurketakLortu("distance", id)
        else:                                           #Denbora aukeratu da
            xbalioa = "Denbora"

            #Denbora neurketak lortu
            xZer=dbk.neurketakLortu("time", id)

        # Y Ardatza lortu (CheckButton-eko balioak hartu)
        yZer=dbk.neurketakLortu(str(self.checkValue.get()), id)

        #Neurketa bateko datuak falta badira ez inprimatu ezer
        if (len(yZer)<=0):
            xZer=[0]
            yZer=[0]

        # Aurretik dauden grafikoak ezabatu egingo ditugu lehenengo
        for widget in self.grafikoIrudia.winfo_children():
            widget.destroy()

        # Figura eta Axis-a sortu
        fig = plt.Figure(figsize=(9, 4), dpi=80, tight_layout=True)
        ax = fig.add_subplot(111)
        mapeado = range(len(xZer))

        #Funtzioaren irudia sortu eta kolorea zehaztu
        ax.plot(xZer, yZer,  color="tab:blue")
        plt.xticks(mapeado, yZer)

        # Bi ardatzen izenak jarri
        ax.set_xlabel(xbalioa)
        ax.set_ylabel(str(self.checkValue.get()))

        # Canvas elementua sortu eta figura sartu goian sortu dugun kontenedorean
        canvas = FigureCanvasTkAgg(fig, master=self.grafikoIrudia)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, expand=1)

    # -------------------------------------------------------------#

    #Bueltak inprimatzen dituen funtzioa
    def bueltakInprimatu(self, entrenamendua):

        #Buelten informazioko TreeView bat jada existitzen den begiratu (Existitzen bada ezabatu)
        if self.bueltaInfo != None :
            for i in self.bueltaInfo.get_children():
                self.bueltaInfo.delete(i)

        #Buelten informazioa bistaratzen duen TreeView-a sortu
        self.bueltaInfo = ttk.Treeview(self.main_frame2, columns=(0, 1, 2, 3, 4, 5), show='headings')

        aukeratutakoGoiburuak = []

        #Markatutako goiburuak zeintzuk diren begiratu (CheckButton-en balioak)
        if (self.izenaValue.get() == "izena"):
            aukeratutakoGoiburuak.append("Izena")
        if (self.mugimenduValue.get() == "mugimenduDenb"):
            aukeratutakoGoiburuak.append("Mugimendu Denbora")
        if (self.distantziaValue.get() == "distantzia"):
            aukeratutakoGoiburuak.append("Distantzia")
        if (self.hasiDataValue.get() == "hasiData"):
            aukeratutakoGoiburuak.append("HasiData")
        if (self.abiaduraMaxValue.get() == "abiaduraMax"):
            aukeratutakoGoiburuak.append("Abiadura Max")
        if (self.bbAbiaduraValue.get() == "bbAbiadura"):
            aukeratutakoGoiburuak.append("Batazbesteko abiadura")

        #Goiburuak TreeView-ean txertatu
        for i, g in enumerate(aukeratutakoGoiburuak):
            self.bueltaInfo.column(f"#{i}", minwidth=0, width=200)
            self.bueltaInfo.heading(i, text=g)

        # Buelta objektuen array-a bueltatu
        datuak = dbk.bueltakLortu(entrenamendua.id)

        inprimatzekoDatuak = []

        #Aukeratutako datuak inprimatzeko lortu
        i = 0
        while (i < len(datuak)):
            lerroa = []
            b = datuak[i]
            if ("Izena" in aukeratutakoGoiburuak):
                lerroa.append(b.izena)
            if ("Mugimendu Denbora" in aukeratutakoGoiburuak):
                lerroa.append(b.mugimenduDenb)
            if ("Distantzia" in aukeratutakoGoiburuak):
                lerroa.append(b.distantzia)
            if ("HasiData" in aukeratutakoGoiburuak):
                lerroa.append(b.hasiData)
            if ("Abiadura Max" in aukeratutakoGoiburuak):
                lerroa.append(b.abiaduraMax)
            if ("Batazbesteko abiadura" in aukeratutakoGoiburuak):
                lerroa.append(b.bbAbiadura)
            inprimatzekoDatuak.append(lerroa)
            i = i + 1

        #Datuak TreeView-ean txertatu
        for i, d in enumerate(inprimatzekoDatuak):
            self.bueltaInfo.insert(parent='', index=i, iid=i, values=d)

        #TreeView-a pantailaratu
        self.bueltaInfo.grid(row=0, column=0)

        #TreeView-eko estiloa zehaztu
        s = ttk.Style()
        s.configure("Treeview.Heading", font=('Helvetica', 9))
        s.configure("Treeview", font=('Helvetica', 9))