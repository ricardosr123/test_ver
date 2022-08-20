import pandas as pd
import re

# Next regex look for the structure "(CO.REG". It considers several cases:
# - With/without first parenthesis
# - Spaces between parenthesis and CO, and between C0 . and . Reg
regex1base = '^\(?\s?CO\s?.?\s?REG'
# - Letters misspelled.
variations1 = '[A-Z0-9\(\)\[\]\{\}]'
regex1lst = [''.join([regex1base[0:i], variations1, regex1base[i + 1:]]) for i in [7, 8, 17, 18, 19]]
regex1lst.insert(0, '^\(CO.REG')  # "Perfect" pattern
# - Some additional cases selected at random
regex1lst.append('^\(CO')
regex1lst.append('R.G.*:')
regex1lst.append('C.+EG')
regex1 = 'r\''+'|'.join(regex1lst)+'\''

# Next regex look for the structure "-INVOICE-". It considers several cases:
# - With/without hyphens and possible misspelled letters
regex2base = '-?INVOICE-?'
variations2 = '[A-Z0-9]'
regex2lst = [''.join([regex2base[0:i], variations2, regex2base[i + 1:]]) for i in [2, 3, 4, 5, 6, 7, 8]]
regex2lst.insert(0, '-INVOICE-')  # "Perfect" pattern
regex2 = 'r\''+'|'.join(regex2lst)+'\''

# Next regex look for the structure  "TOTAL ROUNDED"
regex3base = 'TOTAL\s?\s?ROUNDED'
regex3lst = [''.join([regex3base[0:i], variations2, regex3base[i + 1:]]) for i in [0, 1, 2, 3, 4, 11, 12, 13, 14, 15, 16, 17]]
regex3lst.insert(0, 'TOTAL\sROUNDED')  # "Perfect" pattern
regex3 = 'r\''+'|'.join(regex3lst)+'\''

# regex4 = r'CHANGE'

class TwyReceipt(object):

    def __init__(self, ocr_file):
        """
        :param ocr_file: receipt ocr file location
        """
        def manual_separation(bad_line):
            """Split correctly lines where the text has commas"""
            correct_split = bad_line[0:8] + [",".join(bad_line[8:])]
            return correct_split
        self.receipt = pd.read_csv(ocr_file, names=['x1', 'y1', 'x2', 'y2', 'x3', 'y3', 'x4', 'y4', 'text'],
                                   engine="python", on_bad_lines=manual_separation)

    def get_company(self):
        complst = []
        i = 1
        while True:
            complst.append(self.receipt.iloc[i, 8])
            i += 1
            if re.search(regex1, self.receipt.iloc[i, 8]) or i > 5:
                break
        self.company = ' '.join(complst)
        return self.company

    def get_address(self):
        addrlst = []
        i = 1
        while re.search(regex1, self.receipt.iloc[i, 8]) is None and i < 5:
            i += 1
        i += 1
        while True:
            addrlst.append(self.receipt.iloc[i, 8])
            i += 1
            if re.search(regex2, self.receipt.iloc[i, 8]) or i > 14:
                break
        self.address = ' '.join(addrlst)
        return self.address

    def get_total(self):
        i = self.receipt[self.receipt['text'].str.match(regex3)].index.values+1
        self.tot_round = self.receipt.iloc[i, 8].str.split(expand=True).iloc[0, 1]
        return self.tot_round

    def get_date(self):
        #metodo de chequeo:
        #i = self.receipt[self.receipt['text'].str.match(regex4)].index.values+2
        #self.date = self.receipt.iloc[i, 8].str.split(expand=True).iloc[0, 0]
        self.date = self.receipt.loc[self.receipt['text'].str.match(r'[0-3][0-9]\s?-\s?[01][0-9]\s?-\s?[0-9][0-9]'),
                                     'text'].item().split()[0]
        return self.date

    def get_items(self):
        #Regex a item
        self.n_line_items = int(self.receipt.loc[self.receipt['text'].str.match(r'ITEM\s?\(\s?S\s?\)'), 'text'].item().split()[-1])

        i = 3
        while re.search(regex2, self.receipt.iloc[i, 8]) is None and i < 15:
            i += 1
        i += 3
        self.line_items = []
        for j in range(self.n_line_items):
            self.line_items.append(dict())
            self.line_items[j]['sku'] = self.receipt.iloc[i, 8]
            i += 1
            self.line_items[j]['quantity'] = self.receipt.iloc[i, 8]
            i += 2
            self.line_items[j]['price'] = self.receipt.iloc[i, 8]
            i += 1
            self.line_items[j]['total'] = self.receipt.iloc[i, 8]
            i += 3
            #get item
        print(self.line_items)
        return self.n_line_items

def run():
    receipt_1 = TwyReceipt("./ocr_files/OCR1.txt")
    receipt_2 = TwyReceipt("./ocr_files/OCR2.txt")
    receipt_3 = TwyReceipt("./ocr_files/OCR1mod.txt")

    receipt_1.get_items()
    receipt_2.get_items()
    receipt_3.get_items()


if __name__ == '__main__':
    run()
