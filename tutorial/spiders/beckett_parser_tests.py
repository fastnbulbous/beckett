
import random
import unittest
import logging
#log to stdout
#logging.basicConfig(level=logging.DEBUG)

from beckett_parser import parseBeckettTableRow
from utilities import hasHigherProportionOfLowerCaseCharacters, isProbablyAName, hasNumbersInString
from tutorial.items import BeckettItem

class TestSequenceFunctions(unittest.TestCase):

    def assertExpectedValues(self, description, year, setName, cardNumber, playerNames):
        item = parseBeckettTableRow(description, logging)

        self.assertEqual(year, item['year'], "The year is not as expected")
        self.assertEqual(setName, item['setName'], "The set name is not as expected")
        self.assertEqual(cardNumber, item['cardNumber'], "The card number is not as expected")
        self.assertEqual(len(playerNames), len(item['playerNames']), "The number of players found is not equal.\nExpected Length: ")

        for i in range(0, len(playerNames)):
            self.assertEqual(playerNames[i], item['playerNames'][i], "The name as position: " + str(i) + " does not match. Expected: " + playerNames[i] + " Actual: " + item['playerNames'][i])


    def test_parser_printing_plates(self):
        expectedPlayerNames = ["David Wesley Black"]

        self.assertExpectedValues("1997-98 Stadium Club Printing Plates #204 David Wesley TRAN Black", "1997-98", "Stadium Club Printing Plates", "#204", expectedPlayerNames)

        try:
            item['errorInformation']
            self.assertTrue(False, "There should not be any error information")
        except: KeyError

    def test_parser_removes_unwanted_abbreviations(self):
        expectedPlayerNames = ["LeBron James"]

        self.assertExpectedValues("2003-04 Exquisite Collection #78 LeBron James JSY AU RC", "2003-04", "Exquisite Collection", "#78", expectedPlayerNames)

        try:
            item['errorInformation']
            self.assertTrue(False, "There should not be any error information")
        except: KeyError

suite = unittest.TestLoader().loadTestsFromTestCase(TestSequenceFunctions)
unittest.TextTestRunner(verbosity=2).run(suite)