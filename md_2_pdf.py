import subprocess
import tempfile
import os
import click

def convert_markdown(content, output_format):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".md") as md_file:
        md_file.write(content.encode('utf-8'))
        md_file_path = md_file.name

    if output_format.lower() == 'pdf':
        output_file_path = md_file_path.replace('.md', '.pdf')
    elif output_format.lower() == 'doc':
        output_file_path = md_file_path.replace('.md', '.docx')
    else:
        raise ValueError("Unsupported output format. Choose 'pdf' or 'doc'.")

    command = ['pandoc', md_file_path, '-o', output_file_path]
    subprocess.run(command, check=True)

    os.remove(md_file_path)

    return output_file_path

@click.command()
@click.prompt('Paste your markdown content here', prompt_suffix='\n', hide_input=False)
@click.option('--output_format', type=click.Choice(['pdf', 'doc'], case_sensitive=False), prompt=True)
def main(markdown_content, output_format):
    try:
        output_file = convert_markdown(markdown_content, output_format)
        click.echo(f"Conversion successful! Your file is saved at: {output_file}")
    except Exception as e:
        click.echo(f"An error occurred: {e}")

if __name__ == "__main__":
    main()