#include <iostream>
#include <vector>
#include <cmath>
#include <limits>
#include <omp.h>

// Fonction pour calculer la SAD entre un motif et une sous-série
int calculate_SAD(const std::vector<int>& pattern, const std::vector<int>& sub_series) {
    int sad = 0;
    for (size_t i = 0; i < pattern.size(); ++i) {
        sad += std::abs(pattern[i] - sub_series[i]);
    }
    return sad;
}

// Fonction pour trouver le motif dans la longue série en utilisant OpenMP
std::pair<int, int> find_pattern_in_series(const std::vector<int>& pattern, const std::vector<int>& long_series) {
    int pattern_length = pattern.size();
    int series_length = long_series.size();

    int min_sad = std::numeric_limits<int>::max();
    int best_index = -1;

#pragma omp parallel for
    for (int i = 0; i <= series_length - pattern_length; ++i) {
        std::vector<int> sub_series(long_series.begin() + i, long_series.begin() + i + pattern_length);
        int sad = calculate_SAD(pattern, sub_series);

#pragma omp critical
        {
            if (sad < min_sad) {
                min_sad = sad;
                best_index = i;
            }
        }
    }

    return {best_index, min_sad};
}

int main() {
    std::vector<int> pattern = {0, 1, 1};
    std::vector<int> long_series = {0, 1, 1, 2, 3, 4, 5, 1, 2, 3, 4, 1, 2, 3, 1, 2, 3};

    auto result = find_pattern_in_series(pattern, long_series);

    std::cout << "Le motif est trouvé à l'indice " << result.first
              << " avec une valeur SAD de " << result.second << std::endl;

    return 0;
}
