#include <iostream>
#include <string>
#include <vector>
#include <sstream>
#include <iomanip>
#include <fstream>

inline int GenN() {
    const int MIN_N = 1;
    const int MAX_N = 1e5;
    return rand() % (MAX_N - MIN_N + 1) + MIN_N;
}

inline std::string GetTestNumberRepr(int testNumber) {
    std::stringstream stream;
    stream << std::setfill('0') << std::setw(3) << testNumber;
    return stream.str();
}

inline std::string GetOutputFileName(int testNumber) {
    const std::string OUTPUT_FILE_EXTENSION = ".out";
    return GetTestNumberRepr(testNumber) + OUTPUT_FILE_EXTENSION;
}

inline std::string GetInputFileName(int testNumber) {
    const std::string INPUT_FILE_EXTENSION = ".in";
    return GetTestNumberRepr(testNumber) + INPUT_FILE_EXTENSION;
}


// TODO: refactor code to split correct solution and test generator

std::vector<std::pair<int, int>> GetFactorization(int n) {
    std::vector<std::pair<int, int>> result;
    for (int i = 2; i * i <= n; ++i) {
        if (n % i) {
            result.push_back(std::make_pair(i, 0));
            while (n % i == 0) {
                ++result.back().second;
                n /= i;
            }
        } 
    }
    if (n > 1) {
        result.push_back(std::make_pair(n, 1));
    }
    return result;
}

int GetPhi(int n) {
    std::vector<std::pair<int, int>> factorization = GetFactorization(n);
    int result = n;
    for (const std::pair<int, int>& p : factorization) {
        result -= result / p.first;
    }
    return result;
}

int main() {
    for (int testNumber = 3; testNumber <= 99; ++testNumber) {
        std::cout << testNumber << std::endl;

        const std::string inputFileName = GetInputFileName(testNumber);
        const std::string outputFileName = GetOutputFileName(testNumber);

        std::cout << "  " << inputFileName << " " << outputFileName << std::endl;

        int n = GenN();
        std::cout << "  " << n << " " << GetPhi(n) << std::endl;

        std::ofstream inputFile(inputFileName);
        inputFile << n << std::endl;
        inputFile.close();

        std::ofstream outputFile(outputFileName);
        outputFile << GetPhi(n) << std::endl;
        outputFile.close();
    }
    return 0;
}
