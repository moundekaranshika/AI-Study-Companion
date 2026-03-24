from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet


def create_pdf(summary, questions, flashcards, filename="output.pdf"):
    doc = SimpleDocTemplate(filename)
    styles = getSampleStyleSheet()

    content = []

    # Title
    content.append(Paragraph("AI Study Companion Output", styles['Title']))
    content.append(Spacer(1, 20))

    # Summary
    content.append(Paragraph("Summary", styles['Heading2']))
    content.append(Paragraph(summary, styles['BodyText']))
    content.append(Spacer(1, 15))

    # Questions
    content.append(Paragraph("Viva Questions", styles['Heading2']))
    content.append(Paragraph(questions, styles['BodyText']))
    content.append(Spacer(1, 15))

    # Flashcards
    content.append(Paragraph("Flashcards", styles['Heading2']))
    content.append(Paragraph(flashcards, styles['BodyText']))

    doc.build(content)

    return filename