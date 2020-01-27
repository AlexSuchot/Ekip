import PyPDF2
import hashlib

pdfFileObj = open('Livre_Maupassant.pdf', 'rb')
pdfReader = PyPDF2.PdfFileReader(pdfFileObj)

count = 0
block = ''
decount = pdfReader.numPages

# On parcours toutes les pages du livre et on affiche le texte :
for x in range(pdfReader.numPages):
    # Affiche une page :
    pageObj = pdfReader.getPage(x)
    text = pageObj.extractText() + '\n'
    block += text
    count += 1
    if count == 5:
        print(block)
        encodedBlock = block.encode('UTF-8')
        m = hashlib.sha256()
        m.update(encodedBlock)
        print(m.hexdigest())
        block = ''
        count = 0
        decount -= 5

    elif pdfReader.numPages - x <= 5:
        print(text)
