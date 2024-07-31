import streamlit as st
import re

def convert_text_with_wrong_options(input_text):
    """
    Converts input text with blanks marked by asterisks and wrong options into formatted strings
    for both "Fill-in-the-Blanks" and "Inline Choice" questions.
    
    Parameters:
    input_text (str): The input text containing blanks marked by '*' and wrong options.
    
    Returns:
    tuple: Two strings, one for Fill-in-the-Blanks format and one for Inline Choice format.
    """
    questions = input_text.strip().split('\n\n')
    fib_output = []
    ic_output = []
    
    for question in questions:
        lines = question.split('\n')
        text = lines[0]
        wrong_options = lines[1].strip('[]').split(',') if len(lines) > 1 else []
        
        blanks = re.findall(r'\*(.*?)\*', text)
        num_blanks = len(blanks)
        
        # Fill-in-the-Blanks format
        fib_lines = [
            "Type\tFIB",
            "Title\tVervollständigen Sie die Lücken mit dem korrekten Begriff",
            f"Points\t{num_blanks}"
        ]
        parts = re.split(r'\*(.*?)\*', text)
        for index, part in enumerate(parts):
            if index % 2 == 0:
                fib_lines.append(f"Text\t{part}")
            else:
                fib_lines.append(f"1\t{part}\t20")
        fib_output.append('\n'.join(fib_lines))
        
        # Inline Choice format
        ic_lines = [
            "Type\tInlinechoice",
            "Title\tWörter einordnen",
            "Question\tWählen Sie die richtigen Wörter",
            f"Points\t{num_blanks}"
        ]
        parts = re.split(r'(\*.*?\*)', text)
        for part in parts:
            if part.startswith('*') and part.endswith('*'):
                word = part[1:-1]
                options = [word] + wrong_options
                options_str = '|'.join(options)
                ic_lines.append(f"1\t{options_str}\t{word}\t|")
            else:
                ic_lines.append(f"Text\t{part.strip()}")
        ic_output.append('\n'.join(ic_lines))
    
    return '\n\n'.join(fib_output), '\n\n'.join(ic_output)

# Example usage:
input_text = '''"Der Lehrvertrag ist ein *schriftlicher Vertrag*, der zwischen dem Lehrbetrieb und den gesetzlichen Vertretern eines Lernenden abgeschlossen wird. Der Vertrag muss von beiden Parteien *unterschrieben* werden und enthält alle wichtigen Vereinbarungen über das Lehrverhältnis. Dazu gehören unter anderem die Dauer der *Lehre*, die Höhe der Ausbildungsvergütung und die *Rechte und Pflichten* beider Parteien.
[mündlicher Vertrag],[beglaubigt],[Bewertungskriterien],[Arbeitszeiten]'''

fib_result, ic_result = convert_text_with_wrong_options(input_text)
print("Fill-in-the-Blanks format:")
print(fib_result)
print("\nInline Choice format:")
print(ic_result)


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
