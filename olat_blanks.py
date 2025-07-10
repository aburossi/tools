import streamlit as st
import re

def convert_to_fill_in_the_blanks(input_text):
    """
    Converts input text with blanks marked by slashes into a single formatted 
    "Fill-in-the-Blanks" question, preserving line breaks.
    
    To create multiple distinct questions, separate them with an empty line.
    
    Parameters:
    input_text (str): The input text containing blanks marked by '/'.
    
    Returns:
    str: The formatted output string.
    """
    # To handle multiple question blocks, we split by double newlines (empty line).
    questions = input_text.strip().split('\n\n')
    all_output = []

    for question_block in questions:
        # Calculate total points for the entire block.
        blanks = re.findall(r'/(.*?)/', question_block)
        num_blanks = len(blanks)

        # Create the header for this question block.
        output_lines = [
            "Type\tFIB",
            "Title\tVervollständigen Sie die Lücken mit dem korrekten Begriff",
            f"Points\t{num_blanks}"
        ]

        # This list will hold all the 'Text' and '1' lines.
        content_lines = []
        
        # Split the entire block by the delimiter to isolate text and blanks.
        parts = re.split(r'(/.*?/)', question_block)

        for part in parts:
            if not part:
                continue
            
            # Check if the part is a blank (e.g., "/word/").
            if part.startswith('/') and part.endswith('/'):
                word = part[1:-1]
                content_lines.append(f"1\t{word}\t20")
            else:
                # This part is text. It may contain newlines.
                # Split the text part by newlines to preserve the original line breaks.
                sub_parts = part.split('\n')
                for i, sub_part in enumerate(sub_parts):
                    # Add the text line.
                    content_lines.append(f"Text\t{sub_part}")
                    # If this isn't the last sub_part, it means there was a newline.
                    # We add the next 'Text' line on the next iteration.
                    # This logic correctly preserves the structure.

        # Combine header and content.
        final_output = '\n'.join(output_lines + content_lines)
        all_output.append(final_output)

    return '\n\n'.join(all_output)

def convert_to_drag_the_words(input_text):
    """
    Converts input text with blanks marked by slashes into a single formatted 
    "Drag the Words" question.
    """
    questions = input_text.strip().split('\n\n')
    all_output = []

    for question_block in questions:
        blanks = re.findall(r'/(.*?)/', question_block)
        unique_blanks = list(set(blanks))
        blanks_str = '|'.join(unique_blanks)
        
        # We need to replace newlines with a placeholder for the Question line
        question_text_for_title = question_block.replace('\n', ' ').replace('/', '')
        
        output = [
            "Type\tInlinechoice",
            "Title\tWörter einordnen",
            # The 'Question' field itself doesn't typically handle complex formatting well,
            # so we create a simplified version for it. The main body will have the structure.
            "Question\tWählen Sie die richtigen Wörter",
            f"Points\t{len(blanks)}"
        ]

        content_lines = []
        parts = re.split(r'(/.*?/)', question_block)

        for part in parts:
            if not part:
                continue

            if part.startswith('/') and part.endswith('/'):
                word = part[1:-1]
                # For InlineChoice, the choice part doesn't precede a 'Text' line
                # so we can append it directly.
                content_lines.append(f"1\t{blanks_str}\t{word}\t|")
            else:
                # Handle potential newlines in the text part
                sub_parts = part.split('\n')
                for sub_part in sub_parts:
                    if sub_part: # Avoid adding empty text lines
                        content_lines.append(f"Text\t{sub_part.strip()}")

        final_output = '\n'.join(output + content_lines)
        all_output.append(final_output)

    return '\n\n'.join(all_output)

# --- Streamlit UI (Updated) ---
st.title("Convertisseur de Texte")

st.write("Entrez le texte avec les blancs marqués par des barres obliques (/). Les lignes seront combinées en une seule question. Utilisez une ligne vide pour commencer une nouvelle question.")

input_text = st.text_area("Texte d'entrée", height=200)
conversion_type = st.radio("Sélectionnez le type de sortie", ("Fill-in-the-Blanks", "Inline Choice"))

if st.button("Convertir"):
    if input_text:
        if conversion_type == "Fill-in-the-Blanks":
            output = convert_to_fill_in_the_blanks(input_text)
        else:
            output = convert_to_drag_the_words(input_text)
        
        st.text_area("Texte converti", value=output, height=300)
        st.write("Pour copier le texte, veuillez le sélectionner manuellement et utiliser Ctrl+C (Cmd+C sur Mac).")
    else:
        st.write("Veuillez entrer du texte à convertir.")
