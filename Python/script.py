import PyPDF2

pdfFileObj = open('Livre_Maupassant.pdf', 'rb')

pdfReader = PyPDF2.PdfFileReader(pdfFileObj)

# On parcours toutes les pages du livre et on affiche le texte :
for x in range(pdfReader.numPages):
    pageObj = pdfReader.getPage(x)
    print(pageObj.extractText())
    print('\n')
