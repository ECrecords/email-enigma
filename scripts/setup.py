import kaggle
import os
import pandas as pd
import re

def read_file(file_path):
    """
    Reads a file and removes special characters.

    :param file_path: Path of the file to be read.
    :return: Content of the file as a string with special characters removed.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except UnicodeDecodeError:
        with open(file_path, 'r', encoding='latin-1') as f:
            content = f.read()
    
    # Remove special characters
    content = re.sub(r'[^a-zA-Z0-9\s]', '', content)
    return content
def download_dataset(dataset):
    """
    Downloads the specified Kaggle dataset, reads email contents, and
    returns them in a Pandas DataFrame.

    :param dataset: The Kaggle dataset identifier.
    :return: Pandas DataFrame with email texts and labels.
    """

    data_dir = './data'

    if not os.path.exists(data_dir):
        print("Creating data directory...")
        os.mkdir(data_dir)
    else:
        print("Data directory already exists. Proceeding.")

    # Authenticate with Kaggle API
    kaggle.api.authenticate()

    # Check if the data directory is empty before downloading
    if not os.listdir(data_dir):
        print("Downloading dataset...")
        kaggle.api.dataset_download_files(dataset, path=data_dir, unzip=True)
    else:
        print("Data already downloaded. Proceeding to read files.")

    email_data = []

    for dir_name in os.listdir(data_dir):
        for label in ['spam', 'ham']:
            label_dir = os.path.join(data_dir, dir_name, label)
            if os.path.exists(label_dir) and os.path.isdir(label_dir):
                for email_file in os.listdir(label_dir):
                    file_path = os.path.join(label_dir, email_file)
                    email_text = read_file(file_path)
                    email_data.append({'text': email_text, 'spam': 1 if label == 'spam' else 0})

    return pd.DataFrame(email_data)

def save_to_csv(df, filename):
    """
    Saves the DataFrame to a CSV file.

    :param df: Pandas DataFrame to save.
    :param filename: Filename for the CSV file.
    """
    df.to_csv(filename, index=False)
    print(f"DataFrame saved to {filename}")

if __name__ == "__main__":
    dataset = 'wanderfj/enron-spam'
    df = download_dataset(dataset)
    csv_filename = "./emails.csv"
    save_to_csv(df, csv_filename)
