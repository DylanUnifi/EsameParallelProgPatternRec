import concurrent.futures
import numpy as np
from sklearn.datasets import load_iris

# Chargement du jeu de données Iris
iris = load_iris()
data = iris.data
target = iris.target


def calculate_sad(long_series, pattern, start_index):
    pattern_length = len(pattern)
    current_pattern = long_series[start_index:start_index + pattern_length]
    return sum(abs(long_series_val - pattern_val) for long_series_val, pattern_val in zip(current_pattern, pattern))


def pattern_recognition_parallel(long_series, pattern):
    min_sad = float('inf')
    best_match_index = -1
    pattern_length = len(pattern)

    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_to_index = {executor.submit(calculate_sad, long_series, pattern, i): i for i in
                           range(len(long_series) - pattern_length + 1)}

        for future in concurrent.futures.as_completed(future_to_index):
            index = future_to_index[future]
            sad = future.result()
            minimum = min(sad)
            if minimum < min_sad:
                min_sad = minimum
                best_match_index = index

    if min_sad == float('inf'):
        return -1

    return best_match_index


# Exemple d'utilisation avec le jeu de données Iris
pattern = np.array([5.1, 3.5, 1.4, 0.2])  # Un exemple de motif à rechercher
long_series = data  # Utilisation des données Iris comme série

match_index = pattern_recognition_parallel(long_series, pattern)
if match_index != -1:
    print("Pattern trouvé à l'index :", match_index)
    print("Classe correspondante :", target[match_index])
else:
    print("Pattern non trouvé dans la série.")
