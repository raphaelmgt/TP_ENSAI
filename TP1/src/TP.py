import urllib.parse
import urllib.request
import urllib.robotparser
import urllib
from bs4 import BeautifulSoup
import json
import time

DELAY = 1.5


# 2. Extracting the content

def is_allowed(user_agent: str, url: str) -> bool:
    """
    Tells if the crawler has the right to parse
     a given page.

    Args:
        url (str): The URL of the page

    Returns:
        bool
    """
    robot_parser = urllib.robotparser.RobotFileParser()
    return robot_parser.can_fetch(useragent=user_agent, url=url)


def extract_title(url: str) -> str:
    """
    Extracts the title of a document.

    Args:
        url (str): The URL of the document

    Returns:
        str: The title of the document
    """

    request_url = urllib.request.urlopen(url=url)
    soup = BeautifulSoup(request_url, 'html.parser')

    return soup.title.get_text(strip=True)


def extract_links(url: str) -> list[str]:
    """
    Extracts the links of a document.

    Args:
        url (str): The URL of the document

    Returns:
        list[str]: All the links of the document
    """

    links = []
    request_url = urllib.request.urlopen(url=url)
    soup = BeautifulSoup(request_url, 'html.parser')

    links_extraction = soup.find_all('a', href=True)

    for link in links_extraction:
        href = urllib.parse.urljoin(url, link["href"])
        links.append(href)

    return links


def extract_first_paragraph(url: str):
    """
    Extracts the first paragraph of a document.

    Args:
        url (str): The URL of the document

    Returns:
        str: The first paragraph of the document
    """

    # We retrieve the content of the page
    request_url = urllib.request.urlopen(url=url)
    soup = BeautifulSoup(request_url, 'html.parser')

    # We retrieve the first paragraph (first <p>)
    first_paragraph = soup.find('p')

    if first_paragraph:
        return first_paragraph.get_text(strip=True)

    return first_paragraph


# 3. Crawling logic


def contains_token_product(url: str) -> bool:
    """
    Tells if a given URL contains the token 'product'.

    Args:
        url (str): The URL

    Returns:
        bool
    """

    parsed_url = urllib.parse.urlparse(url)

    return 'product' in parsed_url.path


def get_priority(url: str) -> int:
    """
    Gives a priority score to an URL.

    Args:
        url (str): The URL

    Returns:
        int (0 or 1): The priority score.
    """

    return 0 if contains_token_product(url=url) else 1


def get_priority_for_all_url(urls: list) -> dict:
    """
    Gives a priority score to all URL.

    Args:
        url (str): The list of URLs

    Returns:
        dict: The dict of all URLs with their priority
    """

    scores = {}

    for url in urls:
        scores[url] = get_priority(
            url=url
        )

    return scores


def get_queue(urls: list) -> list:
    """
    Orders a given list of URLS according to the
    priority criterion (if the URL contains the
    token 'product').

    Args:
        urls (list): The list of URLS

    Returns:
        list: The ordered list
    """

    queue = get_priority_for_all_url(
            urls=urls
    )

    return sorted(queue, key=queue.get, reverse=False)


def extract_informations_from_url(url: str) -> dict:
    """
    Extracts all the informations of a document.

    Args:
        url (str): The URL of the document

    Returns:
        dict: {
            "url": str,
            "title": str,
            "description": str,
            "links": list[str]
        }
    """

    title = extract_title(url=url)
    description = extract_first_paragraph(url=url)
    links = extract_links(url=url)

    return {
        "url": url,
        "title": title,
        "description": description,
        "links": links
    }


def crawler(starting_url: str, max_pages: int = 50) -> list:

    result_crawler = []

    # First we extract the content of the starting url
    result_crawler.append(
        extract_informations_from_url(url=starting_url)
    )

    # We then extract and order the list of all url of the document
    urls_to_visit = extract_links(starting_url)
    urls_to_visit = get_queue(urls=urls_to_visit)

    i = 1

    while i < max_pages:

        # Politeness to the servers
        time.sleep(DELAY)

        url = urls_to_visit[0]

        # We make sure that we only extract different URLS
        if url in [page["url"] for page in result_crawler]:
            urls_to_visit.remove(url)

        else:

            # We extract the informations
            result_crawler.append(
                extract_informations_from_url(url=url)
            )

            # We update and order the list of all the URLS to visit
            urls_to_visit = get_queue(
                urls=urls_to_visit + extract_links(url=url)
            )

            i += 1

    return result_crawler


def save_result(result: list):
    """
    Saves the index for the brands in a json file.

    Args:
        index_reviews (list): The origin index
    """

    with open("TP1/products.jsonl", 'w') as file:
        for item in result:
            file.write(json.dumps(item, ensure_ascii=False) + "\n")


save_result(
    result=crawler("https://web-scraping.dev/product/13", max_pages=20)
)
