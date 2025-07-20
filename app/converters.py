from markitdown import MarkItDown
import io

def convert_html_to_format(html_bytes: bytes, output_format: str):
    md = MarkItDown(enable_plugins=False)
    input_stream = io.BytesIO(html_bytes)
    result = md.convert_stream(input_stream, source_format="html")
    markdown = result.text_content

    if output_format == "markdown":
        return {
            "content": markdown.encode("utf-8"),
            "media_type": "text/markdown",
            "filename": "conversation.md"
        }

    elif output_format == "pdf":
        from fpdf import FPDF
        pdf = FPDF()
        pdf.add_page()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.set_font("Arial", size=12)
        for line in markdown.splitlines():
            pdf.multi_cell(0, 10, line)
        # Get the PDF content as bytes using output() with 'S' parameter
        pdf_content = pdf.output(dest='S').encode('latin-1')
        return {
            "content": pdf_content,
            "media_type": "application/pdf",
            "filename": "conversation.pdf"
        }

    elif output_format == "docx":
        from docx import Document
        doc = Document()
        for line in markdown.splitlines():
            doc.add_paragraph(line)
        output = io.BytesIO()
        doc.save(output)
        return {
            "content": output.getvalue(),
            "media_type": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            "filename": "conversation.docx"
        }
