import markdown2
from weasyprint import HTML

def generate_report(path):
    # Convert markdown to HTML
    with open(path, "r", encoding="utf-8") as f:
        md = f.read()
    html = markdown2.markdown(md)

    # Convert HTML to PDF
    HTML(string=html).write_pdf("ux_report.pdf")

if __name__ == "__main__":
    generate_report("ux_report_us_4.md")
    print("📄 PDF report generated as 'ux_report.pdf'")