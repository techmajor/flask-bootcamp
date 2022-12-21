from xml.dom import minidom as md
 
doc = md.parse("topnewsfeed.xml")
 
titles = doc.getElementsByTagName("title")
 
for title in titles:
    print(title.firstChild.nodeValue)