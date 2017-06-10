import tweepy
import requests
import json
import urllib.request
import time
import datetime
import os
import logging
import random
from secret import *

# Basic Logging configuration
logging.basicConfig(filename="twitterBot.log", level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# using default logger name
logger = logging.getLogger(__name__)

# list of xkcd comics already twitted from the list of tech related xkcds
already_twitted = []


# Returns a twitter api object using tweepy
def twitterAuth():
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    return api


# fetch url json data from xkcd.com
def getComic(url):
    print("Fetching " + url)
    resp = requests.get(url)

    if resp.status_code == 200:
        data = json.loads(resp.text)
        imgLink = data['img']
        imgTitle = data['title']
        imgDescription = data['alt']
        imgNum = data['num']
        return [imgLink, imgTitle, imgDescription, imgNum]

    logger.error("Status code !== 200")
    return [None, None, None, None]


# if xkcd_num is -1 then fetch latest comic else fetch comic specified by xkcd_nums
def getComicUrl(xkcd_num):
    if xkcd_num == -1:
        logger.warn("List Exhausted")
        url = "http://xkcd.com/info.0.json"
        logger.info("Fetching latest comic...")
        return getComic(url)

    url = "http://xkcd.com/" + str(xkcd_num) + "/info.0.json"
    logger.info("Fetching comic from list")
    return getComic(url)


# tweet the text
def tweetStatus(text):
    api = twitterAuth()
    try:
        api.update_status(text)
    except tweepy.error.TweepError as e:
        logger.error(e.message, exc_info=True)
    else:
        logger.info("Status Updated " + text)


# choose a random xkcd number from the array and update the already_twitted list
def randomXKCD():
    programming_nums = [5, 10, 12, 19, 26, 28, 54, 55, 62, 68, 74, 77, 85, 86, 88, 89, 94, 95, 112, 113, 114, 117, 128, 134, 135, 144, 149, 153, 156, 163, 173, 177, 178, 179, 181, 183, 184, 195, 196, 199, 207, 208, 215, 216, 217, 221, 224, 225, 230, 234, 243, 246, 247, 250, 251, 256, 262, 263, 272, 274, 278, 286, 287, 289, 292, 297, 303, 312, 314, 323, 327, 329, 340, 341, 342, 343, 344, 345, 349, 352, 353, 356, 364, 370, 371, 375, 376, 378, 379, 380, 385, 386, 394, 399, 403, 407, 409, 410, 413, 416, 424, 434, 435, 438, 442, 447, 456, 463, 466, 467, 468, 482, 487, 494, 495, 504, 505, 512, 518, 519, 521, 522, 528, 530, 533, 534, 538, 539, 553, 554, 561, 563, 565, 568, 569, 573, 587, 589, 591, 593, 597, 599, 601, 602, 607, 609, 612, 619, 621, 622, 624, 626, 635, 643, 644, 645, 648, 658, 664, 672, 676, 686, 687, 688, 695, 701, 703, 704, 710, 713, 718, 721, 722, 726, 727, 741, 743, 754, 759, 763, 773, 775, 797, 801, 802, 804, 806, 809, 816, 824, 832, 833, 834, 837, 838, 844, 849, 855, 858, 859, 862, 866, 868, 869, 870, 872, 881, 893, 894, 896, 899, 900, 903, 904, 910, 912, 925, 932, 934, 936, 937, 940,
                        946, 947, 948, 949, 953, 958, 963, 979, 981, 982, 985, 992, 1000, 1017, 1024, 1031, 1033, 1039, 1046, 1047, 1048, 1050, 1052, 1053, 1056, 1058, 1077, 1081, 1083, 1084, 1090, 1118, 1121, 1131, 1132, 1134, 1137, 1143, 1155, 1159, 1161, 1162, 1163, 1168, 1171, 1172, 1174, 1179, 1180, 1181, 1184, 1185, 1188, 1197, 1200, 1201, 1205, 1213, 1223, 1224, 1226, 1229, 1230, 1234, 1236, 1238, 1247, 1250, 1252, 1258, 1263, 1266, 1269, 1270, 1275, 1276, 1277, 1279, 1286, 1292, 1296, 1299, 1305, 1306, 1309, 1310, 1312, 1313, 1316, 1323, 1328, 1332, 1333, 1334, 1337, 1341, 1344, 1348, 1349, 1350, 1353, 1354, 1361, 1367, 1370, 1374, 1381, 1399, 1401, 1406, 1411, 1421, 1434, 1439, 1446, 1450, 1454, 1479, 1481, 1495, 1504, 1506, 1508, 1513, 1516, 1527, 1537, 1553, 1570, 1571, 1573, 1574, 1576, 1579, 1582, 1586, 1597, 1605, 1608, 1613, 1619, 1626, 1627, 1629, 1630, 1631, 1636, 1638, 1646, 1654, 1667, 1668, 1671, 1683, 1685, 1690, 1692, 1695, 1696, 1700, 1718, 1722, 1724, 1725, 1727, 1728, 1732, 1737, 1739, 1742, 1755, 1760, 1764, 1765, 1773, 1779, 1782, 1785, 1790, 1805, 1806, 1808, 1817, 1820, 1822, 1823, 1831]

    if len(already_twitted) == len(programming_nums):
        return -1

    num = random.choice(programming_nums)

    while num in already_twitted:
        num = random.choice(programming_nums)
        continue

    already_twitted.append(num)

    return num


# tweet with title and image
def tweetXKCD(file, title):
    api = twitterAuth()
    try:
        api.update_with_media(file, status=title)
    except tweepy.error.TweepError as e:
        logger.error(e.message, exc_info=True)
    else:
        logger.info("XKCD tweeted")


# pause the program for one week
def waitForOneWeek():
    OneWeek = datetime.datetime.replace(datetime.datetime.now(
    ) + datetime.timedelta(days=7))

    delta = OneWeek - datetime.datetime.now()
    print(delta.seconds * 7)
    time.sleep(delta.seconds)


if __name__ == "__main__":
    while True:
        xkcd_num = randomXKCD()
        [imgLink, imgTitle, imgDescription, imgNum] = getComicUrl(xkcd_num)

        if imgLink is not None:
            filename = imgTitle + ".png"
            status = imgTitle + " #" + str(imgNum) + " #xkcd"
            urllib.request.urlretrieve(imgLink, filename=filename)
            tweetXKCD(filename, status)
            os.remove(filename)
            waitForOneWeek()
