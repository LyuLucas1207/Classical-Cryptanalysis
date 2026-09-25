import math
import random
from pathlib import Path

# Playfair ciphertext: Assignment1/texts/ciphertexts_80.txt, line 1.
CIPHERTEXT = (
    "PRWAKPWAGBQYBHDWPSNQPOWKOZZQYCINQDQMAHFZMQMUZPDPIUMQLFNBRLON"
    "CSYCHUQBRLPGBOGPRGDPTVQWHABAGPWQBQHVHVMGKFRGXPKMGPHUVYLMLFSM"
    "BNKFHVVUMQTDPSYCWBUMKXKFZNQZRXHWCLBWHRQDVUMFTQKLDPVCDFOBUI"
    "BQGCXHBQSRESMYOMUKDPYPDPTVDPNUXQQBBEHPONFZOZKOZNQLONCHWKOL"
    "UZGPYVBUMQHKONVSVURXPVCSFUVUMQTDPSDPZAOGUMMQHTBOHGHDXKNVG"
    "PHTMQMU"
)

ALPHABET = "ABCDEFGHIKLMNOPQRSTUVWXYZ"
QUADGRAM_PATH = Path(__file__).with_name("english_quadgrams.txt")

# Simulated annealing. Quadgram scores are sums of log10 probabilities.
# On this 300-letter text, gibberish scores near -2000 and English near
# -1340, so T = 50 accepts almost every worse key. T = 12 matches that scale.
TEMPERATURE = 30.0
COOLING = 0.5
ITERATIONS = 2500
RESTARTS = 12
# Stop when a decryption scores above this.
ENGLISH_SCORE = -1500

# Key mutation probabilities. The last 2% shuffles SHUFFLE_COUNT letters.
P_SWAP_ROWS = 0.04
P_SWAP_COLUMNS = 0.04
P_SWAP_LETTERS = 0.90
SHUFFLE_COUNT = 4


# 1. Load English quadgram frequencies
def load_quadgrams(filename):
    counts = {}

    with open(filename, "r") as f:
        for line in f:
            quadgram, count = line.split()
            counts[quadgram] = int(count)

    total = sum(counts.values())

    scores = {
        quad: math.log10(count / total)
        for quad, count in counts.items()
    }

    # Penalty for unknown quadgrams
    floor = math.log10(0.01 / total)

    return scores, floor


QUADGRAMS, FLOOR = load_quadgrams(QUADGRAM_PATH)


# 2. Score decrypted text
def score_text(text):
    score = 0.0
    get = QUADGRAMS.get

    for i in range(len(text) - 3):
        score += get(text[i:i + 4], FLOOR)

    return score


# 3. Playfair decryption
def playfair_decrypt(ciphertext, key):
    # Store each letter's row and column
    positions = {
        letter: (i // 5, i % 5)
        for i, letter in enumerate(key)
    }

    plaintext = []

    for i in range(0, len(ciphertext), 2):
        a = ciphertext[i]
        b = ciphertext[i + 1]

        r1, c1 = positions[a]
        r2, c2 = positions[b]

        if r1 == r2:
            # Same row: move left
            c1 = (c1 - 1) % 5
            c2 = (c2 - 1) % 5

        elif c1 == c2:
            # Same column: move up
            r1 = (r1 - 1) % 5
            r2 = (r2 - 1) % 5

        else:
            # Rectangle: exchange columns
            c1, c2 = c2, c1

        plaintext.append(key[r1 * 5 + c1])
        plaintext.append(key[r2 * 5 + c2])

    return "".join(plaintext)


def playfair_encrypt(plaintext, key):
    positions = {
        letter: (i // 5, i % 5)
        for i, letter in enumerate(key)
    }

    ciphertext = []

    for i in range(0, len(plaintext), 2):
        a = plaintext[i]
        b = plaintext[i + 1]

        r1, c1 = positions[a]
        r2, c2 = positions[b]

        if r1 == r2:
            c1 = (c1 + 1) % 5
            c2 = (c2 + 1) % 5
        elif c1 == c2:
            r1 = (r1 + 1) % 5
            r2 = (r2 + 1) % 5
        else:
            c1, c2 = c2, c1

        ciphertext.append(key[r1 * 5 + c1])
        ciphertext.append(key[r2 * 5 + c2])

    return "".join(ciphertext)


# 4. Random key mutation
def mutate_key(key):
    key = list(key)
    operation = random.random()
    row_limit = P_SWAP_ROWS
    column_limit = row_limit + P_SWAP_COLUMNS
    letter_limit = column_limit + P_SWAP_LETTERS

    if operation < row_limit:
        # Swap two rows
        r1, r2 = random.sample(range(5), 2)

        for c in range(5):
            i = r1 * 5 + c
            j = r2 * 5 + c
            key[i], key[j] = key[j], key[i]

    elif operation < column_limit:
        # Swap two columns
        c1, c2 = random.sample(range(5), 2)

        for r in range(5):
            i = r * 5 + c1
            j = r * 5 + c2
            key[i], key[j] = key[j], key[i]

    elif operation < letter_limit:
        # Swap two letters
        i, j = random.sample(range(25), 2)
        key[i], key[j] = key[j], key[i]

    else:
        # Shuffle a few letters
        indices = random.sample(range(25), SHUFFLE_COUNT)
        letters = [key[i] for i in indices]
        random.shuffle(letters)

        for i, letter in zip(indices, letters):
            key[i] = letter

    return "".join(key)


# 5. Simulated annealing
def simulated_annealing(ciphertext, initial_key):
    temperature = TEMPERATURE
    current_key = initial_key
    current_plaintext = playfair_decrypt(ciphertext, current_key)
    current_score = score_text(current_plaintext)

    best_key = current_key
    best_score = current_score
    best_plaintext = current_plaintext

    while temperature > 0:
        for _ in range(ITERATIONS):
            new_key = mutate_key(current_key)

            new_plaintext = playfair_decrypt(ciphertext, new_key)
            new_score = score_text(new_plaintext)

            difference = new_score - current_score

            # Accept improvements, occasionally accept worse keys:
            # P = exp((S_new - S_old) / T)
            if difference >= 0 or random.random() < math.exp(
                difference / temperature
            ):
                current_key = new_key
                current_score = new_score

                if new_score > best_score:
                    best_key = new_key
                    best_score = new_score
                    best_plaintext = new_plaintext

        print(
            f"Temperature: {temperature:.1f} | "
            f"Best score: {best_score:.2f} | "
            f"Plaintext: {best_plaintext[:40]}"
        )

        if best_score > ENGLISH_SCORE:
            return best_key, best_score, best_plaintext

        temperature -= COOLING

    return best_key, best_score, best_plaintext


def format_matrix(key):
    return "\n".join(
        " ".join(key[i:i + 5]) for i in range(0, 25, 5)
    )


# 6. Execute multiple independent searches
if __name__ == "__main__":
    ciphertext = "".join(CIPHERTEXT.split())

    assert len(ciphertext) % 2 == 0
    assert all(c in ALPHABET for c in ciphertext)

    overall_best_score = float("-inf")
    overall_best_key = None
    overall_best_plaintext = None

    for run in range(RESTARTS):
        # First run uses the alphabetical matrix.
        # Later runs start from randomized matrices.
        if run == 0:
            initial_key = ALPHABET
        else:
            initial_key = "".join(random.sample(ALPHABET, 25))

        key, score, plaintext = simulated_annealing(ciphertext, initial_key)

        if score > overall_best_score:
            overall_best_score = score
            overall_best_key = key
            overall_best_plaintext = plaintext

        print(f"\nCompleted run {run + 1}/{RESTARTS}")
        print("Key:", key)
        print("Score:", score)
        print("Plaintext:", plaintext[:80])

        if overall_best_score > ENGLISH_SCORE:
            break

    print("\n========== BEST RESULT ==========")
    print("Key:", overall_best_key)
    print("Score:", overall_best_score)
    print("Plaintext:", overall_best_plaintext)
    print("\nKey Matrix:")
    print(format_matrix(overall_best_key))

    recovered = playfair_encrypt(overall_best_plaintext, overall_best_key)
    print("\nRe-encrypt matches ciphertext:", recovered == ciphertext)
