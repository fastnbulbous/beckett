__author__ = 'Tom'



sportIDs = { 185223:'Baseball',\
             185224:'Football',\
             185226:'Basketball',\
             185225:'Hockey',\
             186450:'Racing',\
             468286:'Non-sports',\
             364955:'Tennis',\
             364956:'Wrestling',\
             485146:'MiscSports',\
             367307:'Multisport',\
             367265:'Boxing',\
             475770:'MMA',\
             364957:'Soccer' }

inverseSportIDs = dict((v,k) for k, v in sportIDs.iteritems())

basketBallTeamIDs = {344614:'Boston Celtics', \
344618:'Chicago Bulls', 344641:'New Jersey Nets', \
344668:'Los Angeles Lakers', 344646:'Philadelphia 76ers',\
344671:'Toronto Raptors', 344664:'Utah Jazz', 344643:'New York Knicks',\
344626:'Detroit Pistons', 344612:'Atlanta Hawks'}

allTeamIDs = []
allTeamIDs.append(basketBallTeamIDs)

def getTeamNameFromID(teamId):
    id = int(teamId)

    for values in allTeamIDs:
        if id in values.keys():
            return values.get(id)
            break

    return "Could not find id: " + teamId