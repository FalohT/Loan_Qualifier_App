# -*- coding: utf-8 -*-
"""Helper functions to load and save CSV data.

This contains a helper function for loading and saving CSV files.

"""

import csv
import os

def load_csv(csvpath):
    """Reads the CSV file from path provided.

    Args:
        csvpath (Path): The csv file path.

    Returns:
        A list of lists that contains the rows of data from the CSV file.

    """
    with open(csvpath, "r") as csvfile:
        data = []
        csvreader = csv.reader(csvfile, delimiter=",")

        # Skip the CSV Header
        next(csvreader)

        # Read the CSV data
        for row in csvreader:
            data.append(row)
    return data

def save_csv(output_path, qualifying_loans):
    """Saves the CSV file from path provided by user input.
        Checks to make sure the file was written and notifies the user

    Args:
        output_path (Path): The csv file output path from user input.
        qualifying_loans : List of qualifying loans from calculations.

    Saves:
        A list that contains the rows of qualifying loans for a customer.

    """
    header = ["Lender", "Max Loan Amount", "Max LTV", "Max DTI", "Min Credit Score", "Interest Rate"]
    with open(output_path, 'w', newline = '') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(header)

        for loans in qualifying_loans:
            csvwriter.writerow(loans)
        if os.path.isfile(output_path):
            print(f'The file {csvfile.name} was successfully written')
        else:
            print(f'The file {output_path} was not written')
