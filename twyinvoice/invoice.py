import pandas as pd
import re
import json

import twyinvoice.twyinvoiceregex as twyinvoiceregex


class TwyInvoice(object):

    def __init__(self, ocr_file):
        """
        Loads the csv data
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
            if re.search(twyinvoiceregex.rgx_coreg, self.receipt.iloc[i, 8]) or i > 5:
                break
        self.company = ' '.join(complst)

    def extract_address(self):
        addrlst = []
        i = 1
        while re.search(twyinvoiceregex.rgx_coreg, self.receipt.iloc[i, 8]) is None and i < 5:
            i += 1
        i += 1
        while True:
            addrlst.append(self.receipt.iloc[i, 8])
            i += 1
            if re.search(twyinvoiceregex.rgx_invoice, self.receipt.iloc[i, 8]) or i > 14:
                break
        self.address = ' '.join(addrlst)

    def extract_total(self):
        i = self.receipt[self.receipt['text'].str.match(twyinvoiceregex.rgx_totr)].index.values + 1
        self.tot_round = self.receipt.iloc[i, 8].str.split(expand=True).iloc[0, 1]

    def extract_date(self):
        # Alternative method:
        #i = self.receipt[self.receipt['text'].str.match(rgx_change)].index.values+2
        #self.date = self.receipt.iloc[i, 8].str.split(expand=True).iloc[0, 0]
        self.date = self.receipt.loc[self.receipt['text'].str.match(twyinvoiceregex.rgx_date),
                                     'text'].item().split()[0]

    def extract_items(self):
        #Regex a item
        self.n_line_items = int(self.receipt.loc[self.receipt['text'].str.match(twyinvoiceregex.rgx_item), 'text'].item().split()[-1])

        i = 3
        while re.search(twyinvoiceregex.rgx_invoice, self.receipt.iloc[i, 8]) is None and i < 15:
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

    def get_json(self, json_name):
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
