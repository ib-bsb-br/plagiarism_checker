""" This module is used to process text in docx, odt, txt and pdf files """

import re
import zipfile
from os import path

import pytesseract
from pdf2image import convert_from_path
from odf import text, teletype
from odf.opendocument import load
from pdfminer.high_level import extract_text


def get_file_extension(filepath: str) -> str:
    """Return the file extension of the file at the specified path"""
    if not path.isfile(filepath):
        raise ValueError(f"Invalid file path: {filepath}")

    try:
        return path.splitext(filepath)[1]
    except IndexError:
        raise ValueError(f"File extension error for file: {filepath}")


def file_extension_call(file: str) -> list:
    """Map file extension to appropriate function"""

    extension = get_file_extension(file)

    if extension == ".pdf":
        return get_words_from_pdf_file(file)
    elif extension == ".docx":
        return get_words_from_docx_file(file)
    elif extension == ".odt":
        return get_words_from_odt_file(file)
    elif extension == ".txt":
        return get_words_from_txt_file(file)
    else:
        raise ValueError(f"File format not supported for file: {file}. " f"Please convert to pdf, docx, odt, or txt")


def get_words_from_pdf_file(pdf_path: str) -> list:
    """
    Return list of words from a PDF file at the specified path.
    Attempts to extract text using pdfminer.six. If the extracted text is too short
    or empty (e.g., for image-based PDFs), it falls back to OCR using pytesseract.
    """

    # Attempt to extract text using pdfminer.six
    extracted_text_pdfminer = extract_text(pdf_path)
    cleaned_text_pdfminer = re.sub(r"\s+", " ", extracted_text_pdfminer)
    cleaned_text_pdfminer = re.sub(r"<(.|\n)*?>", "", cleaned_text_pdfminer) # Basic cleaning
    cleaned_text_pdfminer = cleaned_text_pdfminer.replace(" ", " ").strip()

    if len(cleaned_text_pdfminer) > 50: # Check if pdfminer text is substantial
        return re.findall(r"\w+", cleaned_text_pdfminer.lower())

    # Fallback to OCR if pdfminer.six text is not substantial
    pages = convert_from_path(pdf_path, 300)
    ocr_text = ''
    for page in pages:
        text_from_page = pytesseract.image_to_string(page, lang='eng')
        ocr_text += text_from_page + " " # Add space between page texts

    ocr_text = ocr_text.replace(" ", " ").strip()
    return re.findall(r"\w+", ocr_text.lower())


def get_words_from_txt_file(txt_path: str) -> list:
    """Return list of words from txt file at specified path"""

    words = []

    with open(txt_path, encoding="utf-8") as file:
        for line in file:
            try:
                for word in line.split():
                    words.append(word.lower())
            except (UnicodeError, UnicodeDecodeError):
                pass

    str_words = " ".join(map(str, words))

    return re.findall(r"\w+", str_words)


def get_words_from_docx_file(docx_path: str) -> list:
    """Return list of words from docx file at specified path"""

    with zipfile.ZipFile(docx_path) as docx:
        content = docx.read("word/document.xml").decode("utf-8")
        cleaned = re.sub("<(.|\n)*?>", "", content)

    return re.findall(r"\w+", cleaned.lower())


def get_words_from_odt_file(odt_path: str) -> list:
    """Return list of words from odt file at specified path"""

    textdoc = load(odt_path)
    paragraphs = textdoc.getElementsByType(text.P)

    full_text = str()

    for paragraph in paragraphs:
        temp = teletype.extractText(paragraph)
        full_text += temp.lower()

    return re.findall(r"\w+", full_text)
