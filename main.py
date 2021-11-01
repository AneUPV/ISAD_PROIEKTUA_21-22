from controllers.StravaAPI import stravaApiKud


if __name__ == '__main__':
    stravaApiKud.getAccessToTheAPI()
    #print(stravaApiKud.getAthlete())
    em = stravaApiKud.getActivities()
    print(stravaApiKud.getActivities_id(em[0]["id"]))
