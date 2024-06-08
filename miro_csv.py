import streamlit as st
import csv
import re
import pandas as pd

def parse_structured_content(content):
    mind_map_data = []
    current_path = []

    # Process each line in the structured content.
    for line in content.split('\n'):
        line = line.strip()
        if line.startswith('# '):
            current_path = [line[2:]]  # Reset path at the main topic level.
        elif line.startswith('## '):
            current_path = current_path[:1] + [line[3:]]  # Subtopic level.
        elif line.startswith('### '):
            current_path = current_path[:2] + [line[4:]]  # Detail level.
        elif line.startswith('#### '):
            current_path = current_path[:3] + [line[5:]]  # Fourth level detail.
        elif line.startswith('- '):
            detail = re.sub(r'\[.*?\]\(.*?\)', '', line[2:]).strip()  # Remove Markdown links.
            full_path = current_path + [detail]
            mind_map_data.append(full_path)
        elif line:
            # For lines that are not headers or lists but still contain content.
            current_path.append(line)
            mind_map_data.append(current_path[:])

    return mind_map_data

def convert_to_dataframe(data):
    # Convert parsed data to a pandas DataFrame for display
    max_columns = max(len(row) for row in data)
    columns = [f"Level {i+1}" for i in range(max_columns)]
    df = pd.DataFrame(data, columns=columns)
    return df

def write_to_csv(data, filename='mind_map.csv'):
    # Write the mind map data to a CSV file.
    with open(filename, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["Main Topic", "Subtopic", "Detail", "Information"])
        for row in data:
            writer.writerow(row + [''] * (4 - len(row)))  # Fill empty columns to match header
    return filename

# Streamlit app layout
st.title("Mind Map CSV Generator")
st.write("Paste your structured content below to generate a CSV file.")

# Text area for user input
user_input = st.text_area("Structured Content", height=300)

if st.button('Submit'):
    if user_input:
        mind_map_data = parse_structured_content(user_input)
        
        if mind_map_data:
            df = convert_to_dataframe(mind_map_data)
            st.write("## Preview of the Data")
            st.dataframe(df)
            csv_filename = write_to_csv(mind_map_data)
            with open(csv_filename, 'rb') as file:
                st.download_button(
                    label="Download CSV",
                    data=file,
                    file_name=csv_filename,
                    mime='text/csv'
                )
        else:
            st.error("Parsed data is empty. Please check the structured content format.")
    else:
        st.error("Please paste the structured content before submitting.")
