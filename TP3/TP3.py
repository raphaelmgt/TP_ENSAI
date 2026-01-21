import json
import spacy
import unicodedata
import re


def import_index(path: str):
    """
    This function read a json file.

    Args:
        path (str): The path that leads to the file

    Returns:
        dict: The imported file
    """

    with open(path, "r", encoding="utf-8") as f:
        index = json.load(f)

    return index


brand_index = import_index(path="TP3/input/brand_index.json")
description_index = import_index(path="TP3/input/description_index.json")
origin_index = import_index(path="TP3/input/origin_index.json")
origin_synonyms = import_index(path="TP3/input/origin_synonyms.json")
reviews_index = import_index(path="TP3/input/reviews_index.json")
title_index = import_index(path="TP3/input/title_index.json")


nlp = spacy.load("en_core_web_md")


def create_token(query: str):
    doc = nlp(query.lower())

    tokens = [
        token.text
        for token in doc
        if not token.is_stop and not token.is_punct
    ]

    return tokens


def normalize_query(query: str) -> list[str]:
    """
    Normalize a given query (removes special
    characters, punctuation and spaces)

    Args:
        query (str): The query that we want to normalize

    Returns:
        list[str]: The list of all words of the query
    """

    query = query.strip().lower()
    query = "".join(
        c for c in unicodedata.normalize("NFD", query)
        if unicodedata.category(c) != "Mn"
    )
    query = re.sub(r"\s+", " ", query)
    return query.split(" ")


def find_token_in_brand_index(tokens: list, url: str) -> list[bool]:
    """
    For each word, this function tells if it is in the
    brand of the document.

    Args:
        tokens (list): List of words

        url (str): The url of the document

    Returns:
        list[bool]: List of bool
    """

    presence_token = []

    for token in tokens:
        if token in brand_index.keys():

            if url in brand_index[token]:
                presence_token.append(True)

            else:
                presence_token.append(False)

    return presence_token


def find_token_in_description_index(tokens: list, url: str) -> list[bool]:
    """
    For each word, this function tells if it is in the
    description of the document.

    Args:
        tokens (list): List of words

        url (str): The url of the document

    Returns:
        list[bool]: List of bool
    """

    presence_token = []

    for token in tokens:
        if token in description_index.keys():

            if url in description_index[token]:
                presence_token.append(True)

            else:
                presence_token.append(False)

    return presence_token


def find_token_in_origin_index(tokens: list, url: str) -> list[bool]:
    """
    For each word, this function tells if it is in the
    origin of the document.

    Args:
        tokens (list): List of words

        url (str): The url of the document

    Returns:
        list[bool]: List of bool
    """

    presence_token = []

    for token in tokens:
        if token in origin_index.keys():

            if url in origin_index[token]:
                presence_token.append(True)

            else:
                presence_token.append(False)

    return presence_token


def find_token_in_title_index(tokens: list, url: str) -> list[bool]:
    """
    For each word, this function tells if it is in the
    title of the document.

    Args:
        tokens (list): List of words

        url (str): The url of the document

    Returns:
        list[bool]: List of bool
    """

    presence_token = []

    for token in tokens:
        if token in brand_index.keys():

            if url in brand_index[token]:
                presence_token.append(True)

            else:
                presence_token.append(False)

    return presence_token


# 3. Ranking


documents = []
with open("TP3/rearranged_products.jsonl", "r", encoding="utf-8") as f:
    for line in f:
        documents.append(json.loads(line))


def get_score_presence_brand(tokens: list, url: str):
    """
    This function computes the score associated with
    the presence of each token in the brand of a given
    document.

    Args:
        tokens (list): List of words

        url (str): The url of the document

    Returns:
        int: The score
    """

    brand_weight = 3

    presence_brand = find_token_in_brand_index(
        tokens=tokens,
        url=url
    )

    return brand_weight*sum(presence_brand)


def get_score_presence_description(tokens: list, url: str):
    """
    This function computes the score associated with
    the presence of each token in the description of
    a given document.

    Args:
        tokens (list): List of words

        url (str): The url of the document

    Returns:
        int: The score
    """

    description_weight = 4

    presence_description = find_token_in_description_index(
        tokens=tokens,
        url=url
    )

    return description_weight*sum(presence_description)


def get_score_presence_origin(tokens: list, url: str):
    """
    This function computes the score associated with
    the presence of each token in the origin country
    of a given document.

    Args:
        tokens (list): List of words

        url (str): The url of the document

    Returns:
        int: The score
    """

    origin_weight = 3.5

    presence_origin = find_token_in_origin_index(
        tokens=tokens,
        url=url
    )

    return origin_weight*sum(presence_origin)


def get_score_presence_title(tokens: list, url: str):
    """
    This function computes the score associated with
    the presence of each token in the title of
    a given document.

    Args:
        tokens (list): List of words

        url (str): The url of the document

    Returns:
        int: The score
    """

    title_weight = 6

    presence_title = find_token_in_title_index(
        tokens=tokens,
        url=url
    )

    if all(x == True for x in presence_title):
        return title_weight*(sum(presence_title) + 1)

    return title_weight*sum(presence_title)


def get_score_rewiews(url: str):
    """
    This function computes the score associated with
    the marks of a given document.

    Args:
        url (str): The url of the document

    Returns:
        int: The score
    """

    review = reviews_index[url]

    return review["mean_mark"] + review["last_rating"]


def get_score_presence_all(query: str, url: str):

    tokens = normalize_query(query=query)

    score_brand = get_score_presence_brand(
        tokens=tokens,
        url=url
    )

    score_description = get_score_presence_description(
        tokens=tokens,
        url=url
    )

    score_origin = get_score_presence_origin(
        tokens=tokens,
        url=url
    )

    score_title = get_score_presence_title(
        tokens=tokens,
        url=url
    )

    score_reviews = get_score_rewiews(url=url)

    # We compute the score associated

    score = (
        score_brand +
        score_description +
        score_origin +
        score_title +
        score_reviews
    )

    return score


def get_score_for_all_url(query: str, documents: list):

    scores = {}

    for document in documents:
        scores[document["url"]] = get_score_presence_all(
            query=query,
            url=document["url"]
        )

    return scores


query = "Energy drink"

data = get_score_for_all_url(query=query, documents=documents)

sorted_urls = sorted(data, key=data.get, reverse=True)

print(sorted_urls)