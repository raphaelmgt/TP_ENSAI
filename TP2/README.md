# TP2- ENSAI

> Ce code permet de créer divers index à partir d'un jeu de données de différents produits e-commerce.

---

## Description globale

On retrouve ici deux fichiers :
    - un notebook `TP.ipynb`,
    - et un fichier python `TP2.py`

Le notebook représente simplement la base que j'ai utiliser pour tester mon code au fur et à mesure de la rédaction. Les deux fichiers ont globalement le même contenu. 

---


## Prérequis

- !python -m spacy download en_core_web_md
- packages : urllib

---


## Présentation de la structure de chaque index

    - brand et origin index: L'index inversé associe chaque token à la liste des URL des documents dans lesquels il apparaît.

    - description et title index: L'index inversé associe chaque token à la liste des URL des documents dans lesquels il apparaît mais aussi sa position dans le document.

    - reviews index : Pour chaque URL est associé le nombre total d'avis, la note moyenne ainsi que la note la plus récente. 

## Comment produire les index ?

Pour produire les tous les index demandés à partir du fichier `TP2/input/products.jsonl`, il suffit simplement d'exécuter le fichier `TP2.py`.

Il est aussi possible de réaliser cela index par index via des lignes de commandes. Par exemple pour réaliser un index associé aux marques, il faut exécuter le code suivant :

```python
doc_products = read_jsonl(path="TP2/input/products.jsonl")
save_index_brand(index_brand=create_index_brand(doc_products))

```
