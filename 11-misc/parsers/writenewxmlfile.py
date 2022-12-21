import xml.etree.ElementTree as ET
 
# This is the parent (root) tag
# onto which other tags would be
# created
data = ET.Element('grade')
 
# inside our root tag
element1 = ET.SubElement(data, 'person')
element2 = ET.SubElement(data, 'person')
 
# Adding subtags under the `Opening`
# subtag
s_elem1 = ET.SubElement(element1, 'name')
s_elem2 = ET.SubElement(element1, 'age')
s_elem3 = ET.SubElement(element2, 'name')
s_elem4 = ET.SubElement(element2, 'age')
 
# Adding attributes to the tags under
# `items`
element1.set('id', '1')
element2.set('id', '2')
 
# Adding text between the `E4` and `D5`
# subtag
s_elem1.text ="Surabhi"
s_elem2.text = "4"
s_elem3.text = "Saanvi"
s_elem4.text = "8" 

# Converting the xml data to byte object,
# for allowing flushing data to file
# stream
b_xml = ET.tostring(data)
tree = ET.ElementTree(data)
tree.write("NewData.xml", xml_declaration=True, encoding="UTF-8")
 
# Opening a file under the name `items2.xml`,
# with operation mode `wb` (write + binary)
# with open("GradeData.xml", "wb") as f:
#     f.write(b_xml)