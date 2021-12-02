from controllers.StravaAPI import stravaApiKud
from controllers.DBKudeatzailea.DBKudeatzailea import DBKudeatzailea
from view.Leihoa import Leihoa

if __name__ == '__main__':

# -------------------------------------------------------------#
#                   API-KO DEIAK                               #
# -------------------------------------------------------------#

    #stravaApiKud.getAccessToTheAPI()

    #1. /athlete
    #stravaApiKud.getAthlete()

    #2. /athlete/activities
    #ema=stravaApiKud.getActivities()
    #id=ema[1]["id"]

    #3. /activities/%id
    #stravaApiKud.getActivities_id(id)

    #4. /activities/%id/streams
    #stravaApiKud.getActivities_id_streams(id)

# -------------------------------------------------------------#
#                   DEI LAGUNGARRIAK                           #
# -------------------------------------------------------------#

    #dbk=DBKudeatzailea()

    #DB-ko taulak sortu
    #dbk.taulakSortu()

    #Stravako API-tik datuak atera eta DB-an sartu
    #dbk.datuakKargatu()

# -------------------------------------------------------------#
#                   LEHIOAREN DEIA                             #
# -------------------------------------------------------------#

    Leihoa()



