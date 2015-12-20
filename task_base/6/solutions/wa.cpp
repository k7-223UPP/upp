#include <iostream>
#include <string>
using namespace std;

int n;
string s;

int main() {
 cin >> n;
 s.reserve(2000);
 for (int i = 0; i < 100; ++i) {
     s.push_back('a');
 }
 for (int i = 0; i < 100; ++i) {
     s.push_back('b');
 }
 cout << s << endl;
 return 0;
}