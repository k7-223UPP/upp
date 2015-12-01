#include <iostream>
#include <cassert>
#include <fstream>
using namespace std;


int main(int argc, char** argv)
{
    ifstream input(argv[1]);
    ifstream output(argv[2]);
    ifstream userOutput(argv[3]);

    int a, b;
    input >> a >> b;

    int ansSum = a + b;
    
    int outputSum;
    output >> outputSum;

    int userSum;
    userOutput >> userSum;

    input.close();
    output.close();
    userOutput.close();

    assert(ansSum == outputSum);

    if (userSum != ansSum) {
        return 1;
    } else {
        return 0;
    }
}
