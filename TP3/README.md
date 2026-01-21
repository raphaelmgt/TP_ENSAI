# TP3- ENSAI

> Ce programme permet, à partir d'index préétablis, de classer différentes URL en fonction de leur pertinence pour répondre à une query.

---


## 📦 Prérequis

- unicodedata
- !python -m spacy download en_core_web_md
- 

---


## Explication de l'étape de ranking

Signaux considérés:

    - La fréquence de chaque token dans les documents.

    - La presence dans le titre vs la presence dans la description : Ici, j'ai associé un poids plus élevé pour le titre (en plus d'ajouter un cas si tous les tokens y étaient présent). Cela mène à de meilleurs résultats de mon point de vue.

    - Les reviews : Je n'ai considéré que la note moyenne et la dernière note reçue pour chaque page. La quasi totalité des document comporte entre 4 et 5 avis. J'ai donc considéré le nombre total de review comme non pertinent dans ce cas.

Point négatif : Je n'ai malheureusement pas réussi à implémenter la fonction qui calcule le score BM25 à partir de la fonction BM25Okapi à partir de la librairie rank_bm25.