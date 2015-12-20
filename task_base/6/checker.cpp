#include <iostream>
#include <cassert>
#include <fstream>
#include <string>
#include <set>

using namespace std;


long long get_hash(char c) {
    return c - 'a';
}

int main(int argc, char** argv)
{
    ifstream input(argv[1]);
    ifstream output(argv[2]);
    ifstream userOutput(argv[3]);


    const long long M = 1e9 + 7, MOD = 29;
    int n;
    bool isCorrect = true;
    set<long long> substrSet;
    string outRes, userRes;

    input >> n;
    output >> outRes;
    userOutput >> userRes;
    
    input.close();
    output.close();
    userOutput.close();

    if (userRes.length() > 2000) {
        isCorrect = false;
    } else {
        long long hash;
        for (int i = 0; i < userRes.length(); ++i) {
            hash = 0;
            for (int j = i; j < userRes.length(); ++j) {
                hash = (hash * MOD) % M;
                hash = (hash + get_hash(userRes[j])) % M;
                substrSet.insert(hash);
            }
        }
        if (substrSet.size() < n) {
            isCorrect = false;
        }
    }

    if (!isCorrect) {
        return 1;
    } else {
        return 0;
    }
}
