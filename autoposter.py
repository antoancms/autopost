import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


def fetch_article(url: str) -> str:
    """Fetch raw text from an article URL."""
    resp = requests.get(url, timeout=10)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")
    paragraphs = [p.get_text(strip=True) for p in soup.find_all("p")]
    return "\n\n".join(paragraphs)


def summarize(text: str, max_words: int = 200) -> str:
    """Naively summarize text to a given word count."""
    words = text.split()
    return " ".join(words[:max_words])


def post_to_wordpress(
    site_url: str,
    username: str,
    app_password: str,
    title: str,
    content: str,
) -> dict:
    """Post content to a WordPress site using the REST API.

    Returns the JSON response from WordPress.
    """
    api_url = urljoin(site_url, "/wp-json/wp/v2/posts")
    payload = {"title": title, "content": content, "status": "publish"}
    headers = {"Content-Type": "application/json"}
    resp = requests.post(api_url, json=payload, auth=(username, app_password), headers=headers, timeout=10)
    resp.raise_for_status()
    return resp.json()
