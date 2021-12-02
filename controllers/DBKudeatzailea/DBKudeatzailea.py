import mysql.connector
from controllers.StravaAPI import stravaApiKud
import unicodedata

from model.Bueltak import Bueltak
from model.Ekipamendua import Ekipamendua
from model.Entrenamendua import Entrenamendua


class DBKudeatzailea:

    def __init__(self):
        #DB-arekin konexioa ezarri
        self.db = mysql.connector.connect(
            host="localhost",
            user="strava",
            password="strava123#",
            database="strava"
        )
        #Kontsultak egiteko kurtsorea
        self.kurtsorea = self.db.cursor()

    # -------------------------------------------------------------#
    #                   FUNTZIOAK                                  #
    # -------------------------------------------------------------#

    #Datu base guztiak erakusteko metodoa
    def erakutsiDB(self):
        self.kurtsorea.execute("SHOW DATABASES;")
        row=True
        try:
            while row:
                row = self.kurtsorea.fetchone()
                print(row)
        except StopIteration:
             print("Ez daude emaitza gehiagorik")

    # -------------------------------------------------------------#

    #Strava DB-ko taula guztiak sortuko dituen metodoa
    def taulakSortu(self):

        #Entrenamendu taula sortu (existitzen ez bada)
        self.kurtsorea.execute("""CREATE TABLE IF NOT EXISTS `strava`.`entrenamendua` (
                                `id` VARCHAR(45) NOT NULL,
                                `izena` VARCHAR(45) NULL,
                                `mugimenduDenb` INT NULL,
                                `mota` VARCHAR(45) NULL,
                                `noiz` TIMESTAMP NULL,
                                `abiaduraMax` FLOAT NULL,
                                `bbAbiadura` FLOAT NULL,
                                `distantzia` FLOAT NULL,
                                `erreKaloria` FLOAT NULL,
                                `mapa` TEXT NULL,
                                PRIMARY KEY (`id`))
                                DEFAULT CHARACTER SET = utf8mb4 ;""")
        self.db.commit()

        # Segmentua taula sortu (existitzen ez bada)
        self.kurtsorea.execute("""CREATE TABLE IF NOT EXISTS `strava`.`segmentua` (
                                  `id` VARCHAR(45) NOT NULL,
                                  `izena` VARCHAR(45) NULL,
                                  `mota` VARCHAR(45) NULL,
                                  `distantzia` FLOAT NULL,
                                  `hiria` VARCHAR(45) NULL,
                                  `estatua` VARCHAR(45) NULL,
                                  `herrialdea` VARCHAR(45) NULL,
                                  PRIMARY KEY (`id`))
                                  DEFAULT CHARACTER SET = utf8mb4;""")
        self.db.commit()

        # Ekipamendua taula sortu (existitzen ez bada)
        self.kurtsorea.execute("""CREATE TABLE IF NOT EXISTS `strava`.`ekipamendua` (
                                  `id` VARCHAR(45) NOT NULL,
                                  `izena` VARCHAR(45) NULL,
                                  PRIMARY KEY (`id`))
                                  DEFAULT CHARACTER SET = utf8mb4;""")
        self.db.commit()

        # Bueltak taula sortu (existitzen ez bada)
        self.kurtsorea.execute("""CREATE TABLE IF NOT EXISTS `strava`.`bueltak` (
                                  `bueltaZenb` VARCHAR(45) NOT NULL,
                                  `entrenaId` VARCHAR(45) NULL,
                                  `izena` VARCHAR(45) NULL,
                                  `mugimenduDenb` INT NULL,
                                  `distantzia` FLOAT NULL,
                                  `hasiData` TIMESTAMP NULL,
                                  `abiaduraMax` FLOAT NULL,
                                  `bbAbiadura` FLOAT NULL,
                                  PRIMARY KEY (`bueltaZenb`),
                                  FOREIGN KEY (`entrenaId`)
                                  REFERENCES `entrenamendua` (`id`)
                                  ON DELETE CASCADE
                                  ON UPDATE CASCADE)
                                  DEFAULT CHARACTER SET = utf8mb4;""")
        self.db.commit()

        # Medizioak taula sortu (existitzen ez bada)
        self.kurtsorea.execute("""CREATE TABLE IF NOT EXISTS `strava`.`medizioak` (
                                 `mota` VARCHAR(45) NOT NULL,
                                 `entrenaId` VARCHAR(45) NOT NULL,
                                 `erresoluzioa` VARCHAR(45) NULL,
                                 `neurketak` TEXT NULL,         
                                 PRIMARY KEY (`mota`,`entrenaId`),
                                 FOREIGN KEY (`entrenaId`)
                                 REFERENCES `entrenamendua` (`id`)
                                 ON DELETE CASCADE
                                 ON UPDATE CASCADE)
                                 DEFAULT CHARACTER SET = utf8mb4;""")
        self.db.commit()

        # Ekipatu taula sortu (existitzen ez bada)
        self.kurtsorea.execute("""CREATE TABLE IF NOT EXISTS `strava`.`ekipatu` (
                                  `ekipamenduId` VARCHAR(45) NOT NULL,
                                  `entrenaId` VARCHAR(45) NOT NULL,
                                   PRIMARY KEY (`ekipamenduId`, `entrenaId`),
                                   FOREIGN KEY (`ekipamenduId`)
                                   REFERENCES `ekipamendua` (`id`)
                                   ON DELETE CASCADE
                                   ON UPDATE CASCADE,
                                   FOREIGN KEY (`entrenaId`)
                                   REFERENCES `entrenamendua` (`id`)
                                   ON DELETE CASCADE
                                   ON UPDATE CASCADE)
                                   DEFAULT CHARACTER SET = utf8mb4;""")
        self.db.commit()

        # Egin taula sortu (existitzen ez bada)
        self.kurtsorea.execute("""CREATE TABLE IF NOT EXISTS `strava`.`egin` (
                                 `entrenaId` VARCHAR(45) NOT NULL,
                                 `segmentuId` VARCHAR(45) NOT NULL,
                                 `denbora` TIMESTAMP NULL,
                                 PRIMARY KEY (`entrenaId`, `segmentuId`),
                                 FOREIGN KEY (`entrenaId`)
                                 REFERENCES `entrenamendua` (`id`)
                                 ON DELETE CASCADE
                                 ON UPDATE CASCADE,
                                 FOREIGN KEY (`segmentuId`)
                                 REFERENCES `segmentua` (`id`)
                                 ON DELETE CASCADE
                                 ON UPDATE CASCADE)
                                 DEFAULT CHARACTER SET = utf8mb4;""")
        self.db.commit()


    # -------------------------------------------------------------#

    #Stravako API-tik datuak hartu eta DB-ra kargatu
    def datuakKargatu(self):

        #Stravako API-ra konektatu
        stravaApiKud.getAccessToTheAPI()

        #Entrenamenduen datuak lortu
        datuak = stravaApiKud.getActivities()
        entrenaLuzera = len(datuak)

        i=0
        while (i<entrenaLuzera) :
            entrenamendua = datuak[i]
            id = entrenamendua["id"]
            izena = entrenamendua["name"]
            mugimenduDenb = entrenamendua["moving_time"]
            mota = entrenamendua["type"]
            noiz = entrenamendua["start_date"]
            abiaduraMax = entrenamendua["max_speed"]
            bbAbiadura = entrenamendua["average_speed"]
            distantzia = entrenamendua["distance"]
            datuak2 = stravaApiKud.getActivities_id(id)
            erreKaloria = datuak2["calories"]

            #Entrenamenduaren mapa bilatu
            if ( "polyline" in  entrenamendua["map"] ):             #"Polyline" bilatu entrenamendua["map"]-en key balioetan
                mapa = entrenamendua["map"]["polyline"]
            elif ("summary_polyline" in entrenamendua["map"] ):     #"Polyline" ez badu, "summary_polyline" bilatu
                mapa = entrenamendua["map"]["summary_polyline"]
            else:                                                   #"Polyline" eta "summary_polyline" ez badago mapa ez dauka, beraz "" balioa jarri
                mapa = ""

            #Jada id horrekin entrenamenduren bat dagoen konprobatu
            self.kurtsorea.execute("SELECT * FROM entrenamendua WHERE id=%s;",(id,))
            emaitza=self.kurtsorea.fetchone()

            if emaitza != None :    #Entrenamendua aurkitzen badu -> UPDATE
                self.kurtsorea.execute("UPDATE entrenamendua SET izena=%s, mugimenduDenb= %s, mota=%s, noiz=%s, abiaduraMax=%s, bbAbiadura=%s, distantzia=%s, erreKaloria=%s, mapa=%s WHERE id=%s;", (izena,mugimenduDenb,mota,noiz,abiaduraMax,bbAbiadura,distantzia,erreKaloria,mapa,id))
                self.db.commit()

            else:                   #Entrenamendua aurkitzen EZ badu -> INSERT
                self.kurtsorea.execute("INSERT IGNORE INTO entrenamendua VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s );",(id,izena,mugimenduDenb,mota,noiz,abiaduraMax,bbAbiadura,distantzia,erreKaloria,mapa))
                self.db.commit()

            #Segmentuen eta egin taulen datuak kargatu
            self.segmentuaBete(datuak2,mota)

            #Bueltak taulen datuak kargatu
            self.bueltakBete(datuak2)

            #Ekipamendua eta ekipatu taulen datuak kargatu
            self.ekipamenduaBete(datuak2)

            datuak3 = stravaApiKud.getActivities_id_streams(id)
            self.medizioakBete(datuak3,id)

            i=i+1

    # -------------------------------------------------------------#

    #Segmentua eta egin taulak betetzen dituen funtzioa
    def segmentuaBete(self,entrenamendua,mota):
        segmentulista = entrenamendua["segment_efforts"]
        segLuzera = len(segmentulista)

        j=0
        while(j<segLuzera) :
            segmentua = segmentulista[j]["segment"]
            segid=segmentua["id"]
            segizena=segmentua["name"]
            segKM=segmentua["distance"]
            segHiri=segmentua["city"]
            segEstatu=segmentua["state"]
            segHerrialdea=segmentua["country"]
            segHasiData=segmentulista[j]["start_date"]

            #Frantziako hiri batek ' bat dauka hiriko izenean, if honekin ' hori ezabatuko da
            if (segHiri != None):
                segHiri= segHiri.replace("'"," ")

            #Jada id hori duen segmenturen bat dagoen konprobatu
            self.kurtsorea.execute("SELECT * FROM segmentua WHERE id=%s;", (segid,))
            emaitza = self.kurtsorea.fetchone()

            if emaitza != None:         #Aurkitu badu -> UPDATE
                self.kurtsorea.execute("UPDATE segmentua SET izena=%s,mota=%s,distantzia=%s,hiria=%s,estatua=%s,herrialdea=%s WHERE id=%s;", (segizena,mota,segKM,segHiri,segEstatu,segHerrialdea,segid))
                self.kurtsorea.execute("UPDATE egin SET denbora=%s WHERE entrenaId=%s AND segmentuId=%s;", (segHasiData,entrenamendua["id"],segid))
                self.db.commit()

            else:                       #Aurkitu EZ badu -> INSERT
                self.kurtsorea.execute("INSERT IGNORE INTO segmentua VALUES (%s,%s,%s,%s,%s,%s,%s);", (segid,segizena,mota,segKM,segHiri,segEstatu,segHerrialdea))
                self.kurtsorea.execute("INSERT IGNORE INTO egin VALUES (%s,%s,%s);", (entrenamendua["id"],segid,segHasiData))
                self.db.commit()
            j=j+1

    # -------------------------------------------------------------#

    #Bueltak taula kargatu
    def bueltakBete(self, entrenamendua):
        entrenaId = entrenamendua["id"]
        bueltak= entrenamendua["laps"]
        bueltaluzera=len(bueltak)

        k=0
        while(k<bueltaluzera):
            unekoBuelta=bueltak[k]
            bueltaid=unekoBuelta["id"]
            bueltaIzena=unekoBuelta["name"]
            bueltaMugDenb= unekoBuelta["moving_time"]
            bueltaEginKM=unekoBuelta["distance"]
            bueltaHasiData=unekoBuelta["start_date"]
            bueltaAbiadMax=unekoBuelta["max_speed"]
            bueltaBBAbiad=unekoBuelta["average_speed"]

            # Jada bueltaId hori daukan bueltak existitzen den konprobatu
            self.kurtsorea.execute("SELECT * FROM bueltak WHERE bueltaZenb=%s;", (bueltaid,))
            emaitza = self.kurtsorea.fetchone()

            if emaitza != None:     #Aurkitzen badu -> UPDATE
                self.kurtsorea.execute("UPDATE bueltak SET entrenaId=%s, izena=%s, mugimenduDenb=%s, distantzia=%s, hasiData=%s, abiaduraMax=%s, bbAbiadura=%s WHERE bueltaZenb=%s;", (entrenaId,bueltaIzena,bueltaMugDenb,bueltaEginKM,bueltaHasiData,bueltaAbiadMax,bueltaBBAbiad,bueltaid))
                self.db.commit()

            else:                   #Aurkitzen EZ badu -> INSERT
                self.kurtsorea.execute("INSERT IGNORE INTO bueltak VALUES (%s,%s,%s,%s,%s,%s,%s,%s);", (bueltaid,entrenaId,bueltaIzena,bueltaMugDenb,bueltaEginKM,bueltaHasiData,bueltaAbiadMax,bueltaBBAbiad))
                self.db.commit()
            k = k + 1

    # -------------------------------------------------------------#

    #Medizioak taula kargatu
    def medizioakBete(self, datuak, entrenaId):

        #Entrenamendu bakoitza dituen neurketa mota begiratu
        for l in datuak.keys():
            if (l == "time"):                       #Denbora
                mota = datuak["time"]
            if (l == "latlng"):                     #Latitudea/Longitudea
                mota = datuak["latlng"]
            if (l == "distance"):                   #Distantzia
                mota = datuak["distance"]
            if (l == "altitude"):                   #Altitudea
                mota = datuak["altitude"]
            if (l == "velocity_smooth"):            #Abiadura leunduta
                mota = datuak["velocity_smooth"]
            if (l == "heartrate"):                  #Pultsazioak
                mota = datuak["heartrate"]
            if (l == "cadence"):                    #Kadentzia
                mota = datuak["cadence"]
            if (l == "watts"):                      #Watt
                mota = datuak["watts"]
            if (l == "temp"):                       #Temperatura
                mota = datuak["temp"]
            if (l == "moving"):                     #Mugimendua (True/False)
                mota = datuak["moving"]
            if (l == "grade_smooth"):               #Aldapa leunduta
                mota = datuak["grade_smooth"]

            izena = l
            neurketak = mota["data"]
            erresoluzioa = mota["resolution"]

            #Jada id hori duen entrenamendua mota horretako neurketa duen begiratu
            self.kurtsorea.execute("SELECT * FROM medizioak WHERE entrenaId=%s AND mota = %s;", (entrenaId,izena))
            emaitza = self.kurtsorea.fetchone()

            if emaitza != None:             #Aurkitu badu -> UPDATE
                self.kurtsorea.execute("UPDATE medizioak SET erresoluzioa=%s, neurketak = '"+str(neurketak)+"' WHERE entrenaId=%s AND mota = %s;", (erresoluzioa,entrenaId,izena))
                self.db.commit()
            else:                           #Aurkitu EZ badu -> INSERT
                self.kurtsorea.execute("INSERT IGNORE INTO medizioak VALUES (%s,%s,%s,'"+str(neurketak)+"');", (izena,entrenaId,erresoluzioa))
                self.db.commit()

    # -------------------------------------------------------------#

    #Ekipatu eta Ekipamendua taulak kargatu
    def ekipamenduaBete(self, entrenamendua):
        if entrenamendua["gear_id"]!=None:
            ekipatu = entrenamendua["gear"]
            ekipId = ekipatu["id"]
            ekipIzena = ekipatu["name"]

            #Jada id hori duen ekipamendua dagoen konprobatu
            self.kurtsorea.execute("SELECT * FROM ekipamendua WHERE id=%s;", (ekipId,))
            emaitza = self.kurtsorea.fetchone()

            if emaitza != None:         #Aurkitzen badu -> UPDATE
                self.kurtsorea.execute("UPDATE ekipamendua SET izena=%s WHERE id=%s;", (ekipIzena,ekipId))
                self.db.commit()
            else:                       #Aurkitzen EZ badu -> INSERT
                self.kurtsorea.execute("INSERT IGNORE INTO ekipamendua VALUES (%s,%s);", (ekipId,ekipIzena))
                self.kurtsorea.execute("INSERT IGNORE INTO ekipatu VALUES (%s,%s);", (ekipId,entrenamendua["id"]))
                self.db.commit()

    # -------------------------------------------------------------#

    #Entrenamenduak erakusteko funtzioa
    def entrenamenduakErakutsi(self):
        self.kurtsorea.execute("SELECT izena, noiz, mugimenduDenb, mota FROM entrenamendua;")
        return self.kurtsorea.fetchall()

    # -------------------------------------------------------------#

    #Motak erakutsi funtzioa
    def motakLortu(self):
        self.kurtsorea.execute("SELECT DISTINCT mota FROM entrenamendua;")
        return self.kurtsorea.fetchall()

    # -------------------------------------------------------------#

    #Bilaketa erakutsi funtzioa
    def bilaketaErakutsi(self,noiztik,nora,mota):

        if len(noiztik)>0:
            if len(nora)>0:
                if mota!="Guztiak":         #Noiztik, nora eta mota (Guztira ez) beteta
                    self.kurtsorea.execute("SELECT * FROM entrenamendua WHERE noiz >= %s AND noiz <= %s AND mota = %s ORDER BY noiz DESC;", (noiztik,nora,mota))
                else:                       #Noiztik, nora eta mota (Guztira bai) beteta
                    self.kurtsorea.execute("SELECT * FROM entrenamendua WHERE noiz >= %s AND noiz <= %s ORDER BY noiz DESC;", (noiztik,nora))
            else:
                if mota!="Guztiak":         #Noiztik eta mota (Guztira ez) beteta
                    self.kurtsorea.execute("SELECT * FROM entrenamendua WHERE noiz >= %s AND mota = %s ORDER BY noiz DESC;", (noiztik,mota))
                else:                       #Noiztik eta mota (Guztira bai) beteta
                    self.kurtsorea.execute("SELECT * FROM entrenamendua WHERE noiz >= %s ORDER BY noiz DESC;", (noiztik,))
        else:
            if len(nora)>0:                 #Nora eta mota (Guztira ez) beteta
                if mota!="Guztiak":
                    self.kurtsorea.execute("SELECT * FROM entrenamendua WHERE noiz <= %s AND mota = %s ORDER BY noiz DESC;", (nora,mota))
                else:                       #Nora eta mota (Guztira bai) beteta
                    self.kurtsorea.execute("SELECT * FROM entrenamendua WHERE noiz <= %s ORDER BY noiz DESC;", (nora,))
            else:
                if mota != "Guztiak":       #Mota (Guztira ez) beteta
                    self.kurtsorea.execute("SELECT * FROM entrenamendua WHERE mota = %s ORDER BY noiz DESC;", (mota,))
                else:                       #Mota (Guztira bai) beteta
                    self.kurtsorea.execute("SELECT * FROM entrenamendua ORDER BY noiz DESC;")
        ema = self.kurtsorea.fetchall()

        #Entrenamendua klaseak sortu
        e = 0
        entrenaLista = []
        while e < len(ema):
            id=ema[e][0]
            izena=ema[e][1]
            mugimenduDenb=ema[e][2]
            mota=ema[e][3]
            noiz=ema[e][4]
            abiaduraMax=ema[e][5]
            bbAbiadura=ema[e][6]
            distantzia=ema[e][7]
            erreKaloria=ema[e][8]
            mapa=ema[e][9]

            #Entrenamendu klaseak sortu eta entrenaLista array-an sartu
            entrenaLista.append(Entrenamendua(id,izena,mugimenduDenb,mota,noiz,abiaduraMax,bbAbiadura,distantzia,erreKaloria, mapa))
            e=e+1

        return entrenaLista

    # -------------------------------------------------------------#

    #Medizio desberdinak lortzeko metodoa
    def neurketaMotakLortu(self):
        self.kurtsorea.execute("SELECT DISTINCT mota FROM medizioak;")
        return self.kurtsorea.fetchall()

    # -------------------------------------------------------------#

    #Entrenamendu konkretu baten bueltak lortu
    def bueltakLortu(self, entrenaId):
        self.kurtsorea.execute("SELECT * FROM bueltak WHERE entrenaId= %s;", (entrenaId,))
        ema = self.kurtsorea.fetchall()
        bueltakLista=[]

        i=0
        while i< len(ema) :
            bueltaZenb=ema[i][0]
            entrenaId=ema[i][1]
            izena=ema[i][2]
            mugimenduDenb=ema[i][3]
            distantzia=ema[i][4]
            hasiData=ema[i][5]
            abiaduraMax=ema[i][6]
            bbAbiadura=ema[i][7]

            #Buelta klasea sortu eta bueltakLista array-an sartu
            bueltakLista.append(Bueltak(bueltaZenb, entrenaId, izena, mugimenduDenb, distantzia, hasiData, abiaduraMax, bbAbiadura))
            i=i+1

        return bueltakLista

    # -------------------------------------------------------------#

    #Ekipamendua eta honekin egindako kilometro kopurua kalkulatu
    def ekipamenduakSortu(self):
        self.kurtsorea.execute("SELECT EK.izena, SUM(EN.distantzia) as guztira FROM ENTRENAMENDUA EN, EKIPAMENDUA EK, EKIPATU E WHERE EN.id=E.entrenaId AND E.ekipamenduId=EK.id GROUP BY EK.izena;")
        ema = self.kurtsorea.fetchall()
        ekipamenduLista=[]

        e=0
        while (e< len(ema)):
            izena=ema[e][0]
            guztira=ema[e][1]

            #Ekipamendu klasea sortu eta ekipamenduLista array-an sartu
            ekipamenduLista.append(Ekipamendua(izena, guztira))
            e=e+1

        return ekipamenduLista

    # -------------------------------------------------------------#

     #Entrenamendu zehatz bateko eta mota konkretu bateko datuak lortu
    def neurketakLortu(self, irizpidea, id):
        self.kurtsorea.execute("SELECT neurketak FROM MEDIZIOAK WHERE entrenaId=%s AND mota=%s;", (id, irizpidea))
        ema=self.kurtsorea.fetchone()

        #Balioak string moduan hartzen ditugu eta array bihurtu behar da
        if ( ema == None or ema == "None" ):
            zer=[]
        else:
            balioak = ema[0]
            zer = balioak[1:len(balioak) - 1].split(', ')
            for i in range(len(zer)):

                # Moving grafikoak boolean balioak ditu eta 0 eta 1 moduan gordeko dira
                if (zer[i] == "True"):
                    zer[i] = 1
                if (zer[i] == "False"):
                    zer[i] = 0
                zer[i] = float(zer[i])

        return zer