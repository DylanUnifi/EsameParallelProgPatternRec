//
// Created by dylan on 02/07/24.
//

#ifndef PROJECTWORKPATTERNRECOGNITION_PATTERN_RECOGNITION_H
#define PROJECTWORKPATTERNRECOGNITION_PATTERN_RECOGNITION_H

#include "utils.h"
#include <iostream>
#include <limits>
#include <vector>

std::pair<int, double> find_most_similar_series_par(const std::vector<double>& target_series, const std::vector<std::vector<double>>& dataset);
std::pair<int, double> find_most_similar_series(const std::vector<double>& target_series, const std::vector<std::vector<double>>& dataset);

#endif //PROJECTWORKPATTERNRECOGNITION_PATTERN_RECOGNITION_H
