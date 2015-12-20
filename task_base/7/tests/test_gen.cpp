#include <iostream>
#include <sstream>
#include <iomanip>
#include <algorithm>
#include <queue>
#include <vector>
#include <set>
#include <fstream>
#include <string>

const int MIN_N = 1;
const int MAX_N = 1e3;

const int MIN_M = 1;
const int MAX_M = 1e5;

const int MIN_W = 0;
const int MAX_W = 1e9;

inline int GetRandIntInRange(int left, int right) {
    return rand() % (right - left + 1) + left;
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

struct Edge {
    int from;
    int to;
    int cost;
};

std::ostream& operator << (std::ostream& outputStream, const Edge& edge) {
    outputStream << edge.from << " " << edge.to << " " << edge.cost;
    return outputStream;
}

Edge GetRandEdge(int n) {
    return Edge{
        GetRandIntInRange(1, n),
        GetRandIntInRange(1, n),
        GetRandIntInRange(MIN_W, MAX_W)
    };
}

struct InputData {
    int n;
    int m;
    int s;
    int f;
    std::vector<Edge> edges;
};

InputData GetRandInputData() {
    InputData result;
    result.n = GetRandIntInRange(MIN_N, MAX_N);
    result.m = GetRandIntInRange(MIN_M, MAX_M);
    result.s = GetRandIntInRange(1, result.n);
    result.f = GetRandIntInRange(1, result.n);
    result.edges.resize(result.m);
    for (int i = 0; i < result.m; ++i) {
        result.edges[i] = GetRandEdge(result.n);
    }
    return result;
}

std::ostream& operator << (std::ostream& outputStream, const InputData& inputData) {
    outputStream << inputData.n << " " << inputData.m << 
        " " << inputData.s << " " << inputData.f << std::endl;
    for (int i = 0; i < inputData.m; ++i) {
        outputStream << inputData.edges[i] << std::endl;
    }
    return outputStream;
}

int GetSolution(const InputData& inputData) {
    int n = inputData.n;
    int m = inputData.m;
    int s = inputData.s - 1;
    int f = inputData.f - 1;
    std::vector<std::vector<Edge>> g(n);
    for (int i = 0; i < m; ++i) {
        int v1 = inputData.edges[i].from - 1;
        int v2 = inputData.edges[i].to - 1;
        int w = inputData.edges[i].cost;
        g[v1].push_back(Edge{v1, v2, w});
        g[v2].push_back(Edge{v2, v1, w});
    }
    const long long INF = 1e18;
    std::vector<long long> dist(n, INF);
    dist[s] = 0;
    std::priority_queue<
        std::pair<long long, int>,
        std::vector<std::pair<long long, int>>,
        std::greater<std::pair<long long, int>>
    > q;
    q.push(std::make_pair(0, s));
    while (!q.empty()) {
        long long curD = q.top().first;
        int curV = q.top().second;
        q.pop();

        if (dist[curV] < curD) {
            continue;
        }

        for (const Edge& edge : g[curV]) {
            if (edge.cost + curD < dist[edge.to]) {
                dist[edge.to] = edge.cost + curD;
                q.push(std::make_pair(dist[edge.to], edge.to));
            }
        }
    }
    if (dist[f] == INF) {
        return -1;
    } else {
        return dist[f];
    }
}

int main() {
    for (int testNumber = 3; testNumber <= 120; ++testNumber) {
        std::cout << testNumber << std::endl;

        const std::string inputFileName = GetInputFileName(testNumber);
        const std::string outputFileName = GetOutputFileName(testNumber);

        std::cout << "  " << inputFileName << " " << outputFileName << std::endl;

        const InputData& inputData = GetRandInputData();

        std::ofstream inputFile(inputFileName);
        inputFile << inputData;
        inputFile.close();

        std::ofstream outputFile(outputFileName);
        outputFile << GetSolution(inputData) << std::endl;
        outputFile.close();
    }
    return 0;
}

// TODO: refactor code to split correct solution and test generator
