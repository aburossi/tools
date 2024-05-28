import streamlit as st
import markdown
import pdfkit
from io import BytesIO

def markdown_to_pdf(markdown_text):
    # Convert Markdown to HTML
    html_text = markdown.markdown(markdown_text)
    
    # Convert HTML to PDF using pdfkit and BytesIO
    pdf_output = BytesIO()
    pdfkit.from_string(html_text, pdf_output)
    pdf_output.seek(0)
    return pdf_output

def main():
    st.title("Markdown to PDF Converter")

    # Input markdown text
    markdown_text = st.text_area("Enter your Markdown text here:")

    if st.button("Convert to PDF"):
        if markdown_text:
            pdf_output = markdown_to_pdf(markdown_text)
            st.success("PDF generated successfully!")
            
            # Provide a download button
            st.download_button(
                label="Download PDF",
                data=pdf_output,
                file_name="output.pdf",
                mime="application/pdf"
            )
        else:
            st.error("Please enter some Markdown text")

if __name__ == "__main__":
    main()
