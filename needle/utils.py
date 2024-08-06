from urllib.parse import urlparse, urlunparse


def make_needle_search_url(needle_url: str):
    parsed_url = urlparse(needle_url)
    new_netloc = f"search.{parsed_url.netloc}"
    return urlunparse(parsed_url._replace(netloc=new_netloc))
