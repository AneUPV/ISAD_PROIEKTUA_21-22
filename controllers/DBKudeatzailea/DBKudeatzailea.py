import mysql.connector

class DBKudeatzailea:
    def __init__(self):
        self.db = mysql.connector.connect(
            host="localhost",
            user="strava",
            password="strava123#",
            database="strava"
        )
        self.kurtsorea = self.db.cursor()

    def erakutsiDB(self):
        self.kurtsorea.execute("SHOW DATABASES;")
        row=True
        try:
            while row:
                row = self.kurtsorea.fetchone()
                print(row)
        except StopIteration:
             print("Ez daude emaitza gehiagorik")

    def taulakSortu(self):

        #Entrenamendu taula sortu (existitzen ez bada)
        self.kurtsorea.execute("""CREATE TABLE `strava`.`tmp` (
  `idtmp` INT NOT NULL,
  PRIMARY KEY (`idtmp`));""")
        self.db.commit()


