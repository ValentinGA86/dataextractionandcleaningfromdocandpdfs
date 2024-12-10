import os
import re
import chardet

def clean_text(text):
    """
    Cleans the input text by removing unwanted characters and normalizing whitespace.

    Args:
        text (str): The raw text to be cleaned.

    Returns:
        str: The cleaned text.
    """
    # Remove headers and footers (customize patterns as needed)
    # Example: Remove lines that contain 'Confidential' or 'Page X of Y'
    text = re.sub(r'Page \d+ of \d+', '', text, flags=re.IGNORECASE)
    text = re.sub(r'Confidential', '', text, flags=re.IGNORECASE)

    # Remove email signatures or disclaimers if present
    # text = re.sub(r'---.*', '', text, flags=re.DOTALL)

    # Remove non-ASCII characters (optional)
    # text = text.encode('ascii', 'ignore').decode()

    # Normalize text to lowercase (optional)
    text = text.lower()

    # Remove special characters (keep basic punctuation)
    text = re.sub(r'[^\w\s\.,;:\'\"?!-]', '', text)

    # Replace multiple spaces and newlines with a single space
    text = re.sub(r'\s+', ' ', text).strip()

    return text

def process_text_file(file_path):
    """
    Reads a text file, cleans its content, and writes the cleaned text back to the file.

    Args:
        file_path (str): The path to the text file.
    """
    # Detect encoding (optional)
    with open(file_path, 'rb') as f:
        raw_data = f.read()
        result = chardet.detect(raw_data)
        encoding = result['encoding'] if result['encoding'] else 'utf-8'

    # Read the file with the detected encoding
    with open(file_path, 'r', encoding=encoding, errors='ignore') as f:
        text = f.read()

    # Clean the text
    cleaned_text = clean_text(text)

    # Write the cleaned text back to the file or to a new file
    cleaned_file_path = file_path  # Overwrite the original file
    # cleaned_file_path = file_path.replace('.txt', '_cleaned.txt')  # Save to a new file

    with open(cleaned_file_path, 'w', encoding='utf-8') as f:
        f.write(cleaned_text)

    print(f"Cleaned {file_path}")

def clean_texts_in_directory(directory):
    """
    Recursively cleans all .txt files in the given directory and its subdirectories.

    Args:
        directory (str): The path to the directory containing text files.
    """
    for root, dirs, files in os.walk(directory):
        for filename in files:
            if filename.lower().endswith('.txt'):
                file_path = os.path.join(root, filename)
                process_text_file(file_path)

# Specify the directory containing your text files
texts_directory = r'/Users/valentin/Documents/IBM/hospitaltrainingdata/HOSPITAL'

clean_texts_in_directory(texts_directory)
