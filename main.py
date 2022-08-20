import pandas as pd
import re

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
        self.temp = []
        i = 1
        while True:
            self.temp.append(self.receipt.iloc[i, 8])
            i += 1
            # Next regex look for this structure (CO.REG: xxxx ). It considers several cases should
            # the characters are not properly recognized. It would be useful to have more receipts
            # to find different kinds of common errors.
            if re.search(r'^\(CO.REG.+\)|^\(CO|R.G.*:|C.+EG', self.receipt.iloc[i, 8]) or i>5:
                break

        #print(re.search(r'C.+FG', self.receipt.iloc[2, 8]))
        self.company=' '.join(self.temp)
        return self.company


def run():
    receipt_1 = TwyReceipt("./ocr_files/OCR1.txt")
    receipt_2 = TwyReceipt("./ocr_files/OCR2.txt")
    receipt_3 = TwyReceipt("./ocr_files/OCR1mod.txt")

    print(receipt_1.get_company())
    print(receipt_2.get_company())
    print(receipt_3.get_company())


if __name__ == '__main__':
    run()
