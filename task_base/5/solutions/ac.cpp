#include <iostream>
#include <vector>

std::vector<std::pair<int, int>> GetFactorization(int n) {
    std::vector<std::pair<int, int>> result;
    for (int i = 2; i * i <= n; ++i) {
        if (n % i == 0) {
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
    int n;
    std::cin >> n;

    std::cout << GetPhi(n) << std::endl;

    return 0;
}
