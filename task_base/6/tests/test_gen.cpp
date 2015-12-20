#include <iostream>
#include <string>
#include <fstream>

using namespace std;

int n;
string s;

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
    input << n << endl;
    input.close();
}

void writeOutput(int t) {
    string t_num = get_t_num(t);
    t_num += ".out";
    ofstream output(t_num);
    output << s << endl;
    output.close();
}
void solve() {
    s.clear();
    //cin >> n;
    n = get_rand(1, int(1e6));
    s.reserve(2000);
    for (int i = 0; i < 1000; ++i) {
        s.push_back('a');
    }
    for (int i = 0; i < 1000; ++i) {
        s.push_back('b');
    }
}

int main() {
    for (int i = 3; i < 100; ++i) {
        solve();
        writeInput(i);
        writeOutput(i);
    }
    return 0;
}