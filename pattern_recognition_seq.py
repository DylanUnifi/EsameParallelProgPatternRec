from sklearn.datasets import load_iris
import numpy as np


# Chargement du jeu de données Iris
iris = load_iris()
data = iris.data
target = iris.target


def pattern_recognition(long_series, pattern):
    min_sad = float('inf')
    best_match_index = -1

    pattern_length = len(pattern)
    for i in range(len(long_series) - pattern_length + 1):
        current_pattern = long_series[i:i + pattern_length]
        sad = sum(abs(long_series_val - pattern_val) for long_series_val, pattern_val in zip(current_pattern, pattern))

        if min(sad) < min_sad:
            min_sad = min(sad)
            best_match_index = i

    if min_sad == float('inf'):
        return -1

    return best_match_index


# Exemple d'utilisation avec le jeu de données Iris
pattern = np.array([5.1, 3.5, 1.4, 0.2])  # Un exemple de motif à rechercher
long_series = data  # Utilisation des données Iris comme série

match_index = pattern_recognition(long_series, pattern)
if match_index != -1:
    print("Pattern trouvé à l'index :", match_index)
    print("Classe correspondante :", target[match_index])
else:
    print("Pattern non trouvé dans la série.")
