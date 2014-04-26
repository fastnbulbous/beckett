# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class BeckettItem(Item):
    setName = Field()
    beckettLink = Field()
    imageLink = Field()
    description = Field()
    cardNumber = Field()
    serialNumber = Field()
    year = Field()
    errorInformation = Field()
    subsetName = Field()
    team = Field()
    playerNames = Field()
    autograph = Field()
    memorabilia = Field()
    rookieCard = Field()
    originalItemDescription = Field()
    sport = Field()
    team = Field()