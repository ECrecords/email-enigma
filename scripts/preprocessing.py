import argparse
import pandas as pd
import re

def contains_link(s):
    # Regular expression pattern to match URLs
    pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
    return s.str.contains(pattern, regex=True)

# Ensure this script is being run directly and not imported as a module
if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        description='Strip the data from the data file'
    )
    parser.add_argument('data', type=str, help='Path to the data file')

    args = parser.parse_args()

    df = pd.read_csv(args.data)

    df['header'] = df['header'].str.strip().str.strip().str.replace(r'Subject: ', '', regex=True)
    df['body'] = df['body'].str.strip()

    # Replace escape characters \r, \n, \t, and others with an empty string
    df['body'] = df['body'].str.replace(r'[\n\r\t]', ' ', regex=True)
    df['header'] = df['header'].str.replace(r'[\n\r\t]', ' ', regex=True)

    # Apply the contains_link function to the 'header' and 'body' columns
    # and combine the results with a logical OR (|)
    df['link'] = (contains_link(df['header']) | contains_link(df['body'])).astype(int)


    print(df.head())

    df.to_csv('data/text.csv', index=False)
