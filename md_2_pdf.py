import subprocess
import tempfile
import os

def convert_markdown(content, output_format):
    # Create a temporary markdown file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".md") as md_file:
        md_file.write(content.encode('utf-8'))
        md_file_path = md_file.name

    # Determine the output file name and format
    if output_format.lower() == 'pdf':
        output_file_path = md_file_path.replace('.md', '.pdf')
    elif output_format.lower() == 'doc':
        output_file_path = md_file_path.replace('.md', '.docx')
    else:
        raise ValueError("Unsupported output format. Choose 'pdf' or 'doc'.")

    # Run pandoc command to convert markdown to the desired format
    command = ['pandoc', md_file_path, '-o', output_file_path]
    subprocess.run(command, check=True)

    # Clean up the temporary markdown file
    os.remove(md_file_path)

    return output_file_path

def main():
    # Get markdown content from the user
    markdown_content = input("Paste your markdown content here:\n")
    output_format = input("Do you want a 'pdf' or 'doc' output? ")

    try:
        output_file = convert_markdown(markdown_content, output_format)
        print(f"Conversion successful! Your file is saved at: {output_file}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
