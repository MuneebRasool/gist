from bs4 import BeautifulSoup


def get_text_from_html(html_content):
    soup = BeautifulSoup(html_content, "html.parser")

    # Remove tracking images (usually width="1" height="1")
    for img in soup.find_all("img", {"width": "1", "height": "1"}):
        img.decompose()

    # Extract clean text from parsed HTML
    clean_text = soup.get_text(separator="\n", strip=True)

    # Display extracted text
    return clean_text
