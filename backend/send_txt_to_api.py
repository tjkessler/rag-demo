import os
import requests
import argparse


def read_txt_files_from_directory(directory: str) -> list[str]:
    """
    Reads all .txt files from the specified directory and returns their
    contents as a list of strings.

    Parameters
    ----------
    directory : str
        The path to the directory containing .txt files.

    Returns
    -------
    list[str]
        A list of strings, where each string is the content of a .txt file.
    """

    documents = []
    for filename in os.listdir(directory):
        if filename.endswith('.txt'):
            file_path = os.path.join(directory, filename)
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read().strip()
                if content:
                    documents.append(content)
    return documents


def send_documents_to_api(documents: list[str], api_url: str) -> dict:
    """
    Sends a list of documents to the specified API URL for ingestion.

    Parameters
    ----------
    documents : list[str]
        A list of strings, where each string is the content of a document.
    api_url : str
        The URL of the API endpoint to send the documents to.

    Returns
    -------
    dict
        The JSON response from the API.
    """

    data = {'documents': '\n'.join(documents)}
    response = requests.post(api_url, json=data)
    response.raise_for_status()
    return response.json()


def main(directory: str, api_url: str) -> None:
    """
    Main function to read .txt files from a directory and send them to the API.

    Parameters
    ----------
    directory : str
        The path to the directory containing .txt files.
    api_url : str
        The URL of the API endpoint to send the documents to.
    """

    documents = read_txt_files_from_directory(directory)
    if not documents:
        print('No .txt files found or all files are empty.')
        return
    try:
        result = send_documents_to_api(documents, api_url)
        print('Successfully sent documents. API response:')
        print(result)
    except Exception as e:
        print(f'Error sending documents: {e}')


if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        description='Send .txt files to backend API for ingestion.'
    )
    parser.add_argument(
        'directory', help='Directory containing .txt files'
    )
    parser.add_argument(
        '--api-url', default='http://localhost:8000/ingest', help='Backend API URL'
    )
    args = parser.parse_args()
    main(args.directory, args.api_url)
