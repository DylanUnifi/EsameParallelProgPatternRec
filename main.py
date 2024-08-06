from utils import load_data, generate_random_dataset, measure_execution_time
import numpy as np
from pattern_recognition import find_most_similar_series_sequential, find_most_similar_series_parallel
import asyncio
import csv


async def main():
    # Chemin vers le fichier CSV
    file_path = r"/home/dylan/PycharmProjects/EsameParallelProgPatternRec/data/Monthly-train.csv"

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
    num_threads = [1, 2, 4, 8, 16]

    with open('/home/dylan/PycharmProjects/EsameParallelProgPatternRec/data/benchmark_csv/num_threads_speedup.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['NumThreads', ' : ', "Speedup: "])
        for num_thread in num_threads:
            num_runs = 1
            dataset = generate_random_dataset(original_data, 10000, series_length)
            avgSequentialTime = 0;
            avgParallelTime = 0;
            avgSpeedup = 0;
            temp_run = num_runs
            while (temp_run > 0):
                # Mesurer le temps d'exécution pour la version séquentielle
                sequential_time = measure_execution_time(
                    lambda: find_most_similar_series_sequential(target_series, dataset))
                print(f"Temps d'exécution séquentiel : {sequential_time:.4f} secondes")
                avgSequentialTime += sequential_time

                # Mesurer le temps d'exécution pour la version parallèle
                parallel_time = measure_execution_time(lambda: find_most_similar_series_parallel(target_series, dataset, num_thread))
                print(f"Temps d'exécution parallèle : {parallel_time:.4f} secondes")
                avgParallelTime += parallel_time

                avgSpeedup += sequential_time / parallel_time;
                temp_run -= 1
            avgSpeedup = avgSpeedup / num_runs
            writer = csv.writer(csvfile)
            writer.writerow([num_thread, ' , ', avgSpeedup])

    with open('/home/dylan/PycharmProjects/EsameParallelProgPatternRec/data/benchmark_csv/length_dataset_speedup.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Dataset Length', ' : ', "Speedup: "])
        for num_series in dataset_sizes:
            # Générer un dataset de taille num_series x series_length
            dataset = generate_random_dataset(original_data, num_series, series_length)
            print(f"Taille du dataset : {num_series} x {series_length}")
            avgSequentialTime = 0; avgParallelTime = 0; avgSpeedup = 0;
            num_runs = 1
            temp_run = num_runs
            while(temp_run > 0):

                # Mesurer le temps d'exécution pour la version séquentielle
                sequential_time = measure_execution_time(lambda: find_most_similar_series_sequential(target_series, dataset))
                print(f"Temps d'exécution séquentiel : {sequential_time:.4f} secondes")
                avgSequentialTime += sequential_time

                # Mesurer le temps d'exécution pour la version parallèle
                parallel_time = measure_execution_time(lambda: find_most_similar_series_parallel(target_series, dataset, 8))
                print(f"Temps d'exécution parallèle : {parallel_time:.4f} secondes")
                avgParallelTime += parallel_time

                avgSpeedup += sequential_time / parallel_time;
                temp_run -= 1
            avgSpeedup = avgSpeedup / num_runs
            writer = csv.writer(csvfile)
            writer.writerow([num_series, ' , ', avgSpeedup])


if __name__ == "__main__":
    asyncio.run(main())
