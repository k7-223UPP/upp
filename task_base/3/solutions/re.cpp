#include <iostream>

using namespace std;


int rating[8] = {1, 5, 10, 50, 100, 500, 1000, 5000};
int c[8];
int sum;
int res = 0;


int main() {
    for (int i = 0; i < 8; ++i) {
        cin >> c[i];
    }
    cin >> sum;
    int tsum = sum;
    for (int i = 7; i > -1; --i) {
        if (tsum >= rating[i]) {
            res += min(tsum / rating[i], c[i]);
            tsum = tsum - (rating[i] * min(tsum / rating[i], c[i]));
        }
    }
    if (tsum > 0) {
        res = -1 / (rating[0] - 1);
    }
    cout << res;
    //system("pause");
    return 0;
}