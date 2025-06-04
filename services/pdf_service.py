from weasyprint import HTML


def text_to_pdf(text: str, pdf_path: str) -> None:
    with open("output.txt", "r", encoding="utf-8") as f:
        bengali_text = f.read()

    html_content = f"""
    <!DOCTYPE html>
    <html lang="bn">
    <head>
        <meta charset="utf-8">
        <style>
            @font-face {{
                font-family: 'Noto Sans Bengali';
                src: url('NotoSansBengali-Regular.ttf') format('truetype');
            }}
            body {{
                font-family: 'Noto Sans Bengali', sans-serif;
                font-size: 16px;
                line-height: 1.6;
                white-space: pre-wrap;
            }}
        </style>
    </head>
    <body>
    {bengali_text}
    </body>
    </html>
    """
    HTML(string=html_content).write_pdf("output.pdf")
