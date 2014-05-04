__author__ = 'Tom'

import re
from beckett_teams import getTeamNameFromID

#generate a search url for a team and particular year. We do this to divide up the searches to better insure we have less than 10000 hits
#beckett seems to cap results at 10000. we also hard search for only the serial card attribute, we don't care about other stuff which can't be used to identify individual cards
def generateSearchUrl(teamId, year, sport):
    serialAttribute = '24470'# serial card attributes
    numberOfRows = '10000' #want 10000 the max search results for beckett
    formattedUrl = "http://www.beckett.com/search/?year_start={year}&attr={attribute}&team={team}&sport={sport}&rowNum={numberOfRows}".format(year=year, attribute=serialAttribute, team=teamId, sport=sport, numberOfRows=numberOfRows)
    return formattedUrl

def getSearchItemFromURL(theUrl, attribute):
    regEx = re.compile(r''+attribute+"=(.*?)&")
    found = regEx.search(theUrl)

    if found:
        #we found an occurance, we need to trim the ampersand adn the attirbute search value before continuing
        foundString = found.group()
        foundString = foundString.replace(attribute+"=", "").strip()
        foundString = foundString.replace("&", "").strip()
        return foundString
    else:
        return ""

def getYearInURL(theUrl):
    return getSearchItemFromURL(theUrl, "year_start")

def getTeamInURL(theUrl):
    teamID = getSearchItemFromURL(theUrl, "team")
    return getTeamNameFromID(teamID)

def hasHigherProportionOfLowerCaseCharacters(inputString):

    if len(inputString) < 1:
        return False

    upperCaseCount = 0.0;

    for char in inputString:
        if char.isupper():
            upperCaseCount += 1.0
        if not char.isalnum(): #reduce the upper case count if we have a . or a - which can be used in shorted names (eg O.J.)
            upperCaseCount -= 1.0

    return (upperCaseCount / len(inputString)) <= 0.50


def isProbablyAName(inputString):
    return hasHigherProportionOfLowerCaseCharacters(inputString) and not hasNumbersInString(inputString)

def hasNumbersInString(inputString):
    return any(char.isdigit() for char in inputString)

def levenshtein(seq1, seq2):
    oneago = None
    thisrow = range(1, len(seq2) + 1) + [0]
    for x in xrange(len(seq1)):
        twoago, oneago, thisrow = oneago, thisrow, [0] * len(seq2) + [x + 1]
        for y in xrange(len(seq2)):
            delcost = oneago[y] + 1
            addcost = thisrow[y - 1] + 1
            subcost = oneago[y - 1] + (seq1[x] != seq2[y])
            thisrow[y] = min(delcost, addcost, subcost)
    return thisrow[len(seq2) - 1]