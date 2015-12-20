#include <iostream>
using namespace std;

int main() {
    int ans = 0;
    while (true) {
        ans += rand();
    }
    std::cout << ans << std::endl;
    return 0;
}
