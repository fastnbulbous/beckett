__author__ = 'Tom'

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