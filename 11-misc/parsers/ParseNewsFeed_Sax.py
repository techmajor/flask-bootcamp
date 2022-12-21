from xml.sax import parse
from xml.sax.handler import ContentHandler
import json

class SVGHandler(ContentHandler):

    def __init__(self):
        super().__init__()
        self.element_stack = []

    @property
    def current_element(self):
        return self.element_stack[-1]

    def startElement(self, name, attrs):
        print("start element: " + name)
        print ("Stack" , str(self.element_stack))
        self.element_stack.append({
            "name": name,
            "attributes": dict(attrs),
            "children": [],
            "value": ""
        })
       
    def endElement(self, name):
        print("end element: \n\n" + name)
        #print("Current element: " , str(self.current_element))
        clean(self.current_element)
        print ("Stack" , str(self.element_stack))
        if len(self.element_stack) > 1:
            child = self.element_stack.pop()
            self.current_element["children"].append(child)
        

    def characters(self, content):
        self.current_element["value"] += content
        if content.strip() != "":
            print(repr(content))


def clean(element):
    element["value"] = element["value"].strip()
    for key in ("attributes", "children", "value"):
        if not element[key]:
            del element[key]
    

def main():
    handler = SVGHandler()
    parse("PersonData.xml", handler)
    root = handler.current_element
    print(json.dumps(root, indent=4))      

if __name__ == "__main__":
  
    # calling main function
    main()

