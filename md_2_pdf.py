import streamlit as st
import markdown
from weasyprint import HTML

def markdown_to_pdf(markdown_text, output_pdf):
    # Convert Markdown to HTML
    html_text = markdown.markdown(markdown_text)
    
    # Convert HTML to PDF using WeasyPrint
    HTML(string=html_text).write_pdf(output_pdf)

# Streamlit app
st.title("Markdown to PDF Converter")

st.write("Enter your Markdown text below:")

# Text area for markdown input
markdown_text = st.text_area("Markdown Input", height=300)

if st.button("Convert to PDF"):
    # Output PDF file name
    output_file = "output.pdf"
    
    # Convert and save as PDF
    markdown_to_pdf(markdown_text, output_file)
    
    # Display download link for the PDF
    with open(output_file, "rb") as file:
        btn = st.download_button(
            label="Download PDF",
            data=file,
            file_name=output_file,
            mime="application/pdf"
        )
