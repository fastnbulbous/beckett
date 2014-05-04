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

soccerTeamIDs = {463621:'Celtic Football Club' }

basketBallTeamIDs = {344614:'Boston Celtics', \
344618:'Chicago Bulls', 344641:'New Jersey Nets', \
344668:'Los Angeles Lakers', 344646:'Philadelphia 76ers',\
344671:'Toronto Raptors', 344664:'Utah Jazz', 344643:'New York Knicks',\
344626:'Detroit Pistons', 344612:'Atlanta Hawks', 344652:'San Antonio Spurs' ,\
344630:'Houston Rockets' ,\
344637:'Miami Heat' ,\
344621:'Cleveland Cavaliers',\
344618:'Chicago Bulls',\
344623:'Dallas Mavericks',\
475125:'Oklahoma City Thunder',\
344672:'Los Angeles Clippers' ,\
344650:'Portland Trail Blazers',\
344629:'Golden State Warriors',\
344648:'Phoenix Suns',\
344638:'Milwaukee Bucks',\
344624:'Denver Nuggets',\
344667:'Washington Wizards',\
344664:'Utah Jazz',\
344640:'Minnesota Timberwolves',\
344645:'Orlando Magic',\
344651:'Sacramento Kings',\
344631:'Indiana Pacers',\
370514:'Charlotte Bobcats',\
344658:'Seattle Supersonics',\
344641:'New Jersey Nets',\
344669:'Charlotte Hornets',\
344666:'Washington Bullets',\
344673:'New Orleans Hornets',\
344642:'New Orleans Jazz',\
344660:'St. Louis Hawks',\
446568:'Harlem Globetrotters'}

allTeamIDs = []
allTeamIDs.append(basketBallTeamIDs)
allTeamIDs.append(soccerTeamIDs)

def getTeamNameFromID(teamId):
    id = int(teamId)

    for values in allTeamIDs:
        if id in values.keys():
            return values.get(id)
            break

    return "Could not find id: " + teamId

