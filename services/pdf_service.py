from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer
from reportlab.lib.units import inch
import os

def text_to_pdf(text: str, pdf_path: str) -> None:
    os.makedirs(os.path.dirname(pdf_path) or ".", exist_ok=True)
    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=letter,
        rightMargin=72,
        leftMargin=72,
        topMargin=72,
        bottomMargin=72
    )
    styles = getSampleStyleSheet()
    style_normal = styles['Normal']
    style_normal.fontName = 'Helvetica'
    style_normal.fontSize = 11
    style_normal.leading = 14
    style_normal.spaceAfter = 12
    
    story = []
    
    paragraphs = [p for p in text.splitlines() if p.strip()]
    
    for para in paragraphs:
        if para.strip().startswith(('•', '-', '*')):
            p = Paragraph(f"&bull; {para[1:].strip()}", style_normal)
        else:
            p = Paragraph(para, style_normal)
        story.append(p)
        story.append(Spacer(1, 0.2 * inch))
    
    doc.build(story)