#include <iostream>
#include <fstream>
#include <string>

using namespace std;

const int SIZE_W = 10001;
const int SIZE_N = 101;
const int INF = 1e9;


int dp[SIZE_W][SIZE_N];
int n;
int w[SIZE_N], c[SIZE_N];
int max_w;

void init() {
    for (int i = 0; i < SIZE_W; ++i) {
        for (int j = 0; j < SIZE_N; ++j) {
            dp[i][j] = -INF;
        }
    }
}

int get_rand(int minn, int maxn) {
    int mod = maxn - minn + 1;
    return (minn + (rand() % mod));
}

int solve() {
    n = get_rand(100, 100);
    //cin >> n;
    for (int i = 0; i < n; ++i) {
        c[i] = get_rand(100, 100);
        w[i] = get_rand(100, 100);
        //cin >> c[i] >> w[i];
    }
    max_w = get_rand(10000, 10000);
    //cin >> max_w;
    dp[0][0] = 0;
    for (int k = 1; k <= n; ++k) {
        for (int n1 = 0; n1 < n; ++n1) {
            for (int w1 = 0; w1 + w[n1] <= max_w; ++w1) {
                if (dp[w1][k - 1] != -INF)
                dp[w1 + w[n1]][k] = max(dp[w1 + w[n1]][k], dp[w1][k - 1] + c[n1]);
            }
        }
    }
    int res = 0;
    for (int k = 1; k <= n; ++k) {
        for (int w1 = 0; w1 <= max_w; ++w1) {
            res = max(res, dp[w1][k]);
        }
    }
    return res;
    //cout << res << endl;
}

string get_t_num(int t) {
    string t_num;
    if (t < 10) {
        t_num = "00" + to_string(long long(t));
    } else if (t < 100) {
        t_num = "0" + to_string(long long (t));
    } else {
        t_num = to_string(long long (t));
    }
    return t_num;
}

void writeInput(int t) {
    string t_num = get_t_num(t);
    t_num += ".in";
    ofstream input(t_num);
    input << n << endl;
    for (int i = 0; i < n; ++i) {
        input << c[i] << ' ' << w[i] << endl;
    }
    input << max_w;
    input.close();
}

void writeOutput(int t, int res) {
    string t_num = get_t_num(t);
    t_num += ".out";
    ofstream output(t_num);
    output << res << endl;
    output.close();
}


int main() {
    for (int i = 100; i <= 100; ++i) {
        int res = solve();
        writeInput(i);
        writeOutput(i, res);
    }
    return 0;
}
