import xml.etree.ElementTree as ET

# with open("MessageInfo.xml") as xml_file: 
#     element_tree.parse(xml_file)

# for event, element in element_tree.iterparse("MessageInfo.xml"):
#     print (event +  "\t" + element.tag)

doc_tree = ET.parse("PersonData.xml")
root_elem = doc_tree.getroot()

for item in root_elem.iter():
    print (item.tag + "\t" + item.text)
    

print (root_elem.findall(''))