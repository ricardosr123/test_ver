import pandas as pd
import re

# Next regex look for this structure "(CO.REG". It considers several cases:
# - With/without first parenthesis
# - Spaces between parenthesis and CO, and between C0 . and . Reg
regex1base = '^\(?\s?CO\s?.?\s?REG'
# - Characters misspelled.
variations = '[A-Z0-9\(\)\[\]\{\}]'
regex1lst = [''.join([regex1base[0:i], variations, regex1base[i + 1:]]) for i in [7, 8, 17, 18, 19]]
regex1lst.insert(0, '^\(CO.REG')  # "Perfect" pattern
# - Some additional cases selected at random
regex1lst.append('^\(CO')
regex1lst.append('R.G.*:')
regex1lst.append('C.+EG')
regex1 = 'r\''+'|'.join(regex1lst)+'\''


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
            if re.search(regex1, self.receipt.iloc[i, 8]) or i > 5:
                break
        self.company = ' '.join(self.temp)
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
