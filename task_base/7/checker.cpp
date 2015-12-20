#include <iostream>
#include <sstream>
#include <cassert>
#include <fstream>
using namespace std;

int main(int argc, char** argv)
{
    ifstream input(argv[1]);
    ifstream output(argv[2]);
    ifstream userOutput(argv[3]);

    int n;
    input >> n;

    int realAnswer;
    output >> realAnswer;

    int userAnswer;
    bool failed = false;
    if (!(userOutput >> userAnswer)) {
        failed = true;
    }

    input.close();
    output.close();
    userOutput.close();

    if (failed || userAnswer != realAnswer) { 
        return 1;
    } else {
        return 0;
    }
}
