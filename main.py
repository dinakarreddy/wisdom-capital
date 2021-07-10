import csv
import logging.config
from datetime import datetime

LOG_CONFIG = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': "[%(asctime)s] %(levelname)s [%(name)s: %(funcName)s: %(lineno)s] %(message)s",
            'datefmt': "%d/%b/%Y %H:%M:%S"
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
    },
    'loggers': {
        '': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
    }
}

logging.config.dictConfig(LOG_CONFIG)

import logging
import os

from bs4 import BeautifulSoup

LOGGER = logging.getLogger(__name__)
HTML_FILES_DIRECTORY = "contracts"
OUTPUT_FILES = {
    "transactions": "transactions.csv",
    "charges": "charges.csv",
}


def process_transactions(transactions_html):
    transactions_children = [x for x in transactions_html.children]
    data = []
    for transactions_child in transactions_children:
        if transactions_child in ('\n',):
            continue
        temp = []
        transaction_child_columns = [x for x in transactions_child.children]
        if transaction_child_columns not in (['NCL F&O'],):
            for column in transaction_child_columns:
                if column == '\n':
                    continue
                else:
                    temp.append(column.text.strip('\xa0').strip('\n').strip())
            # Ignoring rows related to "Scrip Summary" in html
            if not data or len(temp) == len(data[0]):
                data.append(temp)
    header = data[0]
    dict_data = []
    for row in data[1:]:
        dict_data.append({header[i]: row[i] for i in range(len(row))})
    return dict_data


def process_stt_and_other_charges(html):
    children = [y for y in [x for x in html.children][1].children]
    index_data = {
        "PAY IN/ PAY OUT OBLIGATION(Incl. Brok)": 1,
        "Brokerage (Taxable Amount for Supply)": 2,
        "Securities Transaction Tax (Rs.)": 3,
        "CGST Rate": 4,
        "CGST Amount": 5,
        "SGST Rate": 6,
        "SGST Amount": 7,
        "IGST Rate": 8,
        "IGST Amount": 9,
        "UTT Rate": 10,
        "UTT Amount": 11,
        "Exchange Transaction Charges": 12,
        "SEBI Turnover Fees": 13,
        "Clearing Charges": 14,
        "Tax4": 15,
        "CONTRACT WISE BROK": 16,
        "STAMP DUTY": 17,
        "ALIED CHARGES/ BSE CLEARING CHARGES": 18,
        "Net Amount receivable by Client/ (payable by Client)": 19,
    }
    data = {
        key: [x for x in children[(value * 2) + 1].children][-1].text for key, value in index_data.items()
    }
    return data


def process_html(file_path):
    LOGGER.info("processing file_path: {}".format(file_path))
    with open(file_path, "r") as f:
        soup = BeautifulSoup(f.read(), features="html.parser")
        children = [x for x in soup.find('body').children]
        extra = {}
        extra["trade_date"] = datetime.strptime(
            [x for x in [x for x in children[5].children][3].children][3].text.strip(), "%d-%m-%Y").strftime("%Y-%m-%d")
        extra["settlement_no"] = [x for x in [x for x in children[5].children][3].children][7].text.strip()
        extra["settlement_date"] = datetime.strptime(
            [x for x in [x for x in children[5].children][5].children][3].text.strip(), "%d-%m-%Y").strftime("%Y-%m-%d")
        extra["file_path"] = file_path
        transactions_html = children[17]
        transactions_data = process_transactions(transactions_html)
        charges_data = process_stt_and_other_charges(children[23])
    return {"transactions_data": transactions_data, "charges_data": charges_data, "extra": extra}


def main():
    """
    Python version used: 3.6.11

    Parses html files and stores the transactions and charges in two different csv files
    html files are picked up from "contracts" folder at the same level as this file

    For parsing html files it requires beautifulsoup4.
    """
    extra_header = ["trade_date", "settlement_no", "settlement_date", "file_path"]
    transactions_header = extra_header + ['Order No.', 'Order Time', 'Trade No.', 'Trade Time',
                                          'Security/Contract Description',
                                          'Buy(B)/Sell(S)', 'Quantity', 'Gross Rate/Trade Price Per Unit(Rs.)',
                                          'Brokerage per Unit(Rs.)', 'Net Rate per Unit(Rs.)',
                                          'Closing Rate Per Unit(only for Derivatives) (Rs.)',
                                          'Net Total (Before Levies)(Rs.)',
                                          'Remarks']
    charges_header = extra_header + ['PAY IN/ PAY OUT OBLIGATION(Incl. Brok)', 'Brokerage (Taxable Amount for Supply)',
                                     'Securities Transaction Tax (Rs.)', 'CGST Rate', 'CGST Amount', 'SGST Rate',
                                     'SGST Amount',
                                     'IGST Rate', 'IGST Amount', 'UTT Rate', 'UTT Amount',
                                     'Exchange Transaction Charges',
                                     'SEBI Turnover Fees', 'Clearing Charges', 'Tax4', 'CONTRACT WISE BROK',
                                     'STAMP DUTY',
                                     'ALIED CHARGES/ BSE CLEARING CHARGES',
                                     'Net Amount receivable by Client/ (payable by Client)',
                                     'file_path']
    with open(OUTPUT_FILES["charges"], "w") as charges_fp:
        with open(OUTPUT_FILES["transactions"], "w") as transactions_fp:
            transactions_writer = csv.DictWriter(transactions_fp, fieldnames=transactions_header, quoting=csv.QUOTE_ALL)
            charges_writer = csv.DictWriter(charges_fp, fieldnames=charges_header, quoting=csv.QUOTE_ALL)
            transactions_writer.writeheader()
            charges_writer.writeheader()
            for filename in os.listdir(HTML_FILES_DIRECTORY):
                if filename.endswith(".html"):
                    file_path = os.path.join(HTML_FILES_DIRECTORY, filename)
                    data = process_html(file_path)
                    data["charges_data"].update(data["extra"])
                    charges_writer.writerow(data["charges_data"])
                    for row in data["transactions_data"]:
                        row.update(data["extra"])
                        transactions_writer.writerow(row)


if __name__ == '__main__':
    main()
