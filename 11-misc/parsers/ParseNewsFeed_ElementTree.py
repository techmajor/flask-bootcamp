import xml.etree.ElementTree as ET
import csv
import requests

def loadRSS():
    # url of rss feed
    url = 'https://timesofindia.indiatimes.com/rssfeeds/-2128833038.cms'
  
    # creating HTTP response object from given url
    resp = requests.get(url)
  
    # saving the xml file
    with open('topnewsfeed.xml', 'wb') as f:
        f.write(resp.content)


def parse_xml(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()
    print (root.tag)
    return root

def parse_xml_fromstring():
    elem = ET.fromstring("""<?xml version="1.0" encoding="UTF-8"?><rss xmlns:atom="http://www.w3.org/2005/Atom" version="2.0"><channel><title>Bangalore News: Latest Bangalore News Headlines &amp; Live News Updates from Bangalore - Times of India</title><link>https://timesofindia.indiatimes.com/articlelist/-2128833038.cms</link><description>Bangalore news live: TOI brings the latest Bangalore news headlines about Bangalore crime, Bangalore education news, Bangalore real estate news, Bangalore politics and Live Updates on local Bangalore news from Times of India</description><language>en-gb</language><lastBuildDate>2022-12-13T11:35:12+05:30</lastBuildDate><atom:link type="application/rss+xml" rel="self" href="https://timesofindia.indiatimes.com/rssfeeds/-2128833038.cms"/><copyright>Copyright:(C) Tue, 13 Dec 2022 11:35:12 IST Bennett Coleman &amp; Co. Ltd, http://in.indiatimes.com/policyterms/1554651.cms</copyright><docs>http://syndication.indiatimes.com/</docs><image><title>Bangalore News: Latest Bangalore News Headlines &amp; Live News Updates from Bangalore - Times of India</title><url>https://timesofindia.indiatimes.com/photo/507610.cms</url><link>https://timesofindia.indiatimes.com/articlelist/-2128833038.cms</link></image><item><title>Yelahanka sees highest fatal road accidents in B'luru</title><description>&lt;img border="0" hspace="10" align="left" style="margin-top:3px;margin-right:5px;" src="https://timesofindia.indiatimes.com/photo/96183783.cms" /&gt; Fatalities due to road accidents continue to be the highest in Yelahanka. While 52 road fatalities were reported in the police station limits in 2021, the number stood at 40 in the first 10 months of this year.</description><link>https://timesofindia.indiatimes.com/city/bengaluru/yelahanka-sees-highest-fatal-road-accidents-in-bengaluru/articleshow/96183783.cms</link><guid>https://timesofindia.indiatimes.com/city/bengaluru/yelahanka-sees-highest-fatal-road-accidents-in-bengaluru/articleshow/96183783.cms</guid><pubDate>2022-12-13T04:50:54+05:30</pubDate></item></channel></rss>""")
    print (elem.tag)
    return elem

#Non-Incremental parsing
#Parse and Iterate using iterator method
def parse_xml_iterparse(xml_file):
    for element in ET.iterparse(xml_file):
        print (element)

def iterate_itermethod(elem_tree):
    for elem in elem_tree.iter():
        print (elem)

#Iterate specific nodes using findall
def iterate_findall(elem_tree):
    print (len(elem_tree[0]))
    for childNodes in elem_tree[0]:
        for elem in childNodes.findall('title'):
            #print (elem)
            for news_item in elem.iter():
                print(news_item.tag + "\t" + news_item.text if(news_item.text != None) else "" )

#Use XMLPullParser

def main():

    xml_file = "topnewsfeed.xml"
    newsfeed_tree = parse_xml(xml_file)
    #newsfeed_tree = parse_xml_fromstring()
    iterate_itermethod(newsfeed_tree)
    #iterate_findall(newsfeed_tree)
    #parse_xml_iterparse(xml_file)

if __name__ == "__main__":
  
    # calling main function
    main()