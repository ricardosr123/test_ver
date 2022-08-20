import pandas as pd
import re
import json

# Next regex look for the structure "(CO.REG". It considers several cases:
# - With/without first parenthesis
# - Spaces between parenthesis and CO, and between C0 . and . Reg
rgx_coreg_base = '^\(?\s?CO\s?.?\s?REG'
# - Letters misspelled.
variations1 = '[A-Z0-9\(\)\[\]\{\}]'
rgx_coreg_lst = [''.join([rgx_coreg_base[0:i], variations1, rgx_coreg_base[i + 1:]]) for i in [7, 8, 17, 18, 19]]
rgx_coreg_lst.insert(0, '^\(CO.REG')  # "Perfect" pattern
# - Some additional cases selected at random
rgx_coreg_lst.append('^\(CO')
rgx_coreg_lst.append('R.G.*:')
rgx_coreg_lst.append('C.+EG')
rgx_coreg = 'r\'' + '|'.join(rgx_coreg_lst) + '\''

# Next regex look for the structure "-INVOICE-". It considers several cases:
# - With/without hyphens and possible misspelled letters
rgx_invoice_base = '-?INVOICE-?'
variations2 = '[A-Z0-9]'
rgx_invoice_lst = [''.join([rgx_invoice_base[0:i], variations2, rgx_invoice_base[i + 1:]]) for i in [2, 3, 4, 5, 6, 7, 8]]
rgx_invoice_lst.insert(0, '-INVOICE-')  # "Perfect" pattern
rgx_invoice = 'r\'' + '|'.join(rgx_invoice_lst) + '\''

# Next regex look for the structure  "TOTAL ROUNDED"
rgx_totr_base = 'TOTAL\s?\s?ROUNDED'
rgx_totr_lst = [''.join([rgx_totr_base[0:i], variations2, rgx_totr_base[i + 1:]]) for i in [0, 1, 2, 3, 4, 11, 12, 13, 14, 15, 16, 17]]
rgx_totr_lst.insert(0, 'TOTAL\sROUNDED')  # "Perfect" pattern
rgx_totr = 'r\'' + '|'.join(rgx_totr_lst) + '\''

# rgx_change = r'CHANGE'
rgx_date = r'[0-3][0-9]\s?-\s?[01][0-9]\s?-\s?[0-9][0-9]'

rgx_item = r'ITEM\s?\(\s?S\s?\)'

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

    def extract_company(self):
        complst = []
        i = 1
        while True:
            complst.append(self.receipt.iloc[i, 8])
            i += 1
            if re.search(rgx_coreg, self.receipt.iloc[i, 8]) or i > 5:
                break
        self.company = ' '.join(complst)

    def extract_address(self):
        addrlst = []
        i = 1
        while re.search(rgx_coreg, self.receipt.iloc[i, 8]) is None and i < 5:
            i += 1
        i += 1
        while True:
            addrlst.append(self.receipt.iloc[i, 8])
            i += 1
            if re.search(rgx_invoice, self.receipt.iloc[i, 8]) or i > 14:
                break
        self.address = ' '.join(addrlst)

    def extract_total(self):
        i = self.receipt[self.receipt['text'].str.match(rgx_totr)].index.values + 1
        self.tot_round = self.receipt.iloc[i, 8].str.split(expand=True).iloc[0, 1]

    def extract_date(self):
        #Alternative method:
        #i = self.receipt[self.receipt['text'].str.match(rgx_change)].index.values+2
        #self.date = self.receipt.iloc[i, 8].str.split(expand=True).iloc[0, 0]
        self.date = self.receipt.loc[self.receipt['text'].str.match(rgx_date),
                                     'text'].item().split()[0]

    def extract_items(self):
        #Regex a item
        self.n_line_items = int(self.receipt.loc[self.receipt['text'].str.match(rgx_item), 'text'].item().split()[-1])

        i = 3
        while re.search(rgx_invoice, self.receipt.iloc[i, 8]) is None and i < 15:
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

    def get_json(self,json_name):
        self.extract_company()
        self.extract_date()
        self.extract_address()
        self.extract_items()
        self.extract_total()
        dictionary = {'company': self.company,
                      'date': self.date,
                      'address': self.address,
                      'line_items': self.line_items,
                      'total': self.tot_round}
        json_str = json.dumps(dictionary, indent=4)
        with open(json_name, "w") as outfile:
            outfile.write(json_str)

def run():
    receipt_1 = TwyReceipt("./ocr_files/OCR1.txt")
    receipt_2 = TwyReceipt("./ocr_files/OCR2.txt")
    receipt_3 = TwyReceipt("./ocr_files/OCR1mod.txt")

    receipt_1.get_json("./output/OCR1.json")
    receipt_2.get_json("./output/OCR2.json")
    receipt_3.get_json("./output/OCR1mod.json")


if __name__ == '__main__':
    run()
