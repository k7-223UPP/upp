#include <iostream>
#include <vector>

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
    std::string s, t;
    std::cin >> s >> t;

    std::cout << GetOccurrences(s, t) << std::endl;

    return 0;
}
