import unittest
import logging
#log to stdout
#logging.basicConfig(level=logging.DEBUG)

from beckett_parser import parseBeckettTableRow
from utilities import hasHigherProportionOfLowerCaseCharacters, isProbablyAName, hasNumbersInString
from tutorial.items import BeckettItem

class BeckettParserTests(unittest.TestCase):

    def assertNoErrorInformation(self, item):
        try:
            item['errorInformation']
            self.assertTrue(False, "There should not be any error information")
        except: KeyError

    def assertNoSubsetName(self, item):
        try:
            item['subsetName']
            self.assertTrue(False, "There should not be any subset info")
        except: KeyError

    def assertSubsetName(self, item, expectedSubsetName):
        try:
            self.assertEqual(expectedSubsetName, item['subsetName'], "The subset name was not extracted correctly")
        except:
            self.assertTrue(False, "The subset name is valid and should not throw an exception")

    def assertErrorInformation(self, item, expectedErrorInformation):
        try:
            self.assertEqual(expectedErrorInformation, item['errorInformation'], "The error info was not extracted correctly")
        except:
            self.assertTrue(False, "The error info was valid and should not throw an exception")


    def assertExpectedValues(self, description, year, setName, cardNumber, playerNames):
        item = parseBeckettTableRow(description, logging)

        self.assertEqual(year, item['year'], "The year is not as expected")
        self.assertEqual(setName, item['setName'], "The set name is not as expected")
        self.assertEqual(cardNumber, item['cardNumber'], "The card number is not as expected")
        self.assertEqual(len(playerNames), len(item['playerNames']), "The number of players found is not equal.\nExpected Length: ")

        for i in range(0, len(playerNames)):
            self.assertEqual(playerNames[i], item['playerNames'][i], "The name as position: " + str(i) + " does not match. Expected: " + playerNames[i] + " Actual: " + item['playerNames'][i])

        return item

    def test_parser_printing_plates(self):
        expectedPlayerNames = ["David Wesley Black"]

        item = self.assertExpectedValues("1997-98 Stadium Club Printing Plates #204 David Wesley TRAN Black", "1997-98", "Stadium Club Printing Plates", "#204", expectedPlayerNames)

        self.assertNoErrorInformation(item)
        self.assertNoSubsetName(item)

    def test_parser_removes_unwanted_abbreviations(self):
        expectedPlayerNames = ["LeBron James"]

        item = self.assertExpectedValues("2003-04 Exquisite Collection #78 LeBron James JSY AU RC", "2003-04", "Exquisite Collection", "#78", expectedPlayerNames)

        self.assertNoErrorInformation(item)
        self.assertNoSubsetName(item)

    def test_parser_mutliple_names(self):
        expectedPlayerNames = ["Dynasty", "Michael Jordan", "Scottie Pippen", "Dennis Rodman"]

        item = self.assertExpectedValues("1996-97 UDA Chicago Bulls Commemorative Cards #NNO 1997 90s Dynasty/15000/Michael Jordan/Scottie Pippen/Dennis Rodman", "1996-97", "UDA Chicago Bulls Commemorative Cards", "#NNO", expectedPlayerNames)

        self.assertNoErrorInformation(item)
        self.assertNoSubsetName(item)


    def test_parser_griffey(self):
        expectedPlayerNames = ["Ken Griffey Jr."]

        item = self.assertExpectedValues("1999 Metal Universe Precious Metal Gems #273 Ken Griffey Jr. MLPD", "1999", "Metal Universe Precious Metal Gems", "#273", expectedPlayerNames)
        self.assertSubsetName(item, "MLPD")
        self.assertNoErrorInformation(item)

    def test_parser_errorcard_with_AU(self):
        expectedPlayerNames = ["Jordan Zimmerman"]

        item = self.assertExpectedValues("2008 Bowman Chrome Prospects Blue Refractors #BCP254 Jordan Zimmerman AU UER/Last name misspelled", "2008", "Bowman Chrome Prospects Blue Refractors", "#BCP254", expectedPlayerNames)
        self.assertNoSubsetName(item)
        self.assertErrorInformation(item, "/Last name misspelled")

    def test_parser_errorcard_with_subset(self):
        expectedPlayerNames = ["Arvydas Sabonis"]

        item = self.assertExpectedValues("1998-99 UD Choice Premium Choice Reserve #177 Arvydas Sabonis FS UER/spelled Arvadas", "1998-99", "UD Choice Premium Choice Reserve", "#177", expectedPlayerNames)
        self.assertSubsetName(item, "FS")
        self.assertErrorInformation(item, "/spelled Arvadas")




suite = unittest.TestLoader().loadTestsFromTestCase(BeckettParserTests)
unittest.TextTestRunner(verbosity=2).run(suite)