#include <iostream>
#include <string>
#include <fstream>

using namespace std;


int rating[8] = {1, 5, 10, 50, 100, 500, 1000, 5000};
int c[8];
int sum;
int res = 0;

int get_rand(int minn, int maxn) {
    int mod = maxn - minn + 1;
    return (minn + (rand() % mod));
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
    for (int i = 0; i < 8; ++i) {
        input << c[i] << ' ';
    }
    input << endl;
    input << sum << endl;
    input.close();
}

void writeOutput(int t, int res) {
    string t_num = get_t_num(t);
    t_num += ".out";
    ofstream output(t_num);
    output << res << endl;
    output.close();
}

int solve() {
    for (int i = 0; i < 8; ++i) {
        //cin >> c[i];
        c[i] = get_rand(1, 100); 
    }
    sum = get_rand(1, int(1e9));
    //cin >> sum;
    int tsum = sum;
    for (int i = 7; i > -1; --i) {
        if (tsum >= rating[i]) {
            res += min(tsum / rating[i], c[i]);
            tsum = tsum - (rating[i] * min(tsum / rating[i], c[i]));
        }
    }
    if (tsum > 0) {
        res = -1;
    }
    //cout << res;
    return res;
}



int main() {
    for (int i = 3; i < 100; ++i) {
        int res = solve();
        writeInput(i);
        writeOutput(i, res);
    }
    //system("pause");
    return 0;
}