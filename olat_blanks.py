import streamlit as st
import re

def convert_to_fill_in_the_blanks(input_text):
    """
    Converts input text with blanks marked by asterisks into a formatted string for "Fill-in-the-Blanks" questions.
    
    Parameters:
    input_text (str): The input text containing blanks marked by '*'.
    
    Returns:
    str: The formatted output string.
    """
    questions = input_text.strip().split('\n\n')
    all_output = []

    for question in questions:
        blanks = re.findall(r'\*(.*?)\*', question)
        num_blanks = len(blanks)

        output_lines = [
            "Type\tFIB",
            "Title\tVervollständigen Sie die Lücken mit dem korrekten Begriff",
            f"Points\t{num_blanks}"
        ]

        parts = re.split(r'\*(.*?)\*', question)
        text_lines = []

        for index, part in enumerate(parts):
            if index % 2 == 0:
                text_lines.append(f"Text\t{part}")
            else:
                text_lines.append(f"1\t{part}\t20")

        final_output = '\n'.join(output_lines + text_lines)
        all_output.append(final_output)

    return '\n\n'.join(all_output)

def convert_to_drag_the_words(input_text):
    """
    Converts input text with blanks marked by asterisks into a formatted string for "Drag the Words" questions.
    
    Parameters:
    input_text (str): The input text containing blanks marked by '*'.
    
    Returns:
    str: The formatted output string.
    """
    questions = input_text.strip().split('\n\n')
    all_output = []

    for question in questions:
        blanks = re.findall(r'\*(.*?)\*', question)
        unique_blanks = list(set(blanks))
        blanks_str = '|'.join(unique_blanks)
        
        parts = re.split(r'(\*.*?\*)', question)

        output = [
            "Type\tInlinechoice",
            "Title\tWörter einordnen",
            "Question\tWählen Sie die richtigen Wörter",
            f"Points\t{len(blanks)}"
        ]

        for part in parts:
            if part.startswith('*') and part.endswith('*'):
                word = part[1:-1]
                output.append(f"1\t{blanks_str}\t{word}\t|")
            else:
                output.append(f"Text\t{part.strip()}")

        final_output = '\n'.join(output)
        all_output.append(final_output)

    return '\n\n'.join(all_output)

# Streamlit UI
st.title("Text Converter")

st.write("Enter the text with blanks marked by asterisks (*). Separate different questions with empty lines. The formatted output will be generated below.")

input_text = st.text_area("Input Text", height=200)
conversion_type = st.radio("Select Output Type", ("Fill-in-the-Blanks", "Inline Choice"))

if st.button("Convert"):
    if input_text:
        if conversion_type == "Fill-in-the-Blanks":
            output = convert_to_fill_in_the_blanks(input_text)
        else:
            output = convert_to_drag_the_words(input_text)
        
        st.text_area("Converted Text", value=output, height=200)
        st.write("To copy the converted text, please select it manually and use Ctrl+C (Cmd+C on Mac) to copy.")
    else:
        st.write("Please enter some text to convert.")
