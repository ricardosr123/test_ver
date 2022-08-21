from twyinvoice.invoice import TwyInvoice


def run():
    receipt_1 = TwyInvoice("./ocr_files/OCR1.txt")
    receipt_2 = TwyInvoice("./ocr_files/OCR2.txt")
    receipt_3 = TwyInvoice("./ocr_files/OCR1mod.txt")

    receipt_1.get_json("./output/OCR1.json")
    receipt_2.get_json("./output/OCR2.json")
    receipt_3.get_json("./output/OCR1mod.json")


if __name__ == '__main__':
    run()
