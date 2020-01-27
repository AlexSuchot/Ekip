import PyPDF2
import hashlib

pdfFileObj = open('Livre_Maupassant.pdf', 'rb')
pdfReader = PyPDF2.PdfFileReader(pdfFileObj)

count = 0
block = ''
decount = pdfReader.numPages

# Le numéro du bloc :
blockNumber = 1


class Bloc:
    def __init__(self, number, sha256, pagesText, contributorUUID, proofOfWork):
        self.number = number
        self.sha256 = sha256
        self.pagesText = pagesText
        self.contributorUUID = contributorUUID
        self.proofOfWork = proofOfWork


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

        newBloc = Bloc(blockNumber, m.hexdigest(), block, 'contributorUUID', 'proofOfWork')

        blockNumber += blockNumber

    elif count < 5:
        print(text)
