import streamlit as st
import re

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
st.title("Drag the Words Text Converter")

st.write("Enter the text with blanks marked by asterisks (*). Separate different questions with empty lines. The formatted output for 'Drag the Words' will be generated below.")

input_text = st.text_area("Input Text", height=200)
if st.button("Convert"):
    if input_text:
        output = convert_to_drag_the_words(input_text)
        st.text_area("Converted Text", value=output, height=200)
        st.write("To copy the converted text, please select it manually and use Ctrl+C (Cmd+C on Mac) to copy.")
    else:
        st.write("Please enter some text to convert.")
