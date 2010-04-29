import os
import cgi
import random
import datetime
import time
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db
from google.appengine.ext.webapp import template

cheatColonists = True
cheatOccupied = True
cheatPresence = False

tokenType = [
	{
		'name': 'Industry',
		'image': 'images/token-industry.png',
	},
	{
		'name': 'Culture',
		'image': 'images/token-culture.png',
	},
	{
		'name': 'Finance',
		'image': 'images/token-finance.png',
	},
	{
		'name': 'Politics',
		'image': 'images/token-politics.png',
	},
	{
		'name': 'Ship/Draw',
		'image': 'images/token-ship-draw.png',
	},
	{
		'name': 'Occupy/Draw',
		'image': 'images/token-occupy-draw.png',
	},
	{
		'name': 'Attack',
		'image': 'images/token-attack.png',
	},
	{
		'name': 'Pay',
		'image': 'images/token-pay.png',
	},
	{
		'name': 'Black',
		'image': 'images/colonist-black.png',
	},
	{
		'name': 'White',
		'image': 'images/colonist-white.png',
	},
	{
		'name': 'Red',
		'image': 'images/colonist-red.png',
	},
	{
		'name': 'Green',
		'image': 'images/colonist-green.png',
	},
	{
		'name': 'Purple',
		'image': 'images/colonist-purple.png',
	},
]

buildings = [
    {
        'name': 'Colonial House',
        'image': 'images/building-colonial-house.jpg',
        'tier': 1,
        'x': 0*113,
        'y': 0*75,
        'remaining': 0,
        'points': [0,0,0,0,0],
        'multipleAction': False,
    },
    {
        'name': 'Workshop',
        'image': 'images/building-workshop.jpg',
        'tier': 1,
        'x': 0*113,
        'y': 0*75,
        'remaining': 5,
        'points': [2,0,0,0,0],
        'multipleAction': False,
    },
    {
        'name': 'Shipyard',
        'image': 'images/building-shipyard.jpg',
        'tier': 1,
        'x': 0*113,
        'y': 1*75,
        'remaining': 5,
        'points': [0,1,0,0,0],
        'multipleAction': False,
    },
    {
        'name': 'Market',
        'image': 'images/building-market.jpg',
        'tier': 1,
        'x': 0*113,
        'y': 2*75,
        'remaining': 5,
        'points': [0,0,0,0,0],
        'multipleAction': False,
    },
    {
        'name': 'Barracks',
        'image': 'images/building-barracks.jpg',
        'tier': 2,
        'x': 1*113,
        'y': 0*75,
        'remaining': 4,
        'points': [0,0,0,0,0],
        'multipleAction': False,
    },
    {
        'name': 'Bank',
        'image': 'images/building-bank.jpg',
        'tier': 2,
        'x': 1*113,
        'y': 1*75,
        'remaining': 4,
        'points': [0,0,2,0,0],
        'multipleAction': False,
    },
    {
        'name': 'Guild Hall',
        'image': 'images/building-guild-hall.jpg',
        'tier': 2,
        'x': 1*113,
        'y': 2*75,
        'remaining': 4,
        'points': [0,0,0,0,0],
        'multipleAction': False,
    },
    {
        'name': 'Theater',
        'image': 'images/building-theater.jpg',
        'tier': 3,
        'x': 2*113,
        'y': 0*75,
        'remaining': 3,
        'points': [0,2,0,0,0],
        'multipleAction': False,
    },
    {
        'name': 'Fortress',
        'image': 'images/building-fortress.jpg',
        'tier': 3,
        'x': 2*113,
        'y': 1*75,
        'remaining': 3,
        'points': [0,0,0,1,0],
        'multipleAction': False,
    },
    {
        'name': 'Docks',
        'image': 'images/building-docks.jpg',
        'tier': 3,
        'x': 2*113,
        'y': 2*75,
        'remaining': 3,
        'points': [0,0,0,0,0],
        'multipleAction': True,
    },
    {
        'name': 'University',
        'image': 'images/building-university.jpg',
        'tier': 4,
        'x': 3*113,
        'y': 0*75,
        'remaining': 2,
        'points': [0,0,0,0,3],
        'multipleAction': False,
    },
    {
        'name': 'Trade Office',
        'image': 'images/building-trade-office.jpg',
        'tier': 4,
        'x': 3*113,
        'y': 1*75,
        'remaining': 2,
        'points': [0,0,0,0,0],
        'multipleAction': True,
    },
    {
        'name': 'Cartographer',
        'image': 'images/building-cartographer.jpg',
        'tier': 4,
        'x': 3*113,
        'y': 2*75,
        'remaining': 2,
        'points': [0,0,0,0,0],
        'multipleAction': True,
    },
    {
        'name': 'Museum',
        'image': 'images/building-museum.jpg',
        'tier': 5,
        'x': 4*113,
        'y': 0*75,
        'remaining': 1,
        'points': [0,2,0,0,0],
        'multipleAction': False,
    },
    {
        'name': 'Parliament',
        'image': 'images/building-parliament.jpg',
        'tier': 5,
        'x': 4*113,
        'y': 1*75,
        'remaining': 1,
        'points': [0,0,0,2,0],
        'multipleAction': False,
    },
    {
        'name': 'Exchange',
        'image': 'images/building-exchange.jpg',
        'tier': 5,
        'x': 4*113,
        'y': 2*75,
        'remaining': 1,
        'points': [0,0,2,0,0],
        'multipleAction': False,
    },
]

locations = [
	{ 'x': 1091, 'y': 752 },
	{ 'x': 1092, 'y': 921 },
	{ 'x': 914, 'y': 920 },
	{ 'x': 869, 'y': 671 },
	{ 'x': 751, 'y': 602 },
	{ 'x': 716, 'y': 470 },
	{ 'x': 964, 'y': 526 },
	{ 'x': 547, 'y': 658 },
	{ 'x': 632, 'y': 690 },
	{ 'x': 760, 'y': 867 },
	{ 'x': 757, 'y': 1060 },
	{ 'x': 840, 'y': 1115 },
	{ 'x': 90, 'y': 1180 },
	{ 'x': 184, 'y': 1231 },
	{ 'x': 201, 'y': 1136 },
	{ 'x': 128, 'y': 572 },
	{ 'x': 270, 'y': 848 },
	{ 'x': 154, 'y': 738 },
	{ 'x': 37, 'y': 308 },
	{ 'x': 130, 'y': 239 },
	{ 'x': 177, 'y': 142 },
	{ 'x': 420, 'y': 32 },
	{ 'x': 531, 'y': 272 },
	{ 'x': 594, 'y': 162 },
	{ 'x': 922, 'y': 262 },
	{ 'x': 951, 'y': 170 },
	{ 'x': 1062, 'y': 139 },
	{ 'x': 1180, 'y': 374 },
	{ 'x': 1154, 'y': 110 },
	{ 'x': 606, 'y': 1071 },	# africa shipping
	{ 'x': 600, 'y': 1123 },
	{ 'x': 606, 'y': 1177 },
	{ 'x': 628, 'y': 1223 },
	{ 'x': 668, 'y': 1257 },
	{ 'x': 718, 'y': 1273 },
	{ 'x': 459, 'y': 991 },		# south america shipping
	{ 'x': 425, 'y': 1031 },
	{ 'x': 402, 'y': 1078 },
	{ 'x': 439, 'y': 1118 },
	{ 'x': 472, 'y': 1160 },
	{ 'x': 484, 'y': 1211 },
	{ 'x': 66, 'y': 493 },		# caribbean shipping
	{ 'x': 42, 'y': 541 },
	{ 'x': 30, 'y': 592 },
	{ 'x': 25, 'y': 645 },
	{ 'x': 24, 'y': 699 },
	{ 'x': 26, 'y': 752 },
	{ 'x': 307, 'y': 272 },		# north america shipping
	{ 'x': 312, 'y': 218 },
	{ 'x': 314, 'y': 166 },
	{ 'x': 312, 'y': 113 },
	{ 'x': 292, 'y': 64 },
	{ 'x': 252, 'y': 31 },
	{ 'x': 200, 'y': 23 },
	{ 'x': 766, 'y': 226 },		# india shipping
	{ 'x': 804, 'y': 189 },
	{ 'x': 820, 'y': 139 },
	{ 'x': 818, 'y': 87 },
	{ 'x': 786, 'y': 47 },
	{ 'x': 736, 'y': 28 },
	{ 'x': 684, 'y': 25 },
	{ 'x': 1246, 'y': 255 },	# far east shipping
	{ 'x': 1261, 'y': 204 },
	{ 'x': 1276, 'y': 153 },
	{ 'x': 1286, 'y': 102 },
	{ 'x': 1268, 'y': 53 },
	{ 'x': 1223, 'y': 27 },
	{ 'x': 1171, 'y': 21 },
	{ 'x': 1118, 'y': 25 },
	{ 'x': 1142, 'y': 817 },	# europe connections
	{ 'x': 1002, 'y': 823 },
	{ 'x': 956, 'y': 759 },
	{ 'x': 858, 'y': 597 },
	{ 'x': 728, 'y': 1169 },	# africa connections
	{ 'x': 774, 'y': 936 },
	{ 'x': 1015, 'y': 1063 },
	{ 'x': 156, 'y': 903 },		# south america connections
	{ 'x': 380, 'y': 867 },
	{ 'x': 519, 'y': 878 },
	{ 'x': 286, 'y': 690 },		# caribbean connections
	{ 'x': 266, 'y': 519 },
	{ 'x': 326, 'y': 577 },
	{ 'x': 377, 'y': 723 },
	{ 'x': 72, 'y': 169 },		# north america connections
	{ 'x': 367, 'y': 517 },
	{ 'x': 506, 'y': 453 },
	{ 'x': 569, 'y': 527 },
	{ 'x': 476, 'y': 224 },		# india connections
	{ 'x': 478, 'y': 350 },
	{ 'x': 727, 'y': 332 },
	{ 'x': 782, 'y': 285 },
	{ 'x': 823, 'y': 455 },
	{ 'x': 1128, 'y': 257 },	# far east connections
	{ 'x': 953, 'y': 435 },
	{ 'x': 1068, 'y': 535 },
	
	# extra shipping spots
	{ 'x': 656, 'y': 1031 },	# africa shipping 95
	{ 'x': 650, 'y': 1083 },
	{ 'x': 656, 'y': 1137 },
	{ 'x': 678, 'y': 1183 },
	{ 'x': 718, 'y': 1217 },
	{ 'x': 409, 'y': 991 },		# south america shipping
	{ 'x': 375, 'y': 1031 },
	{ 'x': 352, 'y': 1078 },
	{ 'x': 389, 'y': 1118 },
	{ 'x': 422, 'y': 1160 },
	{ 'x': 116, 'y': 493 },		# caribbean shipping
	{ 'x': 92, 'y': 541 },
	{ 'x': 80, 'y': 592 },
	{ 'x': 75, 'y': 645 },
	{ 'x': 74, 'y': 699 },
	{ 'x': 257, 'y': 272 },		# north america shipping
	{ 'x': 262, 'y': 218 },
	{ 'x': 264, 'y': 166 },
	{ 'x': 262, 'y': 113 },
	{ 'x': 242, 'y': 64 },
	{ 'x': 716, 'y': 226 },		# india shipping
	{ 'x': 754, 'y': 189 },
	{ 'x': 770, 'y': 139 },
	{ 'x': 768, 'y': 87 },
	{ 'x': 736, 'y': 47 },
	{ 'x': 1196, 'y': 255 },	# far east shipping
	{ 'x': 1211, 'y': 204 },
	{ 'x': 1226, 'y': 153 },
	{ 'x': 1236, 'y': 102 },
	{ 'x': 1218, 'y': 53 },
]

connections = [
	[0, 1],
	[1, 2],
	[0, 3],
	[3, 4],
	[10, 11],
	[9, 10],
	[1, 11],
	[14, 17],
	[7, 14],
	[8, 13],
	[15, 16],
	[15, 18],
	[8, 15],
	[7, 16],
	[19, 20],
	[9, 18],
	[5, 20],
	[4, 19],
	[21, 22],
	[5, 21],
	[23, 24],
	[23, 25],
	[6, 22],
	[26, 27],
	[6, 24],
	[0, 25],
]

playerColors = [
	{
		'name': 'Black',
		'image': 'images/colonist-black.png',
		'markerImage': 'images/marker-black.png',
		'colonistFontColor': 'white'
	},
	{
		'name': 'White',
		'image': 'images/colonist-white.png',
		'markerImage': 'images/marker-white.png',
		'colonistFontColor': 'black'
	},
	{
		'name': 'Red',
		'image': 'images/colonist-red.png',
		'markerImage': 'images/marker-red.png',
		'colonistFontColor': 'white'
	},
	{
		'name': 'Green',
		'image': 'images/colonist-green.png',
		'markerImage': 'images/marker-green.png',
		'colonistFontColor': 'white'
	},
	{
		'name': 'Purple',
		'image': 'images/colonist-purple.png',
		'markerImage': 'images/marker-purple.png',
		'colonistFontColor': 'white'
	},
]

cards = [
	[0,0,2,1,1, 'images/card-africa0.png', 'Africa-Gov'],
	[1,0,0,1,0, 'images/card-africa1.png', 'Africa-1'],
	[1,0,1,1,0, 'images/card-africa2.png', 'Africa-2'],
	[0,0,2,2,0, 'images/card-africa3.png', 'Africa-3'],
	[2,0,1,1,1, 'images/card-africa4.png', 'Africa-4'],
	[2,0,2,0,2, 'images/card-africa5.png', 'Africa-5'],

	[0,0,0,3,1, 'images/card-south-america0.png', 'South America-Gov'],
	[0,2,0,0,0, 'images/card-south-america1.png', 'South America-1'],
	[0,3,0,0,0, 'images/card-south-america2.png', 'South America-2'],
	[0,4,0,0,0, 'images/card-south-america3.png', 'South America-3'],
	[0,0,3,0,2, 'images/card-south-america4.png', 'South America-4'],
	[0,0,3,0,3, 'images/card-south-america5.png', 'South America-5'],

	[2,1,0,0,1, 'images/card-far-east0.png', 'Far East-Gov'],
	[1,0,1,0,0, 'images/card-far-east1.png', 'Far East-1'],
	[2,0,1,0,0, 'images/card-far-east2.png', 'Far East-2'],
	[2,0,2,0,0, 'images/card-far-east3.png', 'Far East-3'],
	[1,1,1,1,1, 'images/card-far-east4.png', 'Far East-4'],
	[0,0,0,3,3, 'images/card-far-east5.png', 'Far East-5'],

	[0,1,1,1,1, 'images/card-india0.png', 'India-Gov'],
	[0,1,0,1,0, 'images/card-india1.png', 'India-1'],
	[0,1,1,1,0, 'images/card-india2.png', 'India-2'],
	[0,1,2,1,0, 'images/card-india3.png', 'India-3'],
	[0,0,2,1,2, 'images/card-india4.png', 'India-4'],
	[0,0,2,2,2, 'images/card-india5.png', 'India-5'],

	[0,2,0,1,1, 'images/card-caribbean0.png', 'Caribbean-Gov'],
	[0,0,0,2,0, 'images/card-caribbean1.png', 'Caribbean-1'],
	[0,0,1,2,0, 'images/card-caribbean2.png', 'Caribbean-2'],
	[0,0,4,0,0, 'images/card-caribbean3.png', 'Caribbean-3'],
	[0,0,0,3,2, 'images/card-caribbean4.png', 'Caribbean-4'],
	[3,0,0,0,3, 'images/card-caribbean5.png', 'Caribbean-5'],

	[0,0,1,2,1, 'images/card-north-america0.png', 'North America-Gov'],
	[2,0,0,0,0, 'images/card-north-america1.png', 'North America-1'],
	[0,0,3,0,0, 'images/card-north-america2.png', 'North America-2'],
	[2,2,0,0,0, 'images/card-north-america3.png', 'North America-3'],
	[0,2,0,2,1, 'images/card-north-america4.png', 'North America-4'],
	[0,0,0,0,6, 'images/card-north-america5.png', 'North America-5'],

	[0,1,1,0,0, 'images/card-mediterranean0.png', 'Mediterranean-0'],
	[0,2,0,1,0, 'images/card-mediterranean1.png', 'Mediterranean-1'],
	[0,0,0,3,0, 'images/card-mediterranean2.png', 'Mediterranean-2'],
	[1,1,1,1,0, 'images/card-mediterranean3.png', 'Mediterranean-3'],
	[0,0,0,0,5, 'images/card-mediterranean4.png', 'Mediterranean-4'],
	[0,3,0,0,3, 'images/card-mediterranean5.png', 'Mediterranean-5'], # abolition of slavery

	[2,0,0,0,0, 'images/card-slavery0.png', 'Slavery-0'],
	[0,0,2,0,0, 'images/card-slavery1.png', 'Slavery-1'],
	[1,0,2,0,0, 'images/card-slavery2.png', 'Slavery-2'],
	[3,0,0,0,0, 'images/card-slavery3.png', 'Slavery-3'],
	[2,0,2,0,0, 'images/card-slavery4.png', 'Slavery-4'],
	[3,0,2,0,0, 'images/card-slavery5.png', 'Slavery-5'],
]

cardLocations = [
	[797,1190,True],
	[338,1190,True],
	[970,-10,True],
	[535,-10,True],
	[22,804,False],
	[51,-10,True],
	[1208,483,False],
	[1208,698,False],
]

regionTokens = [
	[0,1,2,3,4,5,6,7,8,9],
	[10,11],
	[12,13,14],
	[15,16,17],
	[18,19,20],
	[21,22,23],
	[24,25,26,27,28],
]

regionShippingTokens = [
	[],
	[29,30,31,32,33,34,  95,96,97,98,99],
	[35,36,37,38,39,40, 100,101,102,103,104],
	[41,42,43,44,45,46, 105,106,107,108,109],
	[47,48,49,50,51,52,53, 110,111,112,113,114],
	[54,55,56,57,58,59,60, 115,116,117,118,119],
	[61,62,63,64,65,66,67,68, 120,121,122,123,124],
]

tokenRegions = [0]*69
for region in range(0,len(regionTokens)):
	for locationInRegion in range(0,len(regionTokens[region])):
		tokenRegions[regionTokens[region][locationInRegion]] = region
		
shippingTokenRegions = [0]*125 #[0]*69
for region in range(0,len(regionShippingTokens)):
	for locationInRegion in range(0,len(regionShippingTokens[region])):
		shippingTokenRegions[regionShippingTokens[region][locationInRegion]] = region

pointsToTier = [1,1,2,2,3,3,3,4,4,4,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5]
pointsToScore = [0,0,2,2,4,4,4,7,7,7,10]

Position_OCCUPY, Position_SHIP, Position_CARD, Position_BUILDING, Position_ATTACK, Position_INVALID = range(6)
Phase_BUILD, Phase_PAY, Phase_ACTION, Phase_WAITING_FOR_PLAYERS, Phase_GAMEOVER = range(5)
phaseToStr = ['Build', 'Pay', 'Action', 'Waiting to start', 'Game Over']

error = ''

def colonistImage(playerId):
	return playerColors[playerId]['image']

def buildingImage(buildingId):
	return buildings[buildingId]['image']

def IsMultipleActionBuilding(buildingId):
	return buildings[buildingId]['multipleAction']

def buildingLocationX(buildingLocationId):
	return (buildingLocationId % 4) * 117 + 16

def buildingLocationY(buildingLocationId):
	return (buildingLocationId / 4) * 79 + 308

def tokenImage(tokenId):
	return tokenType[tokenId]['image']

def locationX(locationId):
	return locations[locationId]['x']

def locationY(locationId):
	return locations[locationId]['y']

def markerLocationX(value):
	return value * 41.5 + 10
	
def playerTokenLocationX(tokenId):
	return 490 + (tokenId - 4) * 48

def cardLocationX(cardPos):
	return cardPos * 111 + 9

def cardImage(card):
	return cards[card][5]

def cardBoardLocationX(region):
	return cardLocations[region][0]

def cardBoardLocationY(region):
	return cardLocations[region][1]
	
def isRotatedCard(region):
	return cardLocations[region][2]

def isNotNegativeOne(value):
	return value != -1
	
def get_range(start, stop):
	return range(start,stop)

def greaterThan(v1, v2):
	return v1 > v2

def lessThan(v1, v2):
	return v1 < v2
	
def markerImage(player):
	return playerColors[player]['markerImage']
	
def colonistFontColor(player):
	return playerColors[player]['colonistFontColor']
	
def PhaseToStr(phase):
	return phaseToStr[phase]
	
def formatTime(datetime):
	return datetime.strftime("%Y-%m-%d %H:%M %Z")

def add(v1, v2):
	return v1 + int(v2)

register = webapp.template.create_template_register()
register.filter(colonistImage)
register.filter(buildingImage)
register.filter(IsMultipleActionBuilding)
register.filter(buildingLocationX)
register.filter(buildingLocationY)
register.filter(tokenImage)
register.filter(locationX)
register.filter(locationY)
register.filter(markerLocationX)
register.filter(playerTokenLocationX)
register.filter(cardLocationX)
register.filter(cardImage)
register.filter(isNotNegativeOne)
register.filter(get_range)
register.filter(greaterThan)
register.filter(lessThan)
register.filter(cardBoardLocationX)
register.filter(cardBoardLocationY)
register.filter(isRotatedCard)
register.filter(markerImage)
register.filter(colonistFontColor)
register.filter(PhaseToStr)
register.filter(formatTime)
register.filter(add)
webapp.template.register_template_library('endeavor')

class Global(db.Model):
	waitingGames = db.ListProperty(str)

class Game(db.Model):
	numPlayers = db.IntegerProperty()
	boardTokens = db.ListProperty(int)
	tokenHighlighted = db.ListProperty(bool)
	firstPlayer = db.IntegerProperty()
	turn = db.IntegerProperty()
	phase = db.IntegerProperty()
	remainingBuildings = db.ListProperty(int)
	remainingCards = db.ListProperty(bool)
	playerPassed = db.ListProperty(bool)
	chatHistory = db.ListProperty(str)
	name = db.StringProperty()
	timeCreated = db.DateTimeProperty()
	step = db.IntegerProperty()

class Player(db.Model):
	game = db.ReferenceProperty(Game)
	position = db.IntegerProperty() # also denotes color
	user = db.UserProperty()
	buildings = db.ListProperty(int)
	buildingsOccupied = db.ListProperty(bool)
	colonists = db.IntegerProperty()
	tokenCounts = db.ListProperty(int) # industry, culture, finance, politics, 4 action ones, extra points
	cards = db.ListProperty(int)
	paysLeft = db.IntegerProperty()
	timeCreated = db.DateTimeProperty()

game = 0
players = 0

def GetTopCards():
    global game

    topCards = [-1,-1,-1,-1,-1,-1,-1,-1]
    for region in range(0,8):
        lowest=-1
        for card in range(0,6):
            cardId = region*6 + card
            if lowest == -1 and game.remainingCards[cardId]:
                lowest = cardId
        topCards[region] = lowest
    return topCards

class MainPage(webapp.RequestHandler):
	def get(self):
		global game, players

		gameId = self.request.get('game')
		failed = False
		try:
			game = db.get(db.Key(gameId))
		except:
			failed = True
		if failed or not game:
			self.redirect('/gamelist')
			return

		playersQuery = game.player_set
		playersQuery.order('position')
		players = playersQuery.fetch(100)
		
		waitForAfterStep = self.request.get('wait')
		if waitForAfterStep != '':
			try:
				waitForAfterStep = int(waitForAfterStep)
			except:
				waitForAfterStep=0
			if game.step > waitForAfterStep:
				self.RenderGame()
				return
			self.response.out.write('')
			return

		self.RenderGame()

	def RenderGame(self):
		global game, players, error
		
		if self.request.get('ajax'):
			renderTopAndBottom = False
		else:
			renderTopAndBottom = True

		gameId = self.request.get('game')

		if users.get_current_user():
			url = users.create_logout_url(self.request.uri)
			url_linktext = 'Logout ' + users.get_current_user().nickname()
		else:
			url = users.create_login_url(self.request.uri)
			url_linktext = 'Login'

		if game.phase == Phase_WAITING_FOR_PLAYERS:
			template_values = {
				'url': url,
				'url_linktext': url_linktext,
				'game': game,
				'gameId': gameId,
				'players': players,
				'error': error,
			}

			if renderTopAndBottom:
				path = os.path.join(os.path.dirname(__file__), 'top.html')
				self.response.out.write(template.render(path, template_values))
			path = os.path.join(os.path.dirname(__file__), 'waiting.html')
			self.response.out.write(template.render(path, template_values))
			if renderTopAndBottom:
				path = os.path.join(os.path.dirname(__file__), 'bottom.html')
				self.response.out.write(template.render(path, template_values))
		else:
			playersForTemplate = list()
			topPlayer = GetUserPosition()
			if topPlayer == -1:
				topPlayer = 0
			for i in range(topPlayer, len(players)) + range(0, topPlayer):
				player = players[i]
				player.zippedBuildings = zip(player.buildings, player.buildingsOccupied)
				player.isFirstPlayer = player.position == game.firstPlayer
				player.isCurrentPlayer = player.position == game.turn
				playersForTemplate.append(player)

			for i in range(0, len(buildings)):
				buildings[i]['remaining'] = game.remainingBuildings[i]

			template_values = {
				'url': url,
				'url_linktext': url_linktext,
				'buildings': buildings,
				'game': game,
				'gameId': gameId,
				'players': playersForTemplate,
				'topCards': GetTopCards(),
				'currentPlayer': players[game.turn],
				'error': error,
			}

			if renderTopAndBottom:
				path = os.path.join(os.path.dirname(__file__), 'top.html')
				self.response.out.write(template.render(path, template_values))
			path = os.path.join(os.path.dirname(__file__), 'game.html')
			self.response.out.write(template.render(path, template_values))
			if renderTopAndBottom:
				path = os.path.join(os.path.dirname(__file__), 'bottom.html')
				self.response.out.write(template.render(path, template_values))


def DrawCard(playerId, card):
	global game, players
	players[playerId].cards.append(card)
	players[playerId].tokenCounts[0] += cards[card][0]
	players[playerId].tokenCounts[1] += cards[card][1]
	players[playerId].tokenCounts[2] += cards[card][2]
	players[playerId].tokenCounts[3] += cards[card][3]
	players[playerId].tokenCounts[8] += cards[card][4]
	if card == 6*6+5: # abolish slavery
		for i in range(0,len(players)):
			for j in range(0,len(players[i].cards)):
				removed = True
				while removed and j<len(players[i].cards):
					c = players[i].cards[j]
					if int(c / 6) == 7:
						Discard(i, c)
#						players[i].cards.remove(c)
#						players[i].tokenCounts[8] -= 1
					else:
						removed = False
			players[i].put()
		for slaveryCard in range(7*6, 8*6):
			game.remainingCards[slaveryCard] = False
		
	game.remainingCards[card] = False
	players[playerId].put()

def Discard(playerId, card):
	global players, game

	if not card in players[playerId].cards:
		error = 'That card is unavailable'
		return False # shouldn't happen. hacker attempt maybe.

	players[playerId].tokenCounts[0] -= cards[card][0]
	players[playerId].tokenCounts[1] -= cards[card][1]
	players[playerId].tokenCounts[2] -= cards[card][2]
	players[playerId].tokenCounts[3] -= cards[card][3]
	players[playerId].tokenCounts[8] -= cards[card][4]
	isSlaveryCard = int(card/6) == 7
	if isSlaveryCard:
		players[playerId].tokenCounts[8] -= 1
	if not isSlaveryCard and not IsGovernorCard(card):
		game.remainingCards[card] = True
	players[playerId].cards.remove(card)
	ChatHistory(players[playerId], 'discarded card ' + cards[card][6])
	players[playerId].put()
	return True

def HandOutGovernorCard(ships, region):
	counts = [0,0,0,0,0]
	most = -1
	winner = -1
	for i in ships:
		player = i-8;
		if player>=0 and player<=4:
			counts[player] += 1
			if counts[player] >= most:
				most = counts[player]
				winner = player
	
	DrawCard(winner, region*6)

def GetCardRegion(card):
	x = int(card / 6)
	xToRegion = [1,2,6,5,3,4,0,0]
	return xToRegion[x]

def GetPresence(playerId, region):
	global game, players
	presence = 0
	for i in regionTokens[region]:
		if game.boardTokens[i] == playerId+8:
			presence += 1
	for i in regionShippingTokens[region]:
		if game.boardTokens[i] == playerId+8:
			presence += 1
	return presence

def IsGovernorCard(card):
	return card in [0,6,12,18,24,30]

def IsSlaveryCard(card):
	return int(card/6) == 7

def CanOccupy(player, tokenLocation):
	global error
	
	region = tokenRegions[tokenLocation]
	if region == 0:
		return True
	for i in regionShippingTokens[region]:
		if not game.boardTokens[i] in [-1,8,9,10,11,12]:
			error = 'That region isn\'t opened up yet'
			return False
	if GetPresence(player, region) < 1:
		error = 'You don\'t have presence there'
		return False
	return True

def GetPositionType(pos):
	global game
	
	if pos>=0 and pos<=28:
		if game.boardTokens[pos] in [8,9,10,11,12]:
			return Position_ATTACK
		else:
			return Position_OCCUPY
	if pos>=29 and pos<=68:
#		if game.boardTokens[pos] in [0,1,2,3,4,5,6,7]:
			return Position_SHIP
#		else:
#			return Position_INVALID
	if pos>=200 and pos<200+6*8:
		return Position_CARD
	if pos>=100 and pos<100+8:
		return Position_BUILDING
		
def Draw(card):
	global players, game, error
	
	topCards = GetTopCards()
	stack = int(card / 6)
	card = topCards[stack]
	if card == -1:
		error = 'Invalid card'
		return False

	if IsGovernorCard(card):
		error = 'You can\'t draw a governor card'
		return False
	
	region = GetCardRegion(card)
	presenceNeeded = card % 6
	presence = GetPresence(game.turn, region)
	if presence < presenceNeeded and not cheatPresence:
		error = 'You don\'t have the required presence'
		return False

	DrawCard(game.turn, card)
	ChatHistory(players[game.turn], 'drew card ' + cards[card][6])
	return True
	
def GetNextShippingLocation(region):
	global game
	
	for location in regionShippingTokens[region]:
		if game.boardTokens[location] in [-1,0,1,2,3,4,5,6,7]:
			return location
	return -1

def Ship(arg):
	global players, game, error
	
	region = shippingTokenRegions[arg]
	location = GetNextShippingLocation(region)
	if location == -1:
		error = 'That shipping track is full'
		return False	

	token = game.boardTokens[location]
#	if not (arg in [29,29+6,29+6+6,29+6+6+6,29+6+6+6+7,29+6+6+6+7+7] or game.boardTokens[arg-1] in [8,9,10,11,12]):
#		error = 'Invalid shipping location'
#		return False
		
	players[game.turn].colonists -= 1
	game.boardTokens[location] = 8 + players[game.turn].position
	Highlight(location)

	increaseDescription = ''
	if token != -1:
		players[game.turn].tokenCounts[token] += 1
		increaseDescription = ' (Gained ' + tokenType[token]['name'] + ')'

	if location == 29+5:
		HandOutGovernorCard(game.boardTokens[29:29+6], 0)
	elif location == 29+6+5:
		HandOutGovernorCard(game.boardTokens[29+6:29+6+6], 1)
	elif location == 29+6+6+5:
		HandOutGovernorCard(game.boardTokens[29+6+6:29+6+6+6], 4)
	elif location == 29+6+6+6+6:
		HandOutGovernorCard(game.boardTokens[29+6+6+6:29+6+6+6+7], 5)
	elif location == 29+6+6+6+7+6:
		HandOutGovernorCard(game.boardTokens[29+6+6+6+7:29+6+6+6+7+7], 3)
	elif location == 29+6+6+6+7+7+7:
		HandOutGovernorCard(game.boardTokens[29+6+6+6+7+7:29+6+6+6+7+7+8], 2)
		
	ChatHistory(players[game.turn], 'shipped ' + str(location) + increaseDescription)

	return True

def ResetHighlight():
	global game

	game.tokenHighlighted = [False]*(95+6*5)

def Highlight(arg):
	global game
	
	if not game.tokenHighlighted:
		ResetHighlight()
	game.tokenHighlighted[arg] = True
	
def Occupy(arg, attack=False):
	global players, game, error

	if not CanOccupy(game.turn, arg):
		return False
		
	token = game.boardTokens[arg]
	if token == players[game.turn].position + 8:
		error = 'Can\'t attack your own location'
		return False
#	if not (token>=0 and token<=7):
#		return False

	increaseDescription = ''
	attackToken = token

	players[game.turn].colonists -= 1
	game.boardTokens[arg] = 8 + players[game.turn].position
	Highlight(arg)
	if token>=0 and token<=7:
		players[game.turn].tokenCounts[token] += 1
		if increaseDescription:
			increaseDescription += ', '
		increaseDescription += tokenType[token]['name']

	for i in range(0, len(connections)):
		connection = connections[i]
		if (connection[0] == arg and game.boardTokens[connection[1]] == players[game.turn].position + 8) \
			or (connection[1] == arg and game.boardTokens[connection[0]] == players[game.turn].position + 8):
			connectionTokenIndex = i + 69
			token = game.boardTokens[connectionTokenIndex]
			players[game.turn].tokenCounts[token] += 1
			if increaseDescription:
				increaseDescription += ', '
			increaseDescription += tokenType[token]['name'] 
			game.boardTokens[connectionTokenIndex] = -1
			Highlight(connectionTokenIndex)
			
	if increaseDescription:
		increaseDescription = ' (Gained ' + increaseDescription + ')'

	if attack:
		ChatHistory(players[game.turn], 'attacked ' + tokenType[attackToken]['name'] + ' at '+ str(arg) + increaseDescription)
	else:
		ChatHistory(players[game.turn], 'occupied ' + str(arg) + increaseDescription)
			
	return True
	
def Attack(arg):
	global players
	
	success = Occupy(arg, True)
	if success:
		players[game.turn].colonists -= 1
	return success
	
def Pay(arg):
	global players, error

	if not players[game.turn].buildingsOccupied[arg]:
		error = 'Attempting to pay a non-occupied building'
		return False
	players[game.turn].buildingsOccupied[arg] = False
	players[game.turn].colonists += 1
	ChatHistory(players[game.turn], 'payed the ' + buildings[players[game.turn].buildings[arg]]['name'])
	return True

def Grow():
	global players
	for i in range(0, len(players)):
		players[i].colonists += pointsToTier[players[i].tokenCounts[1]] + 1
		players[i].put()

def AutoPay():
	global game, players
	
	money = pointsToTier[players[game.turn].tokenCounts[2]]
	numOccupied = 0
	for occupied in players[game.turn].buildingsOccupied:
		if occupied:
			numOccupied += 1
	if money >= numOccupied:
		for i in range(0,len(players[game.turn].buildingsOccupied)):
			players[game.turn].buildingsOccupied[i] = False
		players[game.turn].colonists += numOccupied
		players[game.turn].put()
		AdvanceTurn()
	else:
		players[game.turn].paysLeft = money
		players[game.turn].put()

def PointsToScore(points):
	if points >= 15:
		return 15 # clip scores to 15
	if points >= 10:
		return points
	return pointsToScore[points]

def CalculateFinalScore():
	global game, players
	
	for player in players:
		score = 0
		for i in range(4):
			score += PointsToScore(player.tokenCounts[i])
		score += player.tokenCounts[8]
		score += int(player.colonists / 3)
		if FreeGovernorCard(player.position) == -1:
			score += 3
		for i in range(0,29):
			token = game.boardTokens[i]
			if token == 8 + player.position:
				if i in [12, 28]: # positions worth 2 points
					score += 2
				else:
					score += 1
		for i in range(0, len(connections)):
			connection = connections[i]
			if (game.boardTokens[connection[0]] == player.position + 8 \
				and game.boardTokens[connection[1]] == player.position + 8):
				score += 1
		player.score = score
	
	sorted(players, key=lambda player: player.score)
	for player in players:
		ChatHistory(player, 'scored ' + str(player.score))
		
def AdvanceTurn():
	global game, players
	game.turn = (game.turn+1) % game.numPlayers
	if game.phase == Phase_BUILD:
		if game.turn == game.firstPlayer:
			Grow()
			game.phase = Phase_PAY
			AutoPay()
	elif game.phase == Phase_PAY:
		if game.turn == game.firstPlayer:
			game.phase = Phase_ACTION
			game.playerPassed = [False]*game.numPlayers
		else:
			AutoPay()
	elif game.phase == Phase_ACTION:
		allPassed = True
		for p in game.playerPassed:
			if not p:
				allPassed = False
		if allPassed:
			if len(players[game.turn].buildings) >= 8:
				game.phase = Phase_GAMEOVER
				CalculateFinalScore()
			else:
				game.firstPlayer = (game.firstPlayer+1) % game.numPlayers
				game.turn = game.firstPlayer
				game.phase = Phase_BUILD
		else:
			while game.playerPassed[game.turn]:
				game.turn = (game.turn+1) % game.numPlayers
			AutoPass()

def PlayerCanAct():
	global game, players
	
	player = players[game.turn]

	if player.tokenCounts[4]>=1:
		return True
	if player.tokenCounts[5]>=1:
		return True
	if player.tokenCounts[6]>=1 and (player.colonists>=2 or cheatColonists):
		return True
	if player.tokenCounts[7]>=1:
		return True

	for i in range(len(player.buildings)):
		if not player.buildingsOccupied[i]:
			if player.buildings[i] in (3,6,11,13,14,15) and (player.colonists>=1 or cheatColonists): # draw and pay
				return True
			if player.buildings[i] in (0,2,6,8,9,12) and (player.colonists>=2 or cheatColonists): # occupy and ship
				return True
			if player.buildings[i] in (4,8) and (player.colonists>=3 or cheatColonists): # attack
				return True

	return False

def AutoPass():
	global game, players

	if (not PlayerCanAct()) and PlayerHasValidCards(game.turn):
		game.playerPassed[game.turn] = True
		ChatHistory(players[game.turn], 'passed')
		players[game.turn].put()
		AdvanceTurn()

def FreeGovernorCard(playerId):
	global game, players
	
	if PlayerHasValidCards(playerId,False, True):
		return -1
	for card in players[playerId].cards:
		if IsGovernorCard(card):
			return card
	return -1

def PlayerHasValidCards(playerId, allowFreeGovernor=True, allowFreeSlavery=True):
	global game, players
	
	cardTier = pointsToTier[players[playerId].tokenCounts[3]]
	hasSlaveryCard = False
	for card in players[playerId].cards:
		if int(card / 6) == 7:
			hasSlaveryCard = True
	
	hasGovernorCard = False
	for card in players[playerId].cards:
		if IsGovernorCard(card):
			hasGovernorCard = True

	allowedCards = cardTier
	if allowFreeSlavery and hasSlaveryCard and cardTier<5:
		allowedCards += 1
	if allowFreeGovernor and hasGovernorCard:
		allowedCards += 1
		
	if len(players[playerId].cards) > allowedCards:
		return False
	else:
		return True

def JoinGame(gameKey):
	global error
	
	if users.get_current_user():
		player = Player(
			game=gameKey,
			user=users.get_current_user(),
			buildings=[0],
			buildingsOccupied=[False],
			tokenCounts=[0,0,0,0,0,0,0,0,0],
			position = 0,
			colonists = 0,
			timeCreated = datetime.datetime.now(),
		)
		player.put()
		PutGame()
	else:
		error = 'Log in first'
		
def CanBuild(building):
	global game, players, error

	if game.remainingBuildings[building] <= 0:
		error = 'Those buildings are all gone'
		return False

		
	playerBuildTier = pointsToTier[players[game.turn].tokenCounts[0]]
	if playerBuildTier==1 and \
		game.remainingBuildings[1]<=0 and \
		game.remainingBuildings[2]<=0 and \
		game.remainingBuildings[3]<=0:
		playerBuildTier = 2
	if playerBuildTier==2 and \
		game.remainingBuildings[4]<=0 and \
		game.remainingBuildings[5]<=0 and \
		game.remainingBuildings[6]<=0:
		playerBuildTier = 3
	if playerBuildTier==3 and \
		game.remainingBuildings[7]<=0 and \
		game.remainingBuildings[8]<=0 and \
		game.remainingBuildings[9]<=0:
		playerBuildTier = 3
	if playerBuildTier==4 and \
		game.remainingBuildings[10]<=0 and \
		game.remainingBuildings[11]<=0 and \
		game.remainingBuildings[12]<=0:
		playerBuildTier = 5
	if playerBuildTier < buildings[building]['tier']:
		error = 'You don\'t have enough production to built that'
		return False

	twoLevelFive = False
	if buildings[building]['tier'] == 5:
		for building in players[game.turn].buildings:
			if buildings[building]['tier'] == 5:
				twoLevelFive = True
				error = 'Can\'t build two level five buildings'
	if twoLevelFive:
		error = 'Can\'t build two level five buildings'
		return False

	return True

def PutGame():
	global game
	if not game.step:
		game.step = 0
	game.step += 1
	game.put()

class Action(webapp.RequestHandler):
	def get(self):
		global game, players, error
		
		gameId = self.request.get('game')
		actionStr = self.request.get('a')
		arg = self.request.get('arg')
		arg2 = self.request.get('arg2')
		try:
			action = int(actionStr)
			arg = int(arg)
			arg2 = int(arg2)
		except:
			nothing = 1

		game = db.get(db.Key(gameId))
		playersQuery = game.player_set
		playersQuery.order('position')
		players = playersQuery.fetch(100)
		
		positionType = GetPositionType(arg)
		positionType2 = GetPositionType(arg2)
		
		if len(game.boardTokens) == 95:
			game.boardTokens += [-1]*(6*5)

		error = ''
		if not users.get_current_user():
			error = 'You must log in first'
		elif game.phase != Phase_WAITING_FOR_PLAYERS and players[game.turn].user != users.get_current_user() and action != 107:
			error = 'It\'s not your turn'
		else:
			if action == 107: # chat
				text = self.request.get('t')
				ChatHistoryUser(users.get_current_user(), text, ': ')
#				if game.phase == Phase_WAITING_FOR_PLAYERS:
#					ChatHistoryUser(users.get_current_user(), text, ': ')
#				elif IsUserInGame():
#					ChatHistory(players[GetUserPosition()], text, ': ')
#				else:
#					ChatHistoryUser(users.get_current_user(), text, ': ')
				PutGame()
			if game.phase == Phase_WAITING_FOR_PLAYERS:
				if action == 103: # join game
					JoinGame(db.Key(gameId))
				elif action == 105: # remove user
					if IsUserInGame():
						deleteKey = db.Key(arg)
						removed = False
						for player in players:
							if player.key() == deleteKey:
								removed = True
								player.delete()
						if removed and len(players)==1:
							game.delete()
						else:
							PutGame()
					else:
						error = 'That user isn\'t in the game'
				elif action == 106: # change game name
					if IsUserInGame():
						game.name = arg
						PutGame()
				elif action == 104: # start game
					if IsUserInGame():
						numPlayers = len(players)
						if numPlayers in [1,2,3,4,5]:
							firstPlayer = random.randint(0, numPlayers-1)
							playerPositions = range(numPlayers)
							random.shuffle(playerPositions)
							for i in range(numPlayers):
								players[i].position = playerPositions[i]
								players[i].put()
							game.numPlayers = numPlayers
							game.firstPlayer = firstPlayer
							game.turn = firstPlayer
							game.phase = Phase_BUILD
							game.playerPassed = [False]*numPlayers
							PutGame()
					else:
						error = 'Can\'t start a game that you\'re not in'
			elif action == 8: # build
				if game.phase != Phase_BUILD:
					error = 'Not in the build phase'
				else:
					if CanBuild(arg):
						players[game.turn].buildings.append(arg)
						players[game.turn].buildingsOccupied.append(False)
						players[game.turn].tokenCounts[0] += buildings[arg]['points'][0]
						players[game.turn].tokenCounts[1] += buildings[arg]['points'][1]
						players[game.turn].tokenCounts[2] += buildings[arg]['points'][2]
						players[game.turn].tokenCounts[3] += buildings[arg]['points'][3]
						players[game.turn].tokenCounts[8] += buildings[arg]['points'][4]
						game.remainingBuildings[arg] -= 1
						ChatHistory(players[game.turn], 'built a ' + buildings[arg]['name'])
						players[game.turn].put()
						AdvanceTurn()
						PutGame()
			else:
				if game.phase == Phase_ACTION:
					ResetHighlight()

					if action == 100: # pass
						if PlayerHasValidCards(game.turn):
							game.playerPassed[game.turn] = True
							ChatHistory(players[game.turn], 'passed')
							AdvanceTurn()
							PutGame()
						else:
							error = 'You have too many cards. Choose a card to discard.'

					if action == 102: # discard
						if positionType == Position_CARD:
							success = Discard(game.turn, arg - 200)
							if success:
								players[game.turn].put()
								AutoPass()
								PutGame()
							else:
								error = 'Unable to discard'

					elif action>=0 and action<=7: # activate building
						if not players[game.turn].buildingsOccupied[action] or cheatOccupied:
							building = players[game.turn].buildings[action]
							success = False
							
							if action == arg-100: # do no action
								if players[game.turn].colonists>=1 or cheatColonists:
									success = True
								else:
									error = 'Not enough colonists'
							
							elif building == 0: # colonize
								if positionType == Position_OCCUPY:
									if players[game.turn].colonists>=2 or cheatColonists:
										success = Occupy(arg)
									else:
										error = 'Not enough colonists'
								
							elif building == 2: # ship
								if players[game.turn].colonists>=2 or cheatColonists:
									if positionType == Position_SHIP:
										success = Ship(arg)
								else:
									error = 'Not enough colonists'

							elif building == 3: # draw
								if players[game.turn].colonists>=1 or cheatColonists:
									if positionType == Position_CARD:
										success = Draw(arg - 200)
								else:
									error = 'Not enough colonists'
							
							elif building == 6: # ship/draw
								if positionType == Position_SHIP:
									if players[game.turn].colonists>=2 or cheatColonists:
										success = Ship(arg)
									else:
										error = 'Not enough colonists'
								elif positionType == Position_CARD:
									if players[game.turn].colonists>=1 or cheatColonists:
										success = Draw(arg - 200)
									else:
										error = 'Not enough colonists'
								
							elif building == 4: # attack
								if players[game.turn].colonists>=3 or cheatColonists:
									if positionType == Position_ATTACK:
										success = Attack(arg)
								else:
									error = 'Not enough colonists'

							elif building == 8: # occupy/attack
								if positionType == Position_ATTACK:
									if players[game.turn].colonists>=3 or cheatColonists:
										success = Attack(arg)
									else:
										error = 'Not enough colonists'
								elif positionType == Position_OCCUPY:
									if players[game.turn].colonists>=2 or cheatColonists:
										success = Occupy(arg)
									else:
										error = 'Not enough colonists'

							elif building == 9: # occupy+ship
								if positionType == Position_SHIP:
									if players[game.turn].colonists>=2 or cheatColonists:
										success = Ship(arg)
										if positionType2 == Position_OCCUPY:
											if players[game.turn].colonists>=2 or cheatColonists:
												success = Occupy(arg2) or success
											else:
												error = 'Not enough colonists'
									else:
										error = 'Not enough colonists'
								elif positionType == Position_OCCUPY:
									if players[game.turn].colonists>=2 or cheatColonists:
										success = Occupy(arg)
										if positionType2 == Position_SHIP:
											if players[game.turn].colonists>=2 or cheatColonists:
												success = Ship(arg2) or success
											else:
												error = 'Not enough colonists'
									else:
										error = 'Not enough colonists'

							elif building == 11: # draw+draw
								if players[game.turn].colonists>=1 or cheatColonists:
									if positionType == Position_CARD:
										success = Draw(arg - 200)
										if positionType2 == Position_CARD:
											if players[game.turn].colonists>=1 or cheatColonists:
												success = Draw(arg2 - 200) or success
											else:
												error = 'Not enough colonists'
								else:
									error = 'Not enough colonists'

							elif building == 12: # ship+ship
								if players[game.turn].colonists>=2 or cheatColonists:
									if positionType == Position_SHIP:
										success = Ship(arg)
										if positionType2 == Position_SHIP:
											if players[game.turn].colonists>=2 or cheatColonists:
												success = Ship(arg2) or success
											else:
												error = 'Not enough colonists'
								else:
									error = 'Not enough colonists'

							elif building in [13,14,15]: # pay
								if players[game.turn].colonists>=1 or cheatColonists:
									if positionType == Position_BUILDING:
										success = Pay(arg - 100)
									else:
										error = 'Attempting to pay a non-building'
								else:
									error = 'Not enough colonists'

							if success:
								players[game.turn].buildingsOccupied[action] = True
								players[game.turn].colonists -= 1
								players[game.turn].put()
								AdvanceTurn()
								PutGame()
						else:
							error = 'That building is already occupied'
				
					elif action>=9 and action<=12: # use a token
						if players[game.turn].tokenCounts[action-5] <= 0:
							error = 'You don\'t have any of that token'
						else:
							success = False
							if action == 9: # ship/draw
								if positionType == Position_SHIP:
									if players[game.turn].colonists>=1 or cheatColonists:
										success = Ship(arg)
									else:
										error = 'Not enough colonists'
								elif positionType == Position_CARD:
									if players[game.turn].colonists>=0 or cheatColonists:
										success = Draw(arg - 200)
									else:
										error = 'Not enough colonists'
							if action == 10: # occupy/draw
								if positionType == Position_OCCUPY:
									if players[game.turn].colonists>=1 or cheatColonists:
										success = Occupy(arg)
									else:
										error = 'Not enough colonists'
								elif positionType == Position_CARD:
									if players[game.turn].colonists>=0 or cheatColonists:
										success = Draw(arg - 200)
									else:
										error = 'Not enough colonists'
							if action == 11: # attack
								if positionType == Position_ATTACK:
									if players[game.turn].colonists>=2 or cheatColonists:
										success = Attack(arg)
									else:
										error = 'Not enough colonists'
							if action == 12: # pay
								if positionType == Position_BUILDING:
									if players[game.turn].colonists>=0 or cheatColonists:
										success = Pay(arg - 100)
									else:
										error = 'Not enough colonists'
						
							if success:
								players[game.turn].tokenCounts[action-5] -= 1
								players[game.turn].put()
								AdvanceTurn()
								PutGame()

				if game.phase == Phase_PAY:
					if action == 101: # pay
						success = Pay(arg - 100)
						if success:
							players[game.turn].paysLeft -= 1
							players[game.turn].put()
							if players[game.turn].paysLeft <= 0:
								AdvanceTurn()
							PutGame()
					else:
						error = 'Click on a building to pay'

		url = '/?game=' + str(gameId)
		if error:
			url = url + '&e=' + error
		if self.request.get('ajax'):
			url = url + '&ajax=' + self.request.get('ajax')
		self.redirect(url)
		
def getRandomBoardTokens():
	boardTokens = [0]*17 + [1]*20 + [2]*17 + [3]*25 + [4]*6 + [5]*6 + [6]*2 + [7]*2
	random.shuffle(boardTokens)
	return boardTokens

class NewGame(webapp.RequestHandler):
	def get(self):
		global game
		if users.get_current_user():
			game = Game(
				boardTokens=getRandomBoardTokens() + [-1]*(6*5),
				phase=Phase_WAITING_FOR_PLAYERS,
				remainingBuildings=[0,5,5,5,4,4,4,3,3,3,2,2,2,1,1,1],
				remainingCards=[
					True,True,True,True,True,True,
					True,True,True,True,True,True,
					True,True,True,True,True,True,
					True,True,True,True,True,True,
					True,True,True,True,True,True,
					True,True,True,True,True,True,
					True,True,True,True,True,True,
					True,True,True,True,True,True,
				],
				name=users.get_current_user().nickname() + '\'s game',
				timeCreated = datetime.datetime.now(),
				step=0,
			)
			gameId = game.put()
			JoinGame(gameId)
#			gameGlobal = Global.get_or_insert('1')
			self.redirect('/?game=' + str(gameId))
		else:
			self.redirect('/gamelist')

def IsUserInGame():
	global players
	
	for player in players:
		if users.get_current_user() == player.user:
			return True
	return False
	
def GetUserPosition():
	global game, players
	for player in players:
		if users.get_current_user() == player.user:
			return player.position
	return -1
	
def ChatHistory(player, text, separator=' '):
	global game
	css = ''
	if player.position == 1:
		css = 'background-color:black;'
	timeStamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
	game.chatHistory.append('[' + timeStamp + ' UTC] <span style=\'color: ' + playerColors[player.position]['name'] + '; ' + css + '\'>' + player.user.nickname() + '</span>' + separator + cgi.escape(text))

def ChatHistoryUser(user, text, separator=' '):
	global game
	timeStamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
	game.chatHistory.append('[' + timeStamp + ' UTC] <span style=\'color: black\'>' + user.nickname() + '</span>' + separator + cgi.escape(text))

class GameList(webapp.RequestHandler):
	def get(self):
		if users.get_current_user():
			url = users.create_logout_url(self.request.uri)
			url_linktext = 'Logout ' + users.get_current_user().nickname()
		else:
			url = users.create_login_url(self.request.uri)
			url_linktext = 'Login'
			
		games = db.GqlQuery("SELECT * from Game WHERE phase=3 ORDER BY timeCreated DESC").fetch(30)#" ORDER BY timeCreated")
		gamesInProgress = db.GqlQuery("SELECT * from Game WHERE phase in (0,1,2) ORDER BY timeCreated DESC").fetch(30)
		gamesFinished = db.GqlQuery("SELECT * from Game WHERE phase=4 ORDER BY timeCreated DESC").fetch(30)#" ORDER BY timeCreated")
		
#		myPlayers = db.GqlQuery("SELECT * from Player WHERE user=:1 AND timeCreated=NULL", users.get_current_user()).fetch(100)
#		myPlayers = db.GqlQuery("SELECT * from Player WHERE user=:1 ORDER BY timeCreated DESC", users.get_current_user()).fetch(100)
		myPlayers = db.GqlQuery("SELECT * from Player WHERE user=:1", users.get_current_user()).fetch(100)
		myGames = []
		for player in myPlayers:
			if player.game.phase in (0,1,2,3):
				exists = False
				for game in myGames:
					if game.key() == player.game.key():
						exists = True
				if not exists:
					myGames.append(player.game)

		myGames = sorted(myGames, key=lambda game: game.timeCreated, reverse=True)
		

#		myGames = []
#		allGames = db.GqlQuery("SELECT * from Game WHERE phase in (0,1,2,3) ORDER BY timeCreated DESC").fetch(1000)
#		for game in allGames:
#			playersQuery = game.player_set
#			players = playersQuery.fetch(10)
#			isInGame = False
#			for player in players:
#				if player.user == users.get_current_user():
#					isInGame = True
#			if isInGame:
#				myGames.append(game)
		
		template_values = {
			'url': url,
			'url_linktext': url_linktext,
			'games': games,
			'gamesInProgress': gamesInProgress,
			'gamesFinished': gamesFinished,
			'myGames': myGames,
			'user': users.get_current_user(),
		}

		path = os.path.join(os.path.dirname(__file__), 'gamelist.html')
		self.response.out.write(template.render(path, template_values))

application = webapp.WSGIApplication(
                                     [('/', MainPage),
                                      ('/gamelist', GameList),
                                      ('/action', Action),
                                      ('/newgame', NewGame)],
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()