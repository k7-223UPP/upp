#include <iostream>
#include <sstream>
#include <cassert>
#include <fstream>
#include <vector>
using namespace std;

using Answer = vector<int>;

bool Read(Answer& answer, istream& inputStream) {
    int sz;
    if (!(inputStream >> sz)) {
        return false;
    }
    if (sz == -1) {
        answer.clear();
    } else {
        answer.resize(sz);
        for (int i = 0; i < sz; ++i) {
            if (!(inputStream >> answer[i])) {
                return false;
            }
        }
    }
    return true;
}

int main(int argc, char** argv)
{
    ifstream input(argv[1]);
    ifstream output(argv[2]);
    ifstream userOutput(argv[3]);

    int n;
    input >> n;

    Answer realAnswer;
    Read(realAnswer, output);

    Answer userAnswer;
    bool failed = !Read(userAnswer, userOutput);

    input.close();
    output.close();
    userOutput.close();

    if (failed || userAnswer != realAnswer) { 
        return 1;
    } else {
        return 0;
    }
}
