import PyPDF2
from fpdf import FPDF
   
# creating a pdf file object
pdfFileObj = open('Grade8_Slokas.pdf', 'rb')
   
# creating a pdf reader object
pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
   
# printing number of pages in pdf file
print(pdfReader.numPages)
   
# creating a page object
pageObj = pdfReader.getPage(0)
   
# extracting text from page
print(pageObj.extractText())
   
# closing the pdf file object
pdfFileObj.close()

# save FPDF() class into a
# variable pdf
pdf = FPDF()
 
# Add a page
pdf.add_page()
 
# set style and size of font
# that you want in the pdf
pdf.set_font("Arial", size = 15)
 
# create a cell
pdf.cell(200, 10, txt = "File formats in Python",
         ln = 1, align = 'L')
 
# add another cell
pdf.cell(200, 10, txt = "Python Training.",
         ln = 2, align = 'L')
 
# save the pdf with name .pdf
pdf.output("textopdfpy.pdf")  