import streamlit as st
import pandas as pd

def parse_markdown_to_dataframe(markdown_text):
    rows = []
    current_levels = [""] * 4
    
    for line in markdown_text.split("\n"):
        stripped_line = line.strip()
        
        if stripped_line.startswith("####"):
            current_levels[3] = stripped_line[4:].strip()
        elif stripped_line.startswith("###"):
            current_levels[2] = stripped_line[3:].strip()
            current_levels[3] = ""
        elif stripped_line.startswith("##"):
            current_levels[1] = stripped_line[2:].strip()
            current_levels[2] = ""
            current_levels[3] = ""
        elif stripped_line.startswith("#"):
            current_levels[0] = stripped_line[1:].strip()
            current_levels[1] = ""
            current_levels[2] = ""
            current_levels[3] = ""
        
        if all(level != "" for level in current_levels):
            rows.append(current_levels.copy())
    
    return pd.DataFrame(rows, columns=['Level 1', 'Level 2', 'Level 3', 'Level 4'])

def concatenate_columns(row):
    return ','.join(row.dropna().astype(str))

def generate_csv(dataframe):
    dataframe['concatenated'] = dataframe.apply(concatenate_columns, axis=1)
    # Return the concatenated column without a header
    return dataframe[['concatenated']].to_csv(index=False, header=False)

# Streamlit app
st.title("Markdown to CSV Converter")

st.write("""
### Enter your markdown text
""")
markdown_input = st.text_area("Markdown Input", height=300)

if markdown_input:
    df = parse_markdown_to_dataframe(markdown_input)
    st.write("### Preview of the hierarchy")
    st.dataframe(df)
    
    csv = generate_csv(df)
    
    st.download_button(
        label="Download CSV",
        data=csv,
        file_name='converted_hierarchy.csv',
        mime='text/csv'
    )
