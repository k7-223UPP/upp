#include <iostream>
#include <fstream>
#include <queue>
#include <vector>

struct Edge {
    int from;
    int to;
    int cost;
};

struct InputData {
    int n;
    int m;
    int s;
    int f;
    std::vector<Edge> edges;
};

std::istream& operator >> (std::istream& inputStream, InputData& inputData) {
    inputStream >> inputData.n >> inputData.m >> inputData.s >> inputData.f;
    inputData.edges.resize(inputData.m);
    for (int i = 0; i < inputData.m; ++i) {
        inputStream >> inputData.edges[i].from >> inputData.edges[i].to >>
            inputData.edges[i].cost;
    }
    return inputStream;
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
    InputData inputData;
    std::cin >> inputData;

    std::cout << GetSolution(inputData) << std::endl;

    return 0;
}
