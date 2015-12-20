#include <iostream>
#include <sstream>
#include <cassert>
#include <fstream>
#include <vector>
using namespace std;

using Answer = vector<int>;

bool Read(Answer& answer, int m, istream& inputStream) {
    answer.resize(m);
    for (int i = 0; i < m; ++i) {
        if (!(inputStream >> answer[i])) {
            return false;
        }
    }
    return true;
}

int main(int argc, char** argv)
{
    ifstream input(argv[1]);
    ifstream output(argv[2]);
    ifstream userOutput(argv[3]);

    int n, m;
    input >> n >> m;

    Answer realAnswer;
    Read(realAnswer, m, output);

    Answer userAnswer;
    bool failed = !Read(userAnswer, m, userOutput);

    input.close();
    output.close();
    userOutput.close();

    if (failed || userAnswer != realAnswer) { 
        return 1;
    } else {
        return 0;
    }
}
