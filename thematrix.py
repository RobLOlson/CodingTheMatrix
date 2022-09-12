def cartesian_product(a: set, b: set) -> list[tuple]:
    """Return the cartesian product of two sets."""
    return [(x, y) for x in a for y in b]


def makeInverseIndex(strlist: list[str]) -> dict[str, set]:
    words = {elem for elem in " ".join(strlist).split(" ")}
    inverse_index = {
        word: {i for i, doc in enumerate(strlist) if word in doc} for word in words
    }
    return inverse_index


def orSearch(inverse_index: dict[str, set[int]], query: list[str]) -> set | list:
    indeces: set[int] = set()
    for word in query:
        indeces = indeces | inverse_index[word]

    return indeces


def andSearch(inverse_index: dict[str, set[int]], query: list[str]) -> set | list:
    indeces: set[int] = set()
    for word in query:
        if not indeces:
            indeces = indeces | inverse_index[word]
        else:
            indeces = indeces & inverse_index[word]

    return indeces


def invert_dict(target: dict) -> dict:
    return {value: key for key, value in target.items()}


def main():
    pass


if __name__ == "__main__":
    main()
