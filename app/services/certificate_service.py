from pathlib import Path

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas


CERTIFICATE_DIR = Path("certificates")
CERTIFICATE_DIR.mkdir(exist_ok=True)


def generate_certificate(
    recipient_name: str,
    event_name: str,
    event_date: str,
    certificate_id: int
) -> str:

    filename = f"certificate_{certificate_id}.pdf"
    file_path = CERTIFICATE_DIR / filename

    pdf = canvas.Canvas(str(file_path), pagesize=A4)

    width, height = A4

    # Certificate title
    pdf.setFont("Helvetica-Bold", 28)
    pdf.drawCentredString(
        width / 2,
        height - 150,
        "CERTIFICATE OF PARTICIPATION"
    )

    # Main text
    pdf.setFont("Helvetica", 16)
    pdf.drawCentredString(
        width / 2,
        height - 230,
        "This certificate is proudly presented to"
    )

    # Recipient name
    pdf.setFont("Helvetica-Bold", 24)
    pdf.drawCentredString(
        width / 2,
        height - 280,
        recipient_name
    )

    # Event information
    pdf.setFont("Helvetica", 15)
    pdf.drawCentredString(
        width / 2,
        height - 340,
        f"For participating in {event_name}"
    )

    pdf.drawCentredString(
        width / 2,
        height - 375,
        f"Date: {event_date}"
    )

    # Certificate ID
    pdf.setFont("Helvetica", 10)
    pdf.drawCentredString(
        width / 2,
        80,
        f"Certificate ID: {certificate_id}"
    )

    pdf.save()

    return str(file_path)