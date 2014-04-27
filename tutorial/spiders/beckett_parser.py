__author__ = 'Tom'

#import all from utilities module
from utilities import hasHigherProportionOfLowerCaseCharacters, isProbablyAName, hasNumbersInString
from tutorial.items import BeckettItem
import logging
import re
from difflib import get_close_matches# for fuzzy logic matching

probablyGoodPlayersNames = []

def processFullPlayerNames(fullName):

    processedPlayerName = ""
    lengthOfName = len(fullName)
    unprocessedName = ''.join(fullName).strip()

    closeMatch = []

    if unprocessedName in probablyGoodPlayersNames:
        logging.info("matched name directly: " + unprocessedName)
        return unprocessedName

    processedPlayerName = ''.join(fullName).strip()
    closeMatch = get_close_matches(processedPlayerName, probablyGoodPlayersNames, 1, 0.9) # this check is a bit more strict for matching a nmae outright
    if len(closeMatch) == lengthOfName:
        logging.warn("matched whole name adequetely " + ''.join(closeMatch))

    elif lengthOfName > 0:
        startIndex = 0
        offset = 1

        logging.info("Starting name check")

        while startIndex is not lengthOfName and len(closeMatch) < 1:
            nameToCheck = fullName[startIndex:startIndex+offset]
            logging.info("Checking name: " + ''.join(nameToCheck))

            closeMatch = get_close_matches(''.join(nameToCheck), probablyGoodPlayersNames, 1, 0.8)
            if len(closeMatch) < 1:
                logging.info("not found updating offset")
                offset += 1
                if startIndex + offset > lengthOfName:
                    logging.info("still not found moving start index")
                    startIndex += 1
                    offset = 1
            else:
                logging.warn("Fuzzy logic found a match as: " + ''.join(closeMatch) +" - for original names " +''.join(fullName))

    if len(closeMatch) > 0:
        return ''.join(closeMatch).strip()
    else:
        logging.info("Couldn't find a match for name leaving unprocessed " + unprocessedName)
        probablyGoodPlayersNames.append(processedPlayerName)
        return unprocessedName


def removeAbbreviations(itemDescription, abbreviation, logging) :

    if(itemDescription.count('#') > 0):
        logging.warn("We should not be removing the abbreviations if there is still a has in the description representing the card number")

    abbreviationCount = itemDescription.count(abbreviation)

    if abbreviationCount == 1:
        itemDescription = itemDescription.replace(abbreviation, "").strip()
        logging.info("Removing abbreviation " + abbreviation)
    if abbreviationCount > 1:
        logging.warn("We have a high number of instances of the abbreviation: " + abbreviation)

    return itemDescription;

def parseBeckettTableRow(itemDescription, logging):

    item = BeckettItem()

    if len(itemDescription) < 2:
       logging.warn("this item was not long enough and is missing info: " + itemDescription)
       return

    item['originalItemDescription'] = itemDescription

    """Cutting off the year of the product"""

    yearRegEx = re.compile(r'^([\w\-]+)')
    year = yearRegEx.search(itemDescription)

    if year:
        year = year.group()
        logging.info("Extracted year: " + year);
        item['year'] = year
    else:
        logging.error("We could not determine the year for the item:"+itemDescription)
        return #continue the for loop of elements as this is not enough info to pass

    #now we remove the first instance of the year from the item descrption to make further parsing easier
    itemDescription = itemDescription.replace(str(year), "").strip()
    logging.info("Removed Year from descripition: " + year);

    """ Cutting off the set name from the item"""

    if "#" in itemDescription:
        hashIndexPosition = itemDescription.index('#');
        if hashIndexPosition >= len(itemDescription):
            logging.error("There was no hash in this item to help determine the card number:"+itemDescription)
            return #continue the for loop of elements as this is not enough info to pass
        else:
            #the setname is the first part of the string, without the hash #
            setName = itemDescription[0:hashIndexPosition].strip()
            item['setName'] = setName
            itemDescription = itemDescription.replace(str(setName), "").strip()
            logging.info("Extracted setname: " + setName);
            logging.info("Removed set name from description: " + itemDescription);
    else:
        logging.error("Hash was not in the string, can't determine set name correctly")

    cardNumberRegEx = re.compile(r'^(#\S+)')
    cardNumber = cardNumberRegEx.search(itemDescription)

    if cardNumber:
        cardNumber = cardNumber.group()
        logging.info("Extracted card number:" + cardNumber);
        item['cardNumber'] = cardNumber
    else:
        logging.error("We could not find a card number for this item: "+itemDescription)
        return #continue the for loop of elements as this is not enough info to pass

    #now we remove the card number from the item descrption to make further parsing easier
    itemDescription = itemDescription.replace(str(cardNumber), "").strip()


    itemDescription = removeAbbreviations(itemDescription, "JSY", logging)
    itemDescription = removeAbbreviations(itemDescription, "AU", logging)
    itemDescription = removeAbbreviations(itemDescription, "RC", logging)

    logging.info("Removed common abbreviations, remaining description: "+itemDescription)

    errorCount = itemDescription.count("UER")

    if errorCount > 0:
        errorDescriptions = itemDescription.split("UER")
        if errorCount == 1:
            #the card has error info is on the second one
            errorDescription = errorDescriptions[1]

            #remove the error description code and text from the item description
            itemDescription = itemDescription.replace("UER", "").strip()
            logging.info("Trimmed UER tag:" + itemDescription);
            itemDescription = itemDescription.replace(errorDescription.strip(), "").strip()
            item['errorInformation'] = errorDescription

            logging.info("Extracted error description: " + errorDescription);
            logging.info("Trimmed error description: " + errorDescription);
        else:
            logging.error("We had an unecpexted number of UER error stetes for a card: "+itemDescription)
            return #continue the for loop of elements as this is not enough info to pass

    """ Trim of any subset infor which may exist before doing the player names.
    This would be if the last element in the the remaining item descrpition is all capaital letters"""
    subsetName = itemDescription.split()[-1];

    logging.info("Evaluating subset: " + subsetName);

    if not hasHigherProportionOfLowerCaseCharacters(subsetName):
        # if the subset is not a title it means there is more than one capital
        if(len(subsetName) > 1):
            # the subset should be at least 2 letters
            item['subsetName'] = subsetName
            if(itemDescription.count(subsetName) == 1): # only replace the subset if it turns up once in the string
                itemDescription = itemDescription.replace(subsetName, "").strip()
        else:
            logging.warn("We had a subset of only 1 letter for a subset title, seems dodgy")

    """ Now we take a best guess of player names by splitting the remaining string with the /
    character and then checking if the name doesn't have numbers in it"""

    playerNameList = itemDescription.split('/');
    processedPlayersNames = []

    for playerName in playerNameList:
        potentialNames = playerName.split() #now split each potential name in white space
        fullName = []
        for name in potentialNames:
            #if the name is not a number and is in titel format we'll use it
            if isProbablyAName(name):
                fullName.append(name+" ")
                logging.info("Appending name: " + name);
            else:
                logging.warn("Disregarding name: " + name)

        if len(fullName) > 0:
            fullPlayerName = processFullPlayerNames(fullName)
            logging.info("Full player name: " + fullPlayerName);
            processedPlayersNames.append(fullPlayerName)

    item['playerNames'] = processedPlayersNames

    return item;