from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from io import BytesIO
import datetime

class SecurityReportGenerator:
    """Utility to generate professional PDF security reports."""

    @staticmethod
    def generate_pdf(analysis_data, recommendations, risk_score):
        """Generate a PDF report in memory and return the BytesIO object."""
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        styles = getSampleStyleSheet()

        # Custom styles
        title_style = ParagraphStyle(
            'TitleStyle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor("#4F46E5"),
            spaceAfter=20,
            alignment=1
        )

        section_style = ParagraphStyle(
            'SectionStyle',
            parent=styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor("#1F2937"),
            spaceBefore=15,
            spaceAfter=10
        )

        # Document elements
        elements = []

        # Header
        elements.append(Paragraph("Cyberlson Scan Security Audit Report", title_style))
        elements.append(Paragraph(f"Generated on: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", styles['Normal']))
        elements.append(Spacer(1, 20))

        # Risk Score Section
        elements.append(Paragraph("Overall Risk Assessment", section_style))

        color_map = {
            "Low": colors.green,
            "Medium": colors.orange,
            "High": colors.red
        }

        risk_style = ParagraphStyle(
            "RiskStyle",
            parent=styles["Normal"],
            textColor=color_map.get(risk_score, colors.black),
            fontName="Helvetica-Bold"
        )

        elements.append(
            Paragraph(f"Summary Risk Level: {risk_score}", risk_style)
        )
        elements.append(Spacer(1, 15))

        # System Info Table
        elements.append(Paragraph("System Environment Overview", section_style))
        sys_info = analysis_data.get('system_info', {})
        data = [
            ["Metric", "Value"],
            ["Operating System", sys_info.get('os', 'N/A')],
            ["Hostname", sys_info.get('hostname', 'N/A')],
            ["CPU Usage", f"{sys_info.get('cpu', sys_info.get('cpu_usage', 0))}%"],
            ["Memory Usage", f"{sys_info.get('memory', sys_info.get('memory_usage', 0))}%"],
            ["Disk Usage", f"{sys_info.get('disk_usage', 0)}%"],
            ["Boot Time", sys_info.get('boot_time', 'N/A')]
        ]

        t = Table(data, colWidths=[150, 300])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#4F46E5")),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor("#F3F4F6")),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor("#D1D5DB"))
        ]))
        elements.append(t)
        elements.append(Spacer(1, 20))

        # Recommendations Section
        elements.append(Paragraph("Detailed Security Recommendations", section_style))
        risk_color_map = {"High": "red", "Medium": "orange", "Low": "green"}
        for rec in recommendations:
            rec_text = f"<b>[{rec['category']}]</b>: {rec['recommendation']} (<font color='{risk_color_map.get(rec['risk_level'], 'black')}'>{rec['risk_level']}</font>)"
            elements.append(Paragraph(rec_text, styles['Normal']))
            elements.append(Spacer(1, 8))

        # Footer/Disclaimer
        elements.append(Spacer(1, 40))
        elements.append(Paragraph("Educational Disclaimer", styles['Heading4']))
        elements.append(Paragraph(
            "This report is for educational and personal defensive auditing purposes only. "
            "It is not a substitute for a professional security audit. "
            "Always follow security best practices from your vendor.",
            styles['Italic']
        ))

        doc.build(elements)
        buffer.seek(0)
        return buffer