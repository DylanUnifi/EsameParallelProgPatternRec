from utils import calculate_sad, process_series
from joblib import Parallel, delayed
import asyncio


# Fonction pour trouver la série temporelle la plus similaire (version séquentielle)
def find_most_similar_series_sequential(target_series, dataset):
    min_sad = float('inf')
    best_index = -1

    for i, series in enumerate(dataset):
        if len(series) >= len(target_series):
            for j in range(len(series) - len(target_series) + 1):
                sub_series = series[j:j + len(target_series)]
                sad = calculate_sad(target_series, sub_series)
                if sad < min_sad:
                    min_sad = sad
                    best_index = i

    return best_index, min_sad


# Fonction pour trouver la série temporelle la plus similaire (version parallèle)
def find_most_similar_series_parallel(target_series, dataset, n_jobs):
    min_sad = float('inf')
    best_index = -1

    def process_series(i, series):
        nonlocal min_sad, best_index
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

    results = Parallel(n_jobs=n_jobs)(delayed(process_series)(i, series) for i, series in enumerate(dataset))

    for local_best_index, local_min_sad in results:
        if local_min_sad < min_sad:
            min_sad = local_min_sad
            best_index = local_best_index

    return best_index, min_sad
