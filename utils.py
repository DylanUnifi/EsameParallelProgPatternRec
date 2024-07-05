import numpy as np
import pandas as pd
import random
import time
import asyncio


def calculate_sad(series1, series2):
    """
    Calcule la somme des différences absolues (SAD) entre deux séries temporelles.
    """
    return np.sum(np.abs(np.array(series1) - np.array(series2)))


def load_data(filename):
    try:
        # Utilisation de on_bad_lines='skip' pour ignorer les lignes mal formées
        df = pd.read_csv(filename, header=None, on_bad_lines='skip')
        # Supprimer la première ligne
        df = df.iloc[1:, :]
        # Supprimer la première colonne et nettoyer les cellules pour ne garder que les chiffres
        df = df.iloc[:, 1:].applymap(lambda y: ''.join(filter(lambda z: z.isdigit() or z == '.' or z == '-', str(y))))
        # Convertir les cellules en nombres à virgule flottante
        df = df.apply(pd.to_numeric, errors='coerce')
        # Convertir le DataFrame en une liste de listes de nombres
        data = df.values.tolist()
        return data
    except FileNotFoundError:
        print(f"Fichier '{filename}' non trouvé.")
        return []
    except Exception as e:
        print(f"Erreur lors du chargement des données à partir de '{filename}': {str(e)}")
        return []


def clean_series(series, series_length):
    # Enlever les valeurs NaN de la série
    cleaned_series = [x for x in series if not np.isnan(x)]
    # Compléter la série avec des zéros si elle est plus courte que series_length
    if len(cleaned_series) < series_length:
        cleaned_series.extend([0] * (series_length - len(cleaned_series)))
    return cleaned_series


def generate_random_dataset(original_data, num_series, series_length):
    random_dataset = []
    while len(random_dataset) < num_series:
        # Sélectionner aléatoirement une série
        series = random.choice(original_data)
        # Nettoyer la série en enlevant les valeurs NaN
        cleaned_series = clean_series(series, series_length)
        # Vérifier si la série nettoyée a une longueur suffisante
        if len(cleaned_series) >= series_length:
            # Sélectionner une sous-série aléatoire de la longueur spécifiée
            start_index = random.randint(0, len(cleaned_series) - series_length)
            random_series = cleaned_series[start_index:start_index + series_length]
            random_dataset.append(random_series)
    return random_dataset


# Fonction pour mesurer le temps d'exécution d'une fonction
def measure_execution_time(func):
    start = time.time()
    func()
    end = time.time()
    return end - start


# Fonction pour mesurer le temps d'exécution d'une fonction asynchrone
async def measure_execution_time_async(func):
    start = time.time()
    await func()
    end = time.time()
    return end - start


# Fonction asynchrone pour traiter une série temporelle
async def process_series(i, series, target_series):
    local_min_sad = float('inf')
    local_best_index = -1

    if len(series) >= len(target_series):
        for j in range(len(series) - len(target_series) + 1):
            sub_series = series[j:j + len(target_series)]
            sad = calculate_sad(target_series, sub_series)
            if sad < local_min_sad:
                local_min_sad = sad
                local_best_index = i

    return local_best_index, local_min_sad


# Fonction pour trouver la série temporelle la plus similaire (version asynchrone avec asyncio)
async def find_most_similar_series_async(target_series, dataset):
    tasks = [process_series(i, series, target_series) for i, series in enumerate(dataset)]
    results = await asyncio.gather(*tasks)

    min_sad = float('inf')
    best_index = -1

    for local_best_index, local_min_sad in results:
        if local_min_sad < min_sad:
            min_sad = local_min_sad
            best_index = local_best_index

    return best_index, min_sad
