cmake_minimum_required(VERSION 3.28)
project(ProjectWorkPatternRecognition)

# added -fopenmp
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11 -fopenmp")

add_executable(ProjectWorkPatternRecognition main.cpp
        pattern_recognition_seq.cpp
        pattern_recognition_parallel.cpp)
