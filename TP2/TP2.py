import json
import re
import spacy
from urllib.parse import urlparse, parse_qs
from collections import defaultdict

# 1. Reading and processing the URL

path = "TP2/input/products.jsonl"


def read_jsonl(path: str) -> list[dict]:
    """
    This function read a jsonl file.

    Args:
        path (str): The path that leads to the file

    Returns:
        list[dict]: The file
    """

    input = []

    with open(path, "r", encoding="utf-8") as f:

        for line in f:
            input.append(json.loads(line))

    return input


doc_products = read_jsonl(path=path)


def extract_product_info(url: str) -> dict:
    """
    Extracts the product ID and variant from a product URL.

    Args:
        url (str): Product URL

    Returns:
        dict: {
            "product_id": int,
            "variant": str | None
        }
    """
    parsed_url = urlparse(url)

    # Extract the product ID from the path
    match = re.search(r"/product/(\d+)", parsed_url.path)
    product_id = int(match.group(1)) if match else None

    # Extract the variant from the query parameters
    query_params = parse_qs(parsed_url.query)
    variant = query_params.get("variant", [None])[0]

    # Return the result in a dict
    return {
        "product_id": product_id,
        "variant": variant
    }


# 2. Creating inverted indexes

nlp = spacy.load("en_core_web_md")


def create_token(text: str) -> list[str]:
    """
    Tokenizes a text by removing stop words and punctuation.

    Args:
        title (str): Text to be tokenized

    Returns:
        list[str]: Tokenized text
    """

    doc = nlp(text.lower())

    tokens = [
        token.text
        for token in doc
        if not token.is_stop and not token.is_punct
    ]

    return tokens


def get_position_from_tokens(tokens: list) -> list[tuple]:
    """
    Associates each token with its position in the list.

    Args:
        tokens (List[str]): List of tokens

    Returns:
        List[Tuple[str, int]]: Tuples (token, index)
    """

    return [
        (token, position)
        for position, token in enumerate(tokens)
    ]


def create_inverted_index_for_title(documents: list) -> dict:
    """
    Creates an inverted index for the title of each document.

    Args:
        documents (list): All the documents

    Returns:
        dict: The inverted index associated with the titles
    """

    index = defaultdict(lambda: defaultdict(list))

    for document in documents:
        url = document["url"]
        titre = document["title"]
        tokens = create_token(titre)
        mots_positions = get_position_from_tokens(tokens)

        for mot, position in mots_positions:
            index[mot][url].append(position)

    return index


def save_index_title(index_title: dict):
    """
    Saves the index for the title in a json file.

    Args:
        index_title (list): The title index
    """

    with open("TP2/title_index.json", 'w') as file:
        json.dump(index_title, file, indent=4)


save_index_title(index_title=create_inverted_index_for_title(doc_products))


def create_inverted_index_for_description(documents: dict) -> dict:
    """
    Creates an inverted index for the description of each document.

    Args:
        documents (list): All the documents

    Returns:
        dict: The inverted index associated with the descriptions
    """

    index = defaultdict(lambda: defaultdict(list))

    for document in documents:
        url = document["url"]
        description = document["description"]
        tokens = create_token(description)
        mots_positions = get_position_from_tokens(tokens)

        for mot, position in mots_positions:
            index[mot][url].append(position)

    return index


def save_index_description(index_description: dict):
    """
    Saves the index for the description in a json file.

    Args:
        index_title (list): The description index
    """

    with open("TP2/description_index.json", 'w') as file:
        json.dump(index_description, file, indent=4)


save_index_description(
    index_description=create_inverted_index_for_description(doc_products)
)


# 3. Index of reviews


def get_average_rating_reviews(reviews: list) -> float:
    """
    Compute the average rate of reviews.

    Args:
        reviews (list): All the reviews

    Returns:
        float: The average rating
    """

    total_reviews = len(reviews)

    total_rating = 0

    for feedback in reviews:
        total_rating += feedback["rating"]

    return total_rating / total_reviews


def extract_ratings_from_reviews(reviews: dict) -> dict:
    """
    Extracts the total number of reviews, the
    average and the last rating from a givens
    set of reviews.

    Args:
        reviews (str): All the reviews

    Returns:
        dict: {
            "total_reviews": int,
            "average_rating": int,
            "last_rating": int
        }
    """

    total_reviews = len(reviews)
    if total_reviews == 0:
        return {"total_reviews": 0, "average_rating": 0, "last_rating": None}

    average_rating = get_average_rating_reviews(reviews=reviews)

    last_rating = reviews[-1]["rating"]

    return {
        "total_reviews": total_reviews,
        "average_rating": average_rating,
        "last_rating": last_rating
    }


def create_index_reviews(reviews: dict):
    """
    Creates an index for the reviews of each document.

    Args:
        documents (list): All the documents

    Returns:
        dict: The index associated with the reviews
    """

    all_index = {}

    for i in range(len(reviews)):

        url = reviews[i]["url"]
        all_index[url] = extract_ratings_from_reviews(
            reviews=reviews[i]["product_reviews"]
        )

    return all_index


def save_index_reviews(index_reviews: dict):
    """
    Saves the index for the reviews in a json file.

    Args:
        index_reviews (list): The reviews index
    """

    with open("TP2/reviews_index.json", 'w') as file:
        json.dump(index_reviews, file, indent=4)


save_index_reviews(index_reviews=create_index_reviews(doc_products))


# 4. Index of features

def create_index_origin(documents: list) -> dict:
    """
    Creates an index for the origin of each document.

    Args:
        documents (list): All the documents

    Returns:
        dict: The index associated with the origin
    """

    index_origin = defaultdict(list)

    for document in documents:
        if "made in" in document["product_features"].keys():
            origin = document["product_features"]["made in"].lower()

            index_origin[origin].append(document["url"])

    return index_origin


def save_index_origin(index_origin: dict):
    """
    Saves the index for the reviews in a json file.

    Args:
        index_reviews (list): The origin index
    """

    with open("TP2/origin_index.json", 'w') as file:
        json.dump(index_origin, file, indent=4)


save_index_origin(index_origin=create_index_origin(doc_products))


def create_index_brand(documents: list) -> dict:
    """
    Creates an index for the brands of each document.

    Args:
        documents (list): All the documents

    Returns:
        dict: The index associated with the brands
    """

    index_brand = defaultdict(list)

    for document in documents:
        if "brand" in document["product_features"].keys():
            brand = document["product_features"]["brand"].lower()

            index_brand[brand].append(document["url"])

    return index_brand


def save_index_brand(index_brand: dict):
    """
    Saves the index for the brands in a json file.

    Args:
        index_reviews (list): The origin index
    """

    with open("TP2/brand_index.json", 'w') as file:
        json.dump(index_brand, file, indent=4)


save_index_brand(index_brand=create_index_brand(doc_products))
