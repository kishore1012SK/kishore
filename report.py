from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from datetime import datetime

def generate_report(text, filename="audit_report.pdf"):
    doc = SimpleDocTemplate(filename)
    styles = getSampleStyleSheet()
    story = []
    
    story.append(Paragraph("FairAI LiveGuard: Compliance & Bias Audit", styles['Title']))
    story.append(Spacer(1, 12))
    story.append(Paragraph(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", styles['Italic']))
    story.append(Spacer(1, 12))
    
    for line in text.split('\n'):
        story.append(Paragraph(line, styles['Normal']))
        story.append(Spacer(1, 6))
        
    doc.build(story)
    return filename
