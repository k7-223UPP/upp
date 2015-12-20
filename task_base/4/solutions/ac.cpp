#include <iostream>
#include <string>

using namespace std;

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

int main() {
    cin >> s;
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
    if (flag) {
        cout << "YES" << endl;
    } else {
        cout << "NO" << endl;
    }
    //system("pause");
    return 0;
}