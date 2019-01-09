from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import StringIO

class PdfConverter:

   def __init__(self, file_path):
       self.file_path = file_path
# convert pdf file to a string which has space among words
   def convert_pdf_to_txt(self):
       rsrcmgr = PDFResourceManager()
       retstr = StringIO()
       codec = 'utf-8'  # 'utf16','utf-8'
       laparams = LAParams()
       device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
       fp = open(self.file_path, 'rb')
       interpreter = PDFPageInterpreter(rsrcmgr, device)
       password = ""
       maxpages = 0
       caching = True
       pagenos = set()
       for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password, caching=caching, check_extractable=True):
           interpreter.process_page(page)
       fp.close()
       device.close()
       str = retstr.getvalue()
       retstr.close()
       return str
# convert pdf file text to string and save as a text_pdf.txt file
   def save_convert_pdf_to_txt(self):
       content = self.convert_pdf_to_txt()
       txt_pdf = open('text_pdf.txt', 'wb')
       txt_pdf.write(content.encode('utf-8'))
       txt_pdf.close()
if __name__ == '__main__':
    # filepath = "C:/Users/HP/Downloads/Shipmnts-Challenge-master/res/data/AICST-dataset/MF/MAWB/117540-232-67215820_160620171011155112-Page(1).pdf"
    filepath = "C:/Users/HP/Downloads/Shipmnts-Challenge-master/res/data/AICST-dataset/MF/MAWB/118550-Email Copy - 098-77477411_229720171202101200-Page(2).pdf"
    pdfConverter = PdfConverter(file_path='1.pdf')
    print(pdfConverter.save_convert_pdf_to_txt())