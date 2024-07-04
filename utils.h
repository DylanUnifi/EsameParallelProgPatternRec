//
// Created by dylan on 02/07/24.
//

#ifndef PROJECTWORKPATTERNRECOGNITION_UTILS_H
#define PROJECTWORKPATTERNRECOGNITION_UTILS_H

#include <vector>
#include <cmath>
#include <fstream>
#include <sstream>
#include <random>
#include <algorithm>
#include <iterator>
#include <chrono>

double calculate_SAD(const std::vector<double>& series1, const std::vector<double>& series2);
std::string clean_string(const std::string& input);
std::vector<std::vector<double>> load_data(const std::string& filename);
std::vector<std::vector<double>> generate_random_dataset(const std::vector<std::vector<double>>& original_data, size_t num_series, size_t series_length);
// Fonction pour mesurer le temps d'exécution d'une fonction
template<typename Func>
double measure_execution_time(Func func) {
    auto start = std::chrono::steady_clock::now();
    func();
    auto end = std::chrono::steady_clock::now();
    std::chrono::duration<double> elapsed_seconds = end - start;
    return elapsed_seconds.count();
}

#endif //PROJECTWORKPATTERNRECOGNITION_UTILS_H
