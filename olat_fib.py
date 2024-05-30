import streamlit as st
import re

def convert_text(input_text):
    """
    Converts input text with blanks marked by asterisks into a formatted string.
    
    Parameters:
    input_text (str): The input text containing blanks marked by '*'.
    
    Returns:
    str: The formatted output string.
    """
    # Find all blanks in the text
    blanks = re.findall(r'\*(.*?)\*', input_text)
    num_blanks = len(blanks)

    # Prepare the output lines
    output_lines = [
        "Type\tFIB",
        "Title\tVervollständigen Sie die Lücken mit dem korrekten Begriff",
        f"Points\t{num_blanks}"
    ]

    # Split the text at the blanks
    parts = re.split(r'\*(.*?)\*', input_text)

    # Build the text lines with blanks replaced by tab-separated values
    text_lines = []
    for index, part in enumerate(parts):
        if index % 2 == 0:
            text_lines.append(f"Text\t{part}")
        else:
            text_lines.append(f"{index//2 + 1}\t{part}\t15")

    # Combine all parts into the final output
    final_output = '\n'.join(output_lines + text_lines)
    return final_output

# Streamlit UI
st.title("Fill-in-the-Blanks Text Converter")

st.write("Enter the text with blanks marked by asterisks (*). The formatted output will be generated below.")

input_text = st.text_area("Input Text", height=200)
if st.button("Convert"):
    if input_text:
        output = convert_text(input_text)
        st.text_area("Converted Text", value=output, height=200, readonly=True)
        st.write("Copy the above text for your use.")
    else:
        st.write("Please enter some text to convert.")
