from utils import load_data, generate_random_dataset, measure_execution_time, measure_execution_time_async
import numpy as np
from pattern_recognition import find_most_similar_series_sequential, find_most_similar_series_parallel, find_most_similar_series_async
import asyncio


async def main():
    # Chemin vers le fichier CSV
    file_path = r"data/Mcompetitions M4-methods Dataset/Monthly-train.csv"

    # Charger les données à partir du fichier CSV
    original_data = load_data(file_path)

    if not original_data:
        print("Aucune donnée n'a été chargée à partir du fichier.")
        exit()

    # Définir la longueur de la série temporelle à extraire
    series_length = len([x for x in original_data[0] if not np.isnan(x)])  # Exemple : extraire des séries de longueur

    # Définir la série temporelle cible
    target_series = np.random.rand(10).tolist()

    # Définir les tailles du dataset à générer
    dataset_sizes = [100, 500, 1000, 5000, 10000]  # Tailles des datasets à générer

    for num_series in dataset_sizes:

        # Générer un dataset de taille num_series x series_length
        dataset = generate_random_dataset(original_data, num_series, series_length)

        # Mesurer le temps d'exécution pour la version séquentielle
        sequential_time = measure_execution_time(lambda: find_most_similar_series_sequential(target_series, dataset))

        # Mesurer le temps d'exécution pour la version parallèle
        parallel_time = measure_execution_time(lambda: find_most_similar_series_parallel(target_series, dataset))

        # Mesurer le temps d'exécution pour la version asynchrone
        async_time = await measure_execution_time_async(lambda: find_most_similar_series_async(target_series, dataset))

        # Afficher les résultats
        print(f"Taille du dataset : {num_series} x {series_length}")
        print(f"Temps d'exécution séquentiel : {sequential_time:.4f} secondes")
        print(f"Temps d'exécution parallèle : {parallel_time:.4f} secondes")
        print(f"Temps d'exécution asynchrone (asyncio) : {async_time:.4f} secondes")
        print()

if __name__ == "__main__":
    asyncio.run(main())
