import requests
import csv
import xml.etree.ElementTree as ET

def loadRSS():
    # url of rss feed
    url = 'https://timesofindia.indiatimes.com/rssfeeds/-2128833038.cms'
  
    # creating HTTP response object from given url
    resp = requests.get(url)
  
    # saving the xml file
    with open('topnewsfeed.xml', 'wb') as f:
        f.write(resp.content)
          
  
def parseXML_ElementTree(xmlfile):
  
    # create element tree object
    tree = ET.parse(xmlfile)
  
    # get root element
    root = tree.getroot()
  
    # create empty list for news items
    newsitems = []
  
    #iterate news items using iterator method   
    for item in root.iter():
        print (item.tag)
        print (item.text)
        print (item.attrib)

    # iterate news items using findall
    for item in root.findall('./channel/item'):
  
        # empty news dictionary
        news = {}
        # iterate child elements of item
        for child in item:
            news[child.tag] = child.text.encode('utf8')
            #print (child.tag + "\t" + child.text) 
        # append news dictionary to news items list
        newsitems.append(news)
      
    # return news items list
    return newsitems
  
  
def savetoCSV(newsitems, filename):
  
    # specifying the fields for csv file
    fields = ['guid', 'title', 'pubDate', 'description', 'link', 'media']
  
    # writing to csv file
    with open(filename, 'w') as csvfile:
  
        # creating a csv dict writer object
        writer = csv.DictWriter(csvfile, fieldnames = fields)
  
        # writing headers (field names)
        writer.writeheader()
  
        # writing data rows
        writer.writerows(newsitems)
  
      
def main():
    # load rss from web to update existing xml file
    #loadRSS()
  
    # parse xml file
    newsitems = parseXML_ElementTree('topnewsfeed.xml')
  
    # store news items in a csv file
    #savetoCSV(newsitems, 'topnews.csv')
      
      
if __name__ == "__main__":
  
    # calling main function
    main()