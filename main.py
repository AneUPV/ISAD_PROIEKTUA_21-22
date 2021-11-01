from controllers.StravaAPI import stravaApiKud


if __name__ == '__main__':
    stravaApiKud.getAccessToTheAPI()
    #1. /athlete
#    print(stravaApiKud.getAthlete())
    #2. /athlete/activities
#    print(stravaApiKud.getActivities())
    #3. /activities/%id
#    print(stravaApiKud.getActivities_id(61350307, False))
    #4. /activities/%id/streams
    print(stravaApiKud.getActivities_id_streams(61350307))
