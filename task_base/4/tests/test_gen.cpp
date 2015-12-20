#include <iostream>
#include <string>
#include <fstream>

using namespace std;

const char chars[] = "0123456789.";
const int LEN = 11;

string s;

bool check(string &t) {
    int t_num = 0;
    if (t.length() < 4 && t.length() > 0) {
        for (int i = 0; i < t.length(); ++i) {
            if (t[i] >= '0' && t[i] <= '9') {
                t_num *= 10;
                t_num += t[i] - '0';
            } else {
                return false;
            }
        }
        if (t_num >= 0 && t_num <= 255) {
            return true;
        }
    }
    return false;
}

int get_rand(int minn, int maxn) {
    int mod = maxn - minn + 1;
    return minn + (rand() % mod);
}

string get_good_ip() {
    string s;
    for (int i = 0; i < 4; ++i) {
        s += to_string((long long)get_rand(0, 255)) + ".";
    }
    return s;
}

string get_bad_ip() {
    string s;
    int len = get_rand(1, 15);
    for (int i = 0; i < len; ++i) {
        s += chars[get_rand(0, LEN - 1)];
    }
    return s;
}

string get_string() {
    if (get_rand(0, 1) == 0) {
        return get_good_ip();
    } else {
        return get_bad_ip();
    }
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
    input << s << endl;
    input.close();
}

void writeOutput(int t, bool res) {
    string t_num = get_t_num(t);
    t_num += ".out";
    ofstream output(t_num);
    if (res) {
        output << "YES" << endl;
    } else {
        output << "NO" << endl;
    }
    output.close();
}

bool solve() {
    s = get_string();
    //cin >> s;
    string t;
    int i = 0;
    bool flag = true;
    for (int j = 0; j < 4; ++j) {
        while (i < s.length() && s[i] != '.') {
            t += s[i];
            ++i;
        }
        flag = flag && check(t);
        t.clear();
        if (i >= s.length() || s[i] != '.') {
            flag = false;
        }
        ++i;
    }
    return flag;
}
int main() {
    for (int i = 3; i <= 100; ++i) {
        bool flag = solve();
        writeInput(i);
        writeOutput(i, flag);
    }
    return 0;
}