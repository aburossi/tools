import streamlit as st
import re

def convert_to_fill_in_the_blanks(input_text):
    """
    Converts input text with blanks marked by slashes into a formatted string 
    for "Fill-in-the-Blanks" questions.
    
    Parameters:
    input_text (str): The input text containing blanks marked by '/'.
    
    Returns:
    str: The formatted output string.
    """
    # Split the input into separate questions based on double newlines.
    questions = input_text.strip().split('\n\n')
    all_output = []

    for question in questions:
        # Replace single newlines within a question block with a space.
        # This ensures that a multi-line question is treated as a single entity.
        processed_question = question.replace('\n', ' ')
        
        # Find all blanks marked by the new delimiter '/'.
        blanks = re.findall(r'/(.*?)/', processed_question)
        num_blanks = len(blanks)

        output_lines = [
            "Type\tFIB",
            "Title\tVervollständigen Sie die Lücken mit dem korrekten Begriff",
            f"Points\t{num_blanks}"
        ]

        # Split the question by the blanks, but keep the blanks as part of the list.
        parts = re.split(r'(/.*?/)', processed_question)
        text_lines = []

        for part in parts:
            # Ignore any empty strings that might result from the split.
            if not part:
                continue
            
            # Check if the part is a blank (e.g., "/word/").
            if part.startswith('/') and part.endswith('/'):
                word = part[1:-1]  # Extract the word from between the slashes.
                text_lines.append(f"1\t{word}\t20")
            else:
                # Otherwise, it's a regular text part.
                text_lines.append(f"Text\t{part}")

        final_output = '\n'.join(output_lines + text_lines)
        all_output.append(final_output)

    return '\n\n'.join(all_output)

def convert_to_drag_the_words(input_text):
    """
    Converts input text with blanks marked by slashes into a formatted string 
    for "Drag the Words" (Inline Choice) questions.
    
    Parameters:
    input_text (str): The input text containing blanks marked by '/'.
    
    Returns:
    str: The formatted output string.
    """
    questions = input_text.strip().split('\n\n')
    all_output = []

    for question in questions:
        # Apply the same newline replacement for consistency.
        processed_question = question.replace('\n', ' ')

        # Find all blanks marked by the new delimiter '/'.
        blanks = re.findall(r'/(.*?)/', processed_question)
        unique_blanks = list(set(blanks))
        blanks_str = '|'.join(unique_blanks)
        
        # Split by the blanks, keeping them in the list.
        parts = re.split(r'(/.*?/)', processed_question)

        output = [
            "Type\tInlinechoice",
            "Title\tWörter einordnen",
            "Question\tWählen Sie die richtigen Wörter",
            f"Points\t{len(blanks)}"
        ]

        for part in parts:
            # Ignore empty strings.
            if not part:
                continue

            if part.startswith('/') and part.endswith('/'):
                word = part[1:-1]
                output.append(f"1\t{blanks_str}\t{word}\t|")
            else:
                # The part is a text segment. Strip any extra whitespace from its ends.
                output.append(f"Text\t{part.strip()}")

        final_output = '\n'.join(output)
        all_output.append(final_output)

    return '\n\n'.join(all_output)

# --- Streamlit UI (Updated) ---
st.title("Text Converter")

# Updated instruction to reflect the new delimiter.
st.write("Enter the text with blanks marked by slashes (/). Separate different questions with empty lines. The formatted output will be generated below.")

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
