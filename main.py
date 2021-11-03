from controllers.StravaAPI import stravaApiKud

if __name__ == '__main__':

#61350307

    stravaApiKud.getAccessToTheAPI()
    #1. /athlete
#   print(stravaApiKud.getAthlete())
    #2. /athlete/activities
#    print(stravaApiKud.getActivities())
    ema=stravaApiKud.getActivities()
    id=ema[1]["id"]
    #3. /activities/%id
    print("3.ARIKETA")
    print(stravaApiKud.getActivities_id(id).keys())
    #4. /activities/%id/streams                                        #type eta data gorde
    print("4.ARIKETA")
    print(stravaApiKud.getActivities_id_streams(id).keys())

