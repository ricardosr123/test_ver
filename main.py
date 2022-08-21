from twyinvoice.invoice import TwyInvoice


def run():
    # Create invoices
    invoice_1 = TwyInvoice("./ocr_files/OCR1.txt")
    invoice_2 = TwyInvoice("./ocr_files/OCR2.txt")

    # Extract info and build json and save it in the specified location
    invoice_1.get_json("./output/OCR1.json")
    invoice_2.get_json("./output/OCR2.json")


if __name__ == '__main__':
    run()
