#include <iostream>
using namespace std;

int GetGcd(int a, int b) {
    while (a > 0 && b > 0) {
        if (a >= b) {
            a %= b;
        } else {
            b %= a;
        }
    }
    return a + b;
}

int main() {
    int n;
    cin >> n;
    int ans = 0;
    for (int itr0 = 1; itr0 <= n; ++itr0) {
        for (int itr1 = 1; itr1 <= n; ++itr1) {
            for (int i = 1; i <= n; ++i) {
                if (GetGcd(i, n) == 1) {
                    ++ans;
                }
            }
        }
    }
    cout << ans << endl;
    return 0;
}
