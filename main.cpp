#include "utils.h"
#include "pattern_recognition.h"
#include <iostream>

int main() {
    // Définir la série temporelle cible
    std::vector<double> target_series = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10};

    // Charger les données à partir du chemin spécifié
    std::string file_path = "/home/dylan/CLionProjects/ProjectWorkPatternRecognition/data/Mcompetitions M4-methods Dataset/Monthly-train.csv";
    std::vector<std::vector<double>> dataset = load_data(file_path);

    if (dataset.empty()) {
        std::cerr << "Erreur: le jeu de données est vide ou n'a pas été chargé correctement." << std::endl;
        return 1;
    }

    // Charger les données à partir du fichier CSV
    std::vector<std::vector<double>> original_data = load_data(file_path);

    if (original_data.empty()) {
        std::cerr << "Aucune donnée n'a été chargée à partir du fichier." << std::endl;
        return 1;
    }

    // Définir les tailles du dataset à générer
    //size_t num_datasets = 7; // Nombre de datasets à générer
    std::vector<size_t> dataset_sizes = {10000, 25000, 50000, 75000, 100000, 200000, 500000}; // Tailles des datasets à générer

    // Générer et afficher les datasets aléatoires pour chaque taille spécifiée
    for (size_t size : dataset_sizes) {
        size_t series_length = target_series.size(); // Longueur de la série temporelle
        std::vector<std::vector<double>> random_dataset = generate_random_dataset(original_data, size, original_data[0].size());


        // Mesurer le temps d'exécution pour la version séquentielle
        double sequential_time = measure_execution_time([&]() {
            find_most_similar_series(target_series, dataset);
        });

        // Mesurer le temps d'exécution pour la version parallèle avec OpenMP
        double parallel_time = measure_execution_time([&]() {
            find_most_similar_series_par(target_series, dataset);
        });

        // Afficher les résultats
        std::cout << "Taille du dataset : " << size << " x " << series_length << std::endl;
        std::cout << "Temps d'exécution séquentiel : " << sequential_time << " secondes" << std::endl;
        std::cout << "Temps d'exécution parallèle (OpenMP) : " << parallel_time << " secondes" << std::endl;
        std::cout << std::endl;

/*        // Affichage de quelques exemples pour vérifier
        std::cout << "Exemples du dataset aléatoire de taille " << size << " x " << original_data[0].size() << " : " << std::endl;
        for (size_t i = 0; i < std::min(size_t(3), size); ++i) {
            std::cout << "Série " << i << ": ";
            for (double value : random_dataset[i]) {
                std::cout << value << " ";
            }
            std::cout << std::endl;
        }
        std::cout << std::endl;*/
    }

    /*// Trouver en mode parallel la série temporelle la plus similaire
    auto result = find_most_similar_series_par(target_series, dataset);
    int best_index = result.first;
    double min_sad = result.second;

    std::cout << "La série temporelle la plus similaire est à l'indice " << best_index << " avec une valeur SAD de " << min_sad << std::endl;

    // Trouver la série temporelle la plus similaire
    result = find_most_similar_series(target_series, dataset);
    best_index = result.first;
    min_sad = result.second;

    std::cout << "La série temporelle la plus similaire est à l'indice " << best_index << " avec une valeur SAD de " << min_sad << std::endl;
    return 0;*/
}
