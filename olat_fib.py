import streamlit as st
import re
import pyperclip

def convert_text(input_text):
    """
    Converts input text with blanks marked by asterisks into a formatted string for multiple questions.
    
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
                text_lines.append(f"{index//2 + 1}\t{part}\t15")

        final_output = '\n'.join(output_lines + text_lines)
        all_output.append(final_output)

    return '\n\n'.join(all_output)

# Streamlit UI
st.title("Fill-in-the-Blanks Text Converter")

st.write("Enter the text with blanks marked by asterisks (*). Separate different questions with empty lines. The formatted output will be generated below.")

input_text = st.text_area("Input Text", height=200)
if st.button("Convert"):
    if input_text:
        output = convert_text(input_text)
        st.text_area("Converted Text", value=output, height=200)
        
        if st.button("Copy to Clipboard"):
            pyperclip.copy(output)
            st.write("Converted text copied to clipboard.")
    else:
        st.write("Please enter some text to convert.")
