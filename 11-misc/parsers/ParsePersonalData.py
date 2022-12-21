import xml.etree.ElementTree as ET

# with open("MessageInfo.xml") as xml_file: 
#     element_tree.parse(xml_file)

# for event, element in element_tree.iterparse("MessageInfo.xml"):
#     print (event +  "\t" + element.tag)

doc_tree = ET.parse("PersonData.xml")
root_elem = doc_tree.getroot()

print ("Iter: 1")
for item in root_elem.iter():
    print (item.tag + "\t" + item.text)

# print ("Iter:2")
# for p in root_elem.findall('person'):
#     print (p.tag)
#     print (p.attrib)
#     print (p.text)

print ("\nIter:3")
for person in root_elem:
    print (person.tag)
    print (person.attrib)
    for name in person.findall('name'):
        print (name)
        print ("Iterating over an element")
        for entries in name.iter():
            print (entries.tag + "\t" + entries.text)

# print ("Iter:4")
# for item in root_elem.iter('name'):
#     print (item.tag + "\t" + item.text)