import streamlit as st
import pandas as pd

# Define the function to process the input text
def process_input(text):
    data = []
    category = ""
    subcategory = ""
    subsubcategory = ""
    description = ""

    for line in text.splitlines():
        line = line.strip()
        if line.startswith("## "):
            subcategory = line[3:]
        elif line.startswith("### "):
            subsubcategory = line[4:]
        elif line.startswith("- "):
            description = line[2:]
            data.append([category, subcategory, subsubcategory, description])
        elif line.startswith("# "):
            category = line[2:]
            subcategory = ""
            subsubcategory = ""

    return pd.DataFrame(data, columns=["Category", "Subcategory", "Subsubcategory", "Description"])

# Streamlit UI
st.title("Structured Input to CSV Transformer")

input_text = st.text_area("Enter the structured input text here:", height=300)

if st.button("Transform to CSV"):
    df = process_input(input_text)
    st.write("Transformed DataFrame:")
    st.write(df)

    csv = df.to_csv(index=False)
    st.download_button(label="Download CSV", data=csv, file_name="transformed_input.csv", mime="text/csv")
