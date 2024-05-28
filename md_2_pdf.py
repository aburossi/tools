import sys
import markdown
import pdfkit
from PyQt5.QtWidgets import QApplication, QTextEdit, QPushButton, QVBoxLayout, QWidget, QFileDialog
from docx import Document
from bs4 import BeautifulSoup

class MarkdownConverter(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle('Markdown to PDF & DOCX Converter')

        self.textEdit = QTextEdit(self)
        self.savePDFButton = QPushButton('Save as PDF', self)
        self.saveDOCXButton = QPushButton('Save as DOCX', self)

        self.savePDFButton.clicked.connect(self.save_as_pdf)
        self.saveDOCXButton.clicked.connect(self.save_as_docx)

        layout = QVBoxLayout()
        layout.addWidget(self.textEdit)
        layout.addWidget(self.savePDFButton)
        layout.addWidget(self.saveDOCXButton)

        self.setLayout(layout)
        self.show()

    def save_as_pdf(self):
        markdown_text = self.textEdit.toPlainText()
        html_text = markdown.markdown(markdown_text)

        file_dialog = QFileDialog(self)
        save_path, _ = file_dialog.getSaveFileName(self, "Save PDF", "", "PDF files (*.pdf)")

        if save_path:
            pdfkit.from_string(html_text, save_path)

    def save_as_docx(self):
        markdown_text = self.textEdit.toPlainText()
        html_text = markdown.markdown(markdown_text)

        soup = BeautifulSoup(html_text, 'html.parser')
        text = soup.get_text()

        file_dialog = QFileDialog(self)
        save_path, _ = file_dialog.getSaveFileName(self, "Save DOCX", "", "Word files (*.docx)")

        if save_path:
            doc = Document()
            for line in text.split('\n'):
                doc.add_paragraph(line)
            doc.save(save_path)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MarkdownConverter()
    sys.exit(app.exec_())
