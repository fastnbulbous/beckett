__author__ = 'Tom'

import re #regex searches
import pickle #for serilisation
import json # for dumps
from scrapy.spider import Spider
from scrapy.selector import Selector
from scrapy.selector import HtmlXPathSelector
from tutorial.items import BeckettItem
from scrapy.item import Item, Field

from utilities import generateSearchUrl, getTeamInURL, getYearInURL
from beckett_parser import parseBeckettTableRow
from beckett_teams import basketBallTeamIDs, allTeamIDs, sportIDs, inverseSportIDs

import os
import datetime

import logging
logging.basicConfig(filename='beckett.log',level=logging.WARN)

class BeckettSpider(Spider):
    name = "beckett"
    allowed_domains = ["www.beckett.com"]
    start_urls = [
        #"http://www.beckett.com/search/?year_start=1997&attr=24470&team=344618&sport=185226&rowNum=10000"
        #"http://www.dmoz.org/Computers/Programming/Languages/Python/Resources/"
    ]

    sportName = "Basketball"
    teamName = "None"
    sportID = inverseSportIDs.get(sportName)

    startYear = 1996
    endYear = 1998

    for year in range(startYear, endYear):
        for team in basketBallTeamIDs.iterkeys():
            start_urls.append(generateSearchUrl(team, year, sportID))

    def determineFileName(self, inUrl):
        year=getYearInURL(inUrl)
        self.teamName = getTeamInURL(inUrl)

        directory = os.path.join(os.getcwd(), self.sportName, year);

        if not os.path.exists(directory):
                os.makedirs(directory)

        return  str(os.path.join(directory, self.teamName+".beckett"))

    def parse(self, response):

        filename = self.determineFileName(response.url)
        fileoutput = open(filename, 'w')

        becketItems = []

        selector = Selector(response)
        tableRows = selector.xpath("//table[@id='faceted']//tr")

        logging.info("Starting new parse\n")
        logging.info("URL search: " + response.url)

        fileid =1;

        for tableRow in tableRows:
            logging.info("Parsing Row")

            """ Getting the whole item description, which we need to cut up, it is a text element which contains a hash"""

            #convert list to string from xpath query and clean any white space off the edges, strip
            itemDescription = ''.join(tableRow.xpath('./td/a/text()').re(".*#.*"))

            #cache the raw item description as we are going to be parsing it and splicing it up
            originalItemDescription = itemDescription

            # This will could look something like

            logging.info("Parsing item description: "+originalItemDescription)

            item = parseBeckettTableRow(itemDescription, logging)

            try:
                item['sport'] = str(self.sportName)
            except:
                logging.warn("Could not determine sport name")

            try:
                item['team'] = str(self.teamName)
            except:
                logging.warn("Could not determine team name")

            """Now seeing if there are any attributes for memorbilia, autograph, serial number or rookie card in the same column
                these are done as special divs inside the same column in the element above"""

            testAuto  = tableRow.xpath('./td/div[@class="attr au"]/text()').extract()
            testMemorabilia  = tableRow.xpath('./td/div[@class="attr mem"]/text()').extract()
            testRookieCard  = tableRow.xpath('./td/div[@class="attr rc"]/text()').extract()
            testSerialNumber = tableRow.xpath('./td/div[@class="attr sn"]/text()').extract()

            if len(testAuto) > 0:
                logging.info("Is an Auto")
                item['autograph'] = len(testAuto)
            if len(testMemorabilia) > 0:
                logging.info("Is  memorabilia")
                item['memorabilia'] = len(testMemorabilia)
            if len(testRookieCard)> 0:
                logging.info("Is a RC")
                item['rookieCard'] = len(testRookieCard)
            if len(testSerialNumber)> 0:
                logging.info("Is a serial numbered card")
            else:
                logging.warn("Didn't find a serial tag on this")

            """Try getting the becket info link and web image"""

            #gets image links for each card. all of the, have a width of 50
            # './td/img[@width="50"]/@src' worked but without width it also seems to work fine
            imageLink = tableRow.xpath('./td/img/@src').extract()

            try:
                item['imageLink'] = imageLink
            except:
                # couldn't determine image link
                logging.warn("There is no image link for: "+originalItemDescription)

            #this link is not specifically marked up well, other than the name, year and sport match
            # more simply we just make sure we don't get a href link pointing to the login for the
            # beckett price guide. This leaves us with the real card info link
            beckettLink =  tableRow.xpath('./td/a[not(contains(@href, "login"))]/@href').extract()

            try:
                item['beckettLink'] = beckettLink
            except:
                # couldn't determine image link
                logging.warn("There is no beckett link for: "+originalItemDescription)

            """Getting the serial number which is in a separate column and is listed as a number on becket"""

            testSerialNumber  = ''.join(tableRow.xpath('./td/text()').re("\d+"))

            try:
                serialNumber = int(testSerialNumber)
                item['serialNumber'] = serialNumber
            except:
                 # the serial number is not a number and is empty. mark this item for inverstigation
                logging.warn("There is no serial number listed for this item: "+originalItemDescription)

            fileoutput.write(str(item))
            becketItems.append(item)
            fileid +=1

        pickleFile = filename+".pickle"
        pickleOutput = open(pickleFile, 'wb')
        pickle.dump(becketItems, pickleOutput)
        pickleOutput.close()

        fileoutput.close()
        return becketItems