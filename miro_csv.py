import streamlit as st
import pandas as pd

# Define the function to process the input text
def process_input(text):
    data = []
    category = ""
    subcategory = ""
    subsubcategory = ""
    subsubsubcategory = ""
    
    for line in text.splitlines():
        line = line.strip()
        if line.startswith("#### "):
            subsubsubcategory = line[5:]
        elif line.startswith("### "):
            subsubcategory = line[4:]
            subsubsubcategory = ""
        elif line.startswith("## "):
            subcategory = line[3:]
            subsubcategory = ""
            subsubsubcategory = ""
        elif line.startswith("# "):
            category = line[2:]
            subcategory = ""
            subsubcategory = ""
            subsubsubcategory = ""
        elif line:
            data.append([category, subcategory, subsubcategory, subsubsubcategory, line])
    
    return pd.DataFrame(data)

# Streamlit UI
st.title("Structured Input to CSV Transformer")

input_text = st.text_area("Enter the structured input text here:", height=300)

if st.button("Transform to CSV"):
    df = process_input(input_text)
    if not df.empty:
        st.write("Transformed DataFrame:")
        st.write(df)

        csv = df.to_csv(index=False, header=False)
        st.download_button(label="Download CSV", data=csv, file_name="transformed_input.csv", mime="text/csv")
    else:
        st.write("No data to transform. Please check the input format.")
