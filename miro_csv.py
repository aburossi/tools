import streamlit as st
import csv
import io

def process_lines(lines, current_level, current_row):
    while lines:
        line = lines.pop(0).strip()
        if not line:
            continue

        level = line.count('#')
        text = line.lstrip('# ')

        if level > current_level:
            current_row = process_lines(lines, level, current_row + [text])
        elif level == current_level:
            writer.writerow(current_row + [text])
        else:
            lines.insert(0, line)
            return current_row

    return current_row

def generate_csv(input_text):
    lines = input_text.split('\n')
    output = io.StringIO()
    global writer
    writer = csv.writer(output)
    process_lines(lines, 0, [])
    return output.getvalue()

# Streamlit app
st.title('Text to CSV Converter')

st.write('Paste your input text below:')
input_text = st.text_area('Input Text', height=300)

if st.button('Convert to CSV'):
    if input_text:
        csv_output = generate_csv(input_text)
        st.download_button(
            label="Download CSV",
            data=csv_output,
            file_name="output.csv",
            mime="text/csv"
        )
    else:
        st.write('Please paste some input text.')
