__author__ = 'Tom'

import re
from scrapy.spider import Spider
from scrapy.selector import Selector
from scrapy.selector import HtmlXPathSelector
from tutorial.items import BeckettItem

from beckett_parser import parseBeckettTableRow

import logging
logging.basicConfig(filename='parsing.log',level=logging.DEBUG)

class BeckettSpider(Spider):
    name = "beckett"
    allowed_domains = ["www.beckett.com"]
    start_urls = [
        "http://www.beckett.com/search/?term=1997+printing+plates&tmm=extended&attr=24470&rowNum=5000&page=1"
        #"http://www.dmoz.org/Computers/Programming/Languages/Python/Resources/"
    ]

    def parse(self, response):
        filename = response.url.split("/")[-2]

        fileoutput = open(filename, 'w')

        selector = Selector(response)
        tableRows = selector.xpath("//table[@id='faceted']//tr")
        becketItems = []

        logging.info("Starting new parse\n")
        logging.info("URL search: " + response.url)

        for tableRow in tableRows:
            print "Parsing Row"

            """ Getting the whole item description, which we need to cut up, it is a text element which contains a hash"""

            #convert list to string from xpath query and clean any white space off the edges, strip
            itemDescription = ''.join(tableRow.xpath('./td/a/text()').re(".*#.*"))

            #cache the raw item description as we are going to be parsing it and splicing it up
            originalItemDescription = itemDescription

            # This will could look something like

            print originalItemDescription
            logging.info("Parsing item description: "+originalItemDescription)

            item = parseBeckettTableRow(itemDescription, logging)

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