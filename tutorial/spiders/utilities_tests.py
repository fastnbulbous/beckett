import unittest


from utilities import hasHigherProportionOfLowerCaseCharacters, isProbablyAName, hasNumbersInString, generateSearchUrl, getSearchItemFromURL, getYearInURL, getTeamInURL

class UtilitiesTests(unittest.TestCase):

    def test_getSearchUrl(self):
        self.assertEqual("http://www.beckett.com/search/?year_start=1997&attr=24470&team=345678&sport=185226&rowNum=10000", generateSearchUrl("345678", "1997", "185226"))

    def test_get_year_search_item_using_custom_attribute(self):
        self.assertEqual("1997", getSearchItemFromURL("http://www.beckett.com/search/?year_start=1997&attr=24470&team=345678&rowNum=10000", "year_start"))

    def test_get_year_search_item(self):
        self.assertEqual("1997", getYearInURL("http://www.beckett.com/search/?year_start=1997&attr=24470&team=345678&rowNum=10000"))

    def test_get_team_with_no_existant_team(self):
        self.assertEqual("None", getTeamInURL("http://www.beckett.com/search/?year_start=1997&attr=24470&team=1111345678&rowNum=10000"))

    def test_get_team_with_existing_team(self):
        self.assertEqual("Chicago Bulls", getTeamInURL("http://www.beckett.com/search/?year_start=1997&attr=24470&team=344618&rowNum=10000"))


suite = unittest.TestLoader().loadTestsFromTestCase(UtilitiesTests)
unittest.TextTestRunner(verbosity=2).run(suite)