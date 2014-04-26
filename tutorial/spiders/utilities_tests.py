import unittest


from utilities import hasHigherProportionOfLowerCaseCharacters, isProbablyAName, hasNumbersInString, getSearchUrl

class UtilitiesTests(unittest.TestCase):

    def test_getSearchUrl(self):
        self.assertEqual("http://www.beckett.com/search/?year_start=1997&attr=24470&team=345678&rowNum=10000", getSearchUrl("34567", "1997"))

suite = unittest.TestLoader().loadTestsFromTestCase(UtilitiesTests)
unittest.TextTestRunner(verbosity=2).run(suite)