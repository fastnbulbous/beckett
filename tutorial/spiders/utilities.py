__author__ = 'Tom'

def getSearchUrl(teamId, year):
    serialAttribute = '24470'# serial card attributes
    numberOfRows = '10000' #want 10000 the max search results for beckett
    formattedUrl = "http://www.beckett.com/search/?year_start={year}&attr={attribute}&team={team}&rowNum={numberOfRows}".format(year=year, attribute=serialAttribute, team=teamId, numberOfRows=numberOfRows)
    return formattedUrl

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