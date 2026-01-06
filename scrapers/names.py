import random
import requests
from collections import Counter

FIRST_NAME_URL = "https://raw.githubusercontent.com/dominictarr/random-name/master/first-names.txt"
LAST_NAME_URL = "https://raw.githubusercontent.com/dominictarr/random-name/master/names.txt"


def _load_names(url):
    response = requests.get(url, timeout=10)
    response.raise_for_status()

    names = [
        line.strip().title()
        for line in response.text.splitlines()
        if line.strip()
    ]

    # Uniform frequency (acceptable + realistic enough for enterprise data)
    return Counter(names)


def generate_full_names(n):
    first_names = _load_names(FIRST_NAME_URL)
    last_names = _load_names(LAST_NAME_URL)

    first_list, first_weights = zip(*first_names.items())
    last_list, last_weights = zip(*last_names.items())

    first_sample = random.choices(first_list, weights=first_weights, k=n)
    last_sample = random.choices(last_list, weights=last_weights, k=n)

    return [f"{f} {l}" for f, l in zip(first_sample, last_sample)]
