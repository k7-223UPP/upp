#include <iostream>
#include <cassert>
#include <fstream>
#include <string>
using namespace std;


int main(int argc, char** argv)
{
    ifstream input(argv[1]);
    ifstream output(argv[2]);
    ifstream userOutput(argv[3]);

    string res, user_res;
    output >> res;
    userOutput >> user_res;
    
    input.close();
    output.close();
    userOutput.close();

    if (res != user_res) {
        return 1;
    } else {
        return 0;
    }
}
