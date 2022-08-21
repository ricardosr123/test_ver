# Next regex look for the structure "(CO.REG". It considers the following cases:
# - With/without first parenthesis
# - Spaces between parenthesis and CO, and between C0 . and . Reg
rgx_coreg_base = '^\(?\s?CO\s?.?\s?REG'
# - One possible letter misspelled.
variations1 = '[A-Z0-9\(\)\[\]\{\}]'
rgx_coreg_lst = [''.join([rgx_coreg_base[0:i], variations1, rgx_coreg_base[i + 1:]]) for i in [7, 8, 17, 18, 19]]
rgx_coreg_lst.insert(0, '^\(CO.REG')  # "Perfect" pattern
# - Some additional cases selected at random
rgx_coreg_lst.append('^\(CO')
rgx_coreg_lst.append('R.G.*:')
rgx_coreg_lst.append('C.+EG')
rgx_coreg = 'r\'' + '|'.join(rgx_coreg_lst) + '\''

# Next regex look for the structure "-INVOICE-".
# It considers one possible letter misspelled and having or not hyphens
rgx_invoice_base = '-?INVOICE-?'
variations2 = '[A-Z0-9]'
rgx_invoice_lst = [''.join([rgx_invoice_base[0:i], variations2, rgx_invoice_base[i + 1:]]) for i in [2, 3, 4, 5, 6, 7, 8]]
rgx_invoice_lst.insert(0, '-INVOICE-')  # "Perfect" pattern
rgx_invoice = 'r\'' + '|'.join(rgx_invoice_lst) + '\''

# Next regex look for the structure  "TOTAL ROUNDED".
# It considers getting zero,one or two spaces, and one possible letter misspelled
rgx_totr_base = 'TOTAL\s?\s?ROUNDED'
rgx_totr_lst = [''.join([rgx_totr_base[0:i], variations2, rgx_totr_base[i + 1:]]) for i in [0, 1, 2, 3, 4, 11, 12, 13, 14, 15, 16, 17]]
rgx_totr_lst.insert(0, 'TOTAL\sROUNDED')  # "Perfect" pattern
rgx_totr = 'r\'' + '|'.join(rgx_totr_lst) + '\''

# Next regex look for the structure of a date
# rgx_change = r'CHANGE'
rgx_date = r'[0-3][0-9]\s?-\s?[01][0-9]\s?-\s?[0-9][0-9]'

# Next regex look for the structure ITEM(S).
# It considers getting zero,one or two spaces, and one possible letter misspelled
rgx_item = r'ITEM\s?\(\s?S\s?\)'

rgx_item_base = 'ITEM\s?\(\s?S\s?\)'
rgx_item_base_lst = [''.join([rgx_item_base[0:i], variations2, rgx_item_base[i + 1:]]) for i in [0, 1, 2, 3, 12]]
rgx_item_base_lst.insert(0, 'ITEM\(S\)')  # "Perfect" pattern
rgx_item = 'r\'' + '|'.join(rgx_item_base_lst) + '\''
