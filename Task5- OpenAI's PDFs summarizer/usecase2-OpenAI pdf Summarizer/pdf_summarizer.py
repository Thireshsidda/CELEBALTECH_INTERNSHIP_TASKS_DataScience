import PyPDF2
import openai
import fitz

# Set up your OpenAI API key
# Replace 'YOUR_API_KEY' with your actual OpenAI API key
#openai.organization = "org-6FPbDXnJAXHDlC0uuZLbrIA0"
openai.organization = " ##### "
openai.api_key = '###### '
input_pdf = r"C:\Users\Thiresh sidda\Downloads\LinuxFundamentalsByBridgeLabz (1).pdf"

def read_pdf_contents(pdf_file):
    """
    Read the contents of a PDF file page by page.

    Args:
        pdf_file (str): The path to the PDF file.

    Returns:
        list: A list of strings, where each string represents the content of a page.
    """
    contents = []
    with open(pdf_file, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        num_pages = len(pdf_reader.pages)
        for page_num in range(num_pages):
            page = pdf_reader.pages[page_num]
            contents.append(page.extract_text())
    return contents




def summarize_text(text):
    """
    Summarize a piece of text using OpenAI's language model.

    Args:
        text (str): The input text to be summarized.

    Returns:
        str: The summarized text.
    """
    response = openai.Completion.create(
        engine='text-davinci-003',
        prompt=text,
        temperature=0.3,
        max_tokens=100,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0
    )
    return response.choices[0].text.strip()



import fitz

def save_summaries_to_pdf(summaries, output_file):
    """
    Save the summaries to a new PDF file.

    Args:
        summaries (list): A list of strings containing the summaries.
        output_file (str): The path to the output PDF file.

    Returns:
        None
    """
    pdf_writer = fitz.open()
    for summary in summaries:
        page = pdf_writer.new_page()
        page.insert_text(fitz.Point(50, 50), summary)
    pdf_writer.save(output_file)






# Example usage
# Assuming you have a PDF file named 'input.pdf' in the same directory

# Step 1: Read the contents of the PDF file
pdf_contents = read_pdf_contents(input_pdf)

# Step 2: Summarize the contents
summaries = []
for content in pdf_contents:
    summary = summarize_text(content)
    summaries.append(summary)

# Step 3: Save the summaries to a new PDF file
output_pdf = 'output.pdf'
save_summaries_to_pdf(summaries, output_pdf)
print(f"Summarized PDF saved as: {output_pdf}")

