import PyPDF2

def getText(filename):
    pdfFileObj = open(filename, 'rb')
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
    num_pages = pdfReader.numPages
    count = 0
    text = ""
    while count < num_pages:
        pageObj = pdfReader.getPage(count)
        count += 1
        try:
            text += str(pageObj.extractText().encode('utf8'))
        except:
            print("Non searchable PDF!")

    return text

# #For testing only
# output = getText("C:\\Users\\Indranil Chandra\\Desktop\\Shipmnts\\Shipmnts-Challenge\\res\\data\\AICST-dataset\\MF\\test_files\\117586-[Untitled]_303520171013155622-Page(2).pdf")
# print(output)