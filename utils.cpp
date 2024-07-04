//
// Created by dylan on 02/07/24.
//

#include "utils.h"
#include <iostream>

// Fonction pour calculer la SAD entre deux séries temporelles
double calculate_SAD(const std::vector<double>& series1, const std::vector<double>& series2) {
    double sad = 0.0;
    for (size_t i = 0; i < series1.size(); ++i) {
        sad += std::abs(series1[i] - series2[i]);
    }
    return sad;
}

// Fonction pour nettoyer une chaîne de caractères en supprimant les non-chiffres
std::string clean_string(const std::string& input) {
    std::string result;
    for (char c : input) {
        if (std::isdigit(c) || c == '.' || c == '-') { // Garder les chiffres, le point décimal et le signe négatif
            result += c;
        }
    }
    return result;
}


// Fonction pour charger les données à partir d'un fichier CSV en ignorant le premier élément et la première ligne
std::vector<std::vector<double>> load_data(const std::string& filename) {
    std::vector<std::vector<double>> data;
    std::ifstream file(filename);

    if (!file.is_open()) {
        std::cerr << "Erreur: impossible d'ouvrir le fichier " << filename << std::endl;
        return data;
    }

    std::string line;
    bool first_line = true; // Pour ignorer la première ligne
    while (std::getline(file, line)) {
        if (first_line) {
            first_line = false;
            continue; // Ignorer la première ligne
        }

        std::vector<double> row;
        std::stringstream ss(line);
        std::string cell;
        bool first_cell = true; // Pour ignorer le premier élément de chaque ligne
        while (std::getline(ss, cell, ',')) {
            if (first_cell) {
                first_cell = false;
                continue; // Ignorer le premier élément
            }
            if (!cell.empty()) {
                // Nettoyer la chaîne de caractères pour ne garder que les chiffres, le point décimal et le signe négatif
                std::string cleaned_cell = clean_string(cell);
                if (!cleaned_cell.empty()) {
                    row.push_back(std::stod(cleaned_cell));
                }
            }
        }
        if (!row.empty()) {
            data.push_back(row);
        }
    }

    file.close();
    return data;
}


// Fonction pour générer un dataset aléatoire à partir des données chargées
std::vector<std::vector<double>> generate_random_dataset(const std::vector<std::vector<double>>& original_data, size_t num_series, size_t series_length) {
    std::vector<std::vector<double>> random_dataset(num_series, std::vector<double>(series_length));
    std::mt19937 gen(std::random_device{}());
    std::uniform_int_distribution<size_t> dist(0, original_data.size() - 1);

    for (size_t i = 0; i < num_series; ++i) {
        const auto& series = original_data[dist(gen)]; // Sélectionne une série aléatoire

        // Assurez-vous que la série a une longueur suffisante pour extraire une sous-série de la longueur spécifiée
        if (series.size() < series_length) {
            // Si la série est plus courte, ajustez la position de début pour éviter le dépassement
            size_t start_pos = rand() % (series.size());
            std::copy(series.begin() + start_pos, series.end(), random_dataset[i].begin());
            // Si la série est encore plus courte, remplisse le reste avec des zéros
            std::fill(random_dataset[i].begin() + series.size() - start_pos, random_dataset[i].end(), 0);
        } else {
            size_t start_pos = rand() % (series.size() - series_length + 1);
            std::copy(series.begin() + start_pos, series.begin() + start_pos + series_length, random_dataset[i].begin());
        }
    }

    return random_dataset;
}
