from bs4 import BeautifulSoup as BS
import requests
from selenium import webdriver
import os
import sys

XENOCANTO = "www.xeno-canto.org/"
SEARCH_PAGE_XENOCANTO = "http://www.xeno-canto.org/explore?query="

def getLinks(keyword, numofpages):
    # Setup
    mainpage = SEARCH_PAGE_XENOCANTO + keyword
    s = requests.Session()
    res = s.get(mainpage)
    cookies = dict(res.cookies)
    r = s.get(mainpage, cookies=cookies)
    soup = BS(r.text, 'lxml')

    audioIDS = []
    for page in range(numofpages):
        # Get page url and every audio ID on it
        pageurl = mainpage + '&pg=' + str(page + 1)
        r_i = s.get(pageurl, cookies=cookies)
        soup_i = BS(r_i.text, 'lxml')
        soundTags = soup_i.findAll('div', attrs={'class':'xc-button-audio'})
        soundList = getAudioID(soundTags)
        audioIDS += soundList

    downloadLinks = []
    for audioID in audioIDS:
        print audioID
        downloadLinks.append(audioID)

    print len(downloadLinks), ' audios found.'
    return downloadLinks

def getAudioID(soundTags):
    links = []
    for tag in soundTags:
        audioID = tag.find('div', class_='jp-type-single')['data-xc-id']
        links.append(XENOCANTO + audioID)

    return links

def download(downloadLinks, keyword):
    # Setup
    chromeOptions = webdriver.ChromeOptions()
    prefs = {"download.default_directory" : os.getcwd()+'/data/xeno-canto/' + keyword}
    chromeOptions.add_experimental_option("prefs", prefs)
    driver = webdriver.Chrome(executable_path="chromedriver", chrome_options=chromeOptions)

    # Download each sound
    print "Downloading..."
    for filelink in downloadLinks:
        driver.get("http://" + filelink)
        driver.find_element_by_xpath("//img[@src='/static/img/download.png']").click()

if __name__ == "__main__":
    keyword = sys.argv[1]
    numofpages = int(sys.argv[2])
    download(getLinks(keyword, numofpages), keyword)
