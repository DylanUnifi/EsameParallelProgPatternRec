#include "pattern_recognition.h"


// Fonction pour trouver la série temporelle la plus similaire
std::pair<int, double> find_most_similar_series_par(const std::vector<double>& target_series, const std::vector<std::vector<double>>& dataset) {
    int best_index = -1;
    double min_sad = std::numeric_limits<double>::max();

#pragma omp parallel for
    for (size_t i = 0; i < dataset.size(); ++i) {
        const auto& series = dataset[i];
        if (series.size() >= target_series.size()) {
            for (size_t j = 0; j <= series.size() - target_series.size(); ++j) {
                std::vector<double> sub_series(series.begin() + j, series.begin() + j + target_series.size());
                double sad = calculate_SAD(target_series, sub_series);
#pragma omp critical
                {
                    if (sad < min_sad) {
                        min_sad = sad;
                        best_index = i;
                    }
                }
            }
        }
    }

    return {best_index, min_sad};
}

// Fonction pour trouver la série temporelle la plus similaire
std::pair<int, double> find_most_similar_series(const std::vector<double>& target_series, const std::vector<std::vector<double>>& dataset) {
    int best_index = -1;
    double min_sad = std::numeric_limits<double>::max();

    for (size_t i = 0; i < dataset.size(); ++i) {
        const auto &series = dataset[i];
        if (series.size() >= target_series.size()) {
            for (size_t j = 0; j <= series.size() - target_series.size(); ++j) {
                std::vector<double> sub_series(series.begin() + j, series.begin() + j + target_series.size());
                double sad = calculate_SAD(target_series, sub_series);
                if (sad < min_sad) {
                    min_sad = sad;
                    best_index = i;
                }
            }
        }
    }

    return {best_index, min_sad};
}