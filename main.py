import os
from docx import Document
import PyPDF2

def extract_text_from_docx(file_path):
    """
    Extracts text from a .docx file.

    Args:
        file_path (str): The path to the .docx file.

    Returns:
        str: The extracted text.
    """
    doc = Document(file_path)
    full_text = []
    for para in doc.paragraphs:
        full_text.append(para.text)
    return '\n'.join(full_text)

def extract_text_from_pdf(file_path):
    """
    Extracts text from a .pdf file.

    Args:
        file_path (str): The path to the .pdf file.

    Returns:
        str: The extracted text.
    """
    text = ''
    with open(file_path, 'rb') as f:
        reader = PyPDF2.PdfReader(f)
        for page_num, page in enumerate(reader.pages):
            page_text = page.extract_text()
            if page_text:
                text += page_text
            else:
                print(f'Warning: No text found on page {page_num + 1} of {file_path}')
    return text

def extract_texts_from_directory(directory):
    for root, dirs, files in os.walk(directory):
        for filename in files:
            # Skip temporary files starting with '~$' and hidden files starting with '.'
            if filename.startswith('~$') or filename.startswith('.'):
                print(f"Skipping temporary or hidden file: {filename}")
                continue
            file_path = os.path.join(root, filename)
            # Process .docx files
            if filename.lower().endswith('.docx'):
                print(f'Extracting text from {filename}')
                try:
                    text = extract_text_from_docx(file_path)
                    # Save the extracted text to a .txt file
                    txt_filename = os.path.splitext(filename)[0] + '.txt'
                    txt_file_path = os.path.join(root, txt_filename)
                    with open(txt_file_path, 'w', encoding='utf-8') as txt_file:
                        txt_file.write(text)
                except Exception as e:
                    print(f"Error processing {filename}: {e}")
            # Process .pdf files
            elif filename.lower().endswith('.pdf'):
                print(f'Extracting text from {filename}')
                try:
                    text = extract_text_from_pdf(file_path)
                    # Save the extracted text to a .txt file
                    txt_filename = os.path.splitext(filename)[0] + '.txt'
                    txt_file_path = os.path.join(root, txt_filename)
                    with open(txt_file_path, 'w', encoding='utf-8') as txt_file:
                        txt_file.write(text)
                except Exception as e:
                    print(f"Error processing {filename}: {e}")
            else:
                print(f'Skipping {filename}: Unsupported file type.')

# Specify the directory containing your documents
documents_directory = r'/Users/valentin/Documents/IBM/hospitaltrainingdata/HOSPITAL'

extract_texts_from_directory(documents_directory)
