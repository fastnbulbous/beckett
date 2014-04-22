__author__ = 'Tom'

import re
from scrapy.spider import Spider
from scrapy.selector import Selector
from scrapy.selector import HtmlXPathSelector
from tutorial.items import BeckettItem
from scrapy.item import Item, Field

from beckett_parser import parseBeckettTableRow

import logging
logging.basicConfig(filename='beckett.log',level=logging.INFO)

class BeckettSpider(Spider):
    name = "beckett"
    allowed_domains = ["www.beckett.com"]
    start_urls = [
        "http://www.beckett.com/search/?sport=185226&rowNum=1000&tmm=extended&term=lebron+exquisite+2003&attr=24470"
        #"http://www.dmoz.org/Computers/Programming/Languages/Python/Resources/"
    ]

    def parse(self, response):
        filename = response.url.split("/")[-2]

        fileoutput = open(filename, 'w')

        selector = Selector(response)
        tableRows = selector.xpath("//table[@id='faceted']//tr")

        logging.info("Starting new parse\n")
        logging.info("URL search: " + response.url)

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

            """Now seeing if there are any attributes for memorbilia, autograph, serial number or rookie card in the same column
                these are done as special divs inside the same column in the element above"""

            testAuto  = tableRow.xpath('./td/div[@class="attr au"]/text()').extract()
            testMemorabilia  = tableRow.xpath('./td/div[@class="attr mem"]/text()').extract()
            testRookieCard  = tableRow.xpath('./td/div[@class="attr rc"]/text()').extract()
            testSerialNumber = tableRow.xpath('./td/div[@class="attr sn"]/text()').extract()

            print("Tetsing divs for:" + originalItemDescription)

            print testAuto
            print "Test auto length " + str(len(testAuto))
            print testMemorabilia
            print "Test mem " + str(len(testMemorabilia))
            print testRookieCard
            print testSerialNumber

            

            if len(testAuto) > 0:
                logging.info("Is an Auto")
                item['autograph'] = len(testAuto)
            if testMemorabilia is not None:
                logging.info("Is  memorabilia")
                print "is memorabilia"
            if testRookieCard is not None:
                logging.info("Is a RC")
                print "is rc"


            """Getting the serial number which is in a separate column and is listed as a number on becket"""

            testSerialNumber  = ''.join(tableRow.xpath('./td/text()').re("\d+"))

            try:
                serialNumber = int(testSerialNumber)
                item['serialNumber'] = serialNumber
            except:
                 # the serial number is not a number and is empty. mark this item for inverstigation
                logging.warn("There is no serial number listed for this item: "+originalItemDescription)

            fileoutput.write(str(item)+"\n")

        fileoutput.close()