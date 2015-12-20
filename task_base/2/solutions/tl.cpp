#include <iostream>

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

void foo(int t) {
    t = t + 1;
}

int main() {
    cin >> n;
    for (int i = 0; i < n; ++i) {
        cin >> c[i] >> w[i];
    }
    cin >> max_w;
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
    while(true) {};
    cout << res << endl;
   // system("pause");
    return 0;
}
