import unittest
import logging
logging.basicConfig(filename='beckett.log',level=logging.INFO)
#log to stdout
#logging.basicConfig(level=logging.DEBUG)

from beckett_parser import parseBeckettTableRow, probablyGoodPlayersNames, processFullPlayerNames
from utilities import hasHigherProportionOfLowerCaseCharacters, isProbablyAName, hasNumbersInString
from tutorial.items import BeckettItem

class BeckettParserTests(unittest.TestCase):

    def setUp(self):
        probablyGoodPlayersNames = [] # clear this list so it doesn't interfere with other tests

    def tearDown(self):
        del probablyGoodPlayersNames[:]

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
        expectedPlayerNames = ["David Wesley Black"] # we don't have any probable good player names yet, so this will just take what it has current knowledge on

        item = self.assertExpectedValues("1997-98 Stadium Club Printing Plates #204 David Wesley TRAN Black", "1997-98", "Stadium Club Printing Plates", "#204", expectedPlayerNames)

        self.assertNoErrorInformation(item)
        self.assertNoSubsetName(item)

    def test_parser_printing_plates_with_fuzzy_logic_removing_crap(self):
        expectedPlayerNames = ["David Wesley"]

        probablyGoodPlayersNames.append("David Wesley") # if we already have a good entry for this player, we shouldn't get other crap

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


    def test_parser_nfl_shortened_names(self):
        expectedPlayerNames = ["S.Young", "J.Rice"]

        item = self.assertExpectedValues("1999 Playoff Contenders SSD Touchdown Tandems Die Cuts #T22 S.Young/J.Rice/51", "1999", "Playoff Contenders SSD Touchdown Tandems Die Cuts", "#T22", expectedPlayerNames)
        self.assertNoSubsetName(item)
        self.assertNoErrorInformation(item)

    def assertNameWasFoundAsAFuzzyMatch(self, expectedName, testNames):
        probablyGoodPlayersNames.append(expectedName)
        returnedNames = processFullPlayerNames(testNames)
        self.assertEqual(expectedName, returnedNames , "Expected Name: " + expectedName +" - did not match the returned names:" + returnedNames + "- for the test names we passed in " + "".join(testNames))

    def test_guess_spelling_for_Mutombo(self):
        testNames = [['Dikemb2e ', 'Mutumbo '], ['Dikembe ', 'Mutumbo ', 'Cyan '], ['Dikimbe ', 'Mutumbo ']]
        for testName in testNames:
            self.assertNameWasFoundAsAFuzzyMatch("Dikembe Mutombo", testName)

    def test_guess_spelling_for_hardaways(self):
        testNames = [['Tim ', 'Hardaway ', 'Jsy'], ['Tim ', 'Hardaway ', 'Black']]
        for testName in testNames:
            self.assertNameWasFoundAsAFuzzyMatch("Tim Hardaway Jr", testName)

        testNames = [['Tim ', 'Hardaway ', 'RC'], ['Tim ', 'Hardaway ', 'Black ']]
        for testName in testNames:
            self.assertNameWasFoundAsAFuzzyMatch("Tim Hardaway", testName)

suite = unittest.TestLoader().loadTestsFromTestCase(BeckettParserTests)
unittest.TextTestRunner(verbosity=2).run(suite)