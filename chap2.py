from vec import Vec, zero_vec

NEEDLE = [1, -1, 1, 1, -1, 1]
HAYSTACK = [1, -1, 1, 1, 1, -1, 1, 1, 1]
DEMOCRATS = [
    elem.split(" ")[0]
    for elem in open("voting_record_dump109.txt", "r").readlines()
    if elem.split(" ")[1] == "D"
]
REPUBLICANS = [
    elem.split(" ")[0]
    for elem in open("voting_record_dump109.txt", "r").readlines()
    if elem.split(" ")[1] == "R"
]


def segment(u: list | tuple, v: list | tuple, n: int = 100) -> list:
    """Generate a sequence of n convex combinations of vectors u and v."""
    n -= 1
    return [
        tuple(u_0 * alpha / n + v_0 * (n - alpha) / n for u_0, v_0 in zip(u, v))
        for alpha in range(n, -1, -1)
    ]


def dot_product_list(needle: list, haystack: list) -> list:
    return [
        sum(
            needle[i] * haystack[offset : offset + len(needle)][i]
            for i in range(len(needle))
        )
        for offset in range(len(haystack) - len(needle) + 1)
    ]


def triangular_solve_n(rowlist: list[Vec], b):
    D = rowlist[0].D
    n = len(D)
    assert D == set(range(n))
    x = zero_vec(D)

    for i in reversed(range(n)):
        x[i] = (b[i] - rowlist[i] * x) / rowlist[i][i]

    return x


def triangular_solve(rowlist, label_list, b):
    D = rowlist[0].D
    x = zero_vec(D)

    for j in reversed(range(len(D))):
        c = label_list[j]
        row = rowlist[j]
        x[c] = (b[j] - x * row) / row[c]

    return x


def create_voting_dict(strlist: list[str]):
    result = {}
    for senator in strlist:
        sen = senator.split(" ")
        result[f"{sen[0]}"] = list(map(int, sen[3:]))

    return result


def policy_compare(sen_a: str, sen_b: str, voting_dict: dict[str, list[int]]) -> int:
    return Vec.from_list(voting_dict[sen_a]) * Vec.from_list(voting_dict[sen_b])


def most_similar_senator(sen_a: str, voting_dict: dict[str, list[int]]) -> str:
    best = 0
    result = sen_a
    for candidate in voting_dict.keys():
        if candidate == sen_a:
            break
        if trial := policy_compare(sen_a, candidate, voting_dict) > best:
            best = trial
            result = candidate

    return result


def least_similar_senator(sen_a: str, voting_dict: dict[str, list[int]]) -> str:
    best = policy_compare(sen_a, sen_a, voting_dict)
    result = sen_a
    for candidate in voting_dict.keys():
        if candidate == sen_a:
            break
        if trial := policy_compare(sen_a, candidate, voting_dict) < best:
            best = trial
            result = candidate

    return result


def find_average_similarity(
    sen: str, sen_set: list[str] | set[str], voting_dict: dict[str, list[int]]
) -> float:
    total = 0
    sen_set = set(sen_set) - set(sen)  # Do not compare sen to himself
    N = len(sen_set)
    for senator in sen_set:
        total += policy_compare(sen, senator, voting_dict)

    return total / N


def find_average_record(
    sen_set: list[str] | set[str], voting_dict: dict[str, list[int]]
) -> list[float]:
    votes = [Vec.from_list(voting_dict[sen]) for sen in sen_set]
    avg = zero_vec(votes[0].D)
    for vote in votes:
        avg = avg + vote

    return avg / len(votes)


def bitter_rivals(voting_dict, n: int = 1):
    """Return the n most bitter (negative dot product) voting record pairs."""
    return sorted(
        list(
            set(
                (policy_compare(x, y, voting_dict), ", ".join(sorted([x, y])))
                for x in voting_dict.keys()
                for y in voting_dict.keys()
            )
        )
    )[:n]
