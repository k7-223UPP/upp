#include <iostream>
#include <vector>
using namespace std;

const int MAX_N = 100050000;

int main() {
    vector<int> ans(MAX_N, 0);
    int y = 0;
    for (int i = 0; i < 1000500; ++i) {
        int x = rand() % ans.size();

        y += x;
    }
    cout << y << endl;
    return 0;
}
