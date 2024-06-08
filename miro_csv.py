import streamlit as st
import pandas as pd
import csv
import re

def parse_structured_content(content):
    # Parse structured content to a list of paths for the mind map.
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
            detail = re.sub(r'\[.*?\]\(.*?\)', '', line[5:]).strip()  # Remove Markdown links.
            full_path = current_path + [detail]
            mind_map_data.append(full_path)

    return mind_map_data

def write_to_csv(data, filename='schweizer_vorsorgesystem.csv'):
    # Write the mind map data to a CSV file.
    with open(filename, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        for row in data:
            writer.writerow(row)
    print(f"CSV file '{filename}' created successfully.")

def concatenate_columns(row):
    return ','.join(row.dropna().astype(str))

def generate_csv(data):
    df = pd.DataFrame(data, columns=['Level 1', 'Level 2', 'Level 3', 'Level 4'])
    df['concatenated'] = df.apply(concatenate_columns, axis=1)
    return df[['concatenated']].to_csv(index=False, header=False, encoding='utf-8')

# Streamlit app
st.title("Markdown to CSV Converter")

st.write("""
### Enter your markdown text
""")
markdown_input = st.text_area("Markdown Input", height=300)

if markdown_input:
    mind_map_data = parse_structured_content(markdown_input)
    df = pd.DataFrame(mind_map_data, columns=['Level 1', 'Level 2', 'Level 3', 'Level 4'])
    st.write("### Preview of the hierarchy")
    st.dataframe(df)
    
    csv = generate_csv(mind_map_data)
    
    st.download_button(
        label="Download CSV",
        data=csv,
        file_name='converted_hierarchy.csv',
        mime='text/csv'
    )
