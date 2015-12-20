#include <iostream>
#include <utility>
#include <string>
#include <vector>
#include <sstream>
#include <iomanip>
#include <fstream>

const int MIN_N = 1;
const int MAX_N = 5e4;

inline int GetRandIntInRange(int left, int right) {
    return rand() % (right - left + 1) + left;
}

inline char GetRandAlpha() {
    const int ALPHABET_SIZE = 26;
    return rand() % ALPHABET_SIZE + 'a';
}

std::string GetRandString(int n) {
    std::string result;
    result.resize(n);
    for (int i = 0; i < n; ++i) {
        result[i] = GetRandAlpha();
    }
    return result;
}

std::string GetRandString() {
    int n = GetRandIntInRange(MIN_N, MAX_N);
    return GetRandString(n);
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

std::vector<int> GetZFunction(const std::string& s) {
    int n = s.length();
    std::vector<int> z(n);
    z[0] = 0;
    for (int i = 1, l = -1, r = -1; i < n; ++i) {
        if (i <= r) {
            z[i] = std::min(r - i + 1, z[i - l]);
        } else {
            z[i] = 0;
        }
        while (i + z[i] < n && s[z[i]] == s[i + z[i]]) {
            ++z[i];
        }
        if (i + z[i] - 1 > r) {
            l = i;
            r = i + z[i] - 1;
        }
    }
    return z;
}

std::vector<int> GetOccurrences(const std::string& s, const std::string& t) {
    int n = s.length();
    int m = t.length();
    std::vector<int> z = GetZFunction(s + t);
    std::vector<int> result;
    for (int i = n; i < n + m; ++i) {
        if (z[i] >= n) {
            result.push_back(i - n);
        }
    }
    return result;
}

std::ostream& operator << (std::ostream& outputStream, const std::vector<int>& vector) {
    if (vector.empty()) {
        outputStream << -1;
    } else {
        outputStream << vector.size() << std::endl;
        for (int i : vector) {
            outputStream << i << " ";
        }
    }
    return outputStream;
}

int main() {
    for (int testNumber = 3; testNumber <= 120; ++testNumber) {
        std::cout << testNumber << std::endl;

        const std::string inputFileName = GetInputFileName(testNumber);
        const std::string outputFileName = GetOutputFileName(testNumber);

        std::cout << "  " << inputFileName << " " << outputFileName << std::endl;

        std::string s, t;

        if (testNumber & 1) {
            s = GetRandString();
            t = GetRandString();
        } else {
            t = GetRandString();
            int n = t.length();
            int l = GetRandIntInRange(1, n);
            int r = GetRandIntInRange(1, n);
            if (l > r) {
                std::swap(l, r);
            }
            s = t.substr(l, r - l + 1);
        }

        std::ofstream inputFile(inputFileName);
        inputFile << s << std::endl;
        inputFile << t << std::endl;
        inputFile.close();

        std::ofstream outputFile(outputFileName);
        outputFile << GetOccurrences(s, t) << std::endl;
        outputFile.close();
    }
    return 0;
}

// TODO: refactor code to split correct solution and test generator
