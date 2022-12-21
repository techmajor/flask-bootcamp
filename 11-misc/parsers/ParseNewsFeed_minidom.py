from logging import getLevelName
import requests
from xml.dom import minidom

def loadRSS(xml_filename):
    # url of rss feed
    url = 'https://timesofindia.indiatimes.com/rssfeeds/-2128833038.cms'
    #url = 'http://site.api.espn.com/apis/site/v2/sports/football/college-football/news'
  
    # creating HTTP response object from given url
    resp = requests.get(url)
  
    # saving the xml file
    with open(xml_filename, 'wb') as f:
        f.write(resp.content)


def parse_xml(xml_filename):
    doc = minidom.parse(xml_filename)
    return doc

def get_nodelist(doc):
    items = doc.getElementsByTagName("record")
    for item in items:
        title = item.getElementsByTagName("text")[0]
        ilink = item.getElementsByTagName("name")[0]
        pubDate = item.getElementsByTagName("numberrange")[0]

        print (title.firstChild.data)
        print (ilink.firstChild.data)
        print (pubDate.firstChild.data)

        print (len(title.childNodes))

        for textNodes in title.childNodes:
            print (textNodes.data)
  
def main():
    xml_filename = "name_number_data.xml"
    #loadRSS(xml_filename)
    doc = parse_xml(xml_filename)
    get_nodelist(doc)

if __name__ == "__main__":
  
    # calling main function
    main()  