#include <iostream>
#include <vector>

struct FirstQuery {
    int l;
    int r;
    int c;
};

struct SecondQuery {
    int pos;
};

struct InputData {
    int n;
    int m;
    std::vector<int> tp;
    std::vector<int> ids;
    std::vector<FirstQuery> first;
    std::vector<SecondQuery> second;
};

std::istream& operator >> (std::istream& inputStream, InputData& inputData) {
    inputStream >> inputData.n >> inputData.m;
    inputData.tp.resize(inputData.m);
    inputData.ids.resize(inputData.m);
    for (int i = 0; i < inputData.m; ++i) {
        inputStream >> inputData.tp[i];
        if (inputData.tp[i] == 1) {
            int l, r, c;
            inputStream >> l >> r >> c;
            inputData.ids[i] = inputData.first.size();
            inputData.first.push_back(FirstQuery{l, r, c});
        } else {
            int pos;
            inputStream >> pos;
            inputData.ids[i] = inputData.second.size();
            inputData.second.push_back(SecondQuery{pos});
        }
    }
    return inputStream;
}

class SegmentTree {
public:
    SegmentTree(int n) 
        : n(n)
    {
        c.resize(4 * n);
        Build(1, 0, n - 1);
    }

    int Get(int pos) {
        return Get(1, 0, n - 1, pos);
    }

    void Update(int l, int r, int x) {
        Update(1, 0, n - 1, l, r, x);
    }
private:
    int n;
    std::vector<int> c;

    static const int C_DEFAULT = 1;
    static const int C_UNUSED = -1;

    void Build(int v, int tl, int tr) {
        if (tl == tr) {
            c[v] = C_DEFAULT;
        } else {
            c[v] = C_UNUSED;
            int tm = (tl + tr) >> 1;
            Build(2 * v, tl, tm);
            Build(2 * v + 1, tm + 1, tr);
        }
    }

    void Push(int v, int tl, int tr) {
        if (c[v] != C_UNUSED && tl != tr) {
            c[2 * v] = c[2 * v + 1] = c[v];
            c[v] = C_UNUSED;
        }
    }

    int Get(int v, int tl, int tr, int pos) {
        Push(v, tl, tr);
        if (tl == tr) {
            return c[v];
        } else {
            int tm = (tl + tr) >> 1;
            if (pos <= tm) {
                return Get(2 * v, tl, tm, pos);
            } else {
                return Get(2 * v + 1, tm + 1, tr, pos);
            }
        }
    }

    void Update(int v, int tl, int tr, int l, int r, int x) {
        Push(v, tl, tr);
        if (tl == l && tr == r) {
            c[v] = x;
        } else {
            int tm = (tl + tr) >> 1;
            if (r <= tm) {
                Update(2 * v, tl, tm, l, r, x);
            } else if (l > tm) {
                Update(2 * v + 1, tm + 1, tr, l, r, x);
            } else {
                Update(2 * v, tl, tm, l, tm, x);
                Update(2 * v + 1, tm + 1, tr, tm + 1, r, x);
            }
        }
    }
};

std::vector<int> GetSolution(const InputData& inputData) {
    SegmentTree st(inputData.n);
    std::vector<int> result;
    for (int i = 0; i < inputData.m; ++i) {
        int id = inputData.ids[i];
        if (inputData.tp[i] == 1) {
            int l = inputData.first[id].l;
            int r = inputData.first[id].r;
            int c = inputData.first[id].c;
            --l;
            --r;
            st.Update(l, r, c);
        } else {
            int pos = inputData.second[id].pos;
            --pos;
            result.push_back(st.Get(pos));
        }
    }
    return result;
}

std::ostream& operator << (std::ostream& outputStream, const std::vector<int>& vector) {
    for (int i : vector) {
        outputStream << i << std::endl;
    }
    return outputStream;
}

int main() {
    InputData inputData;
    std::cin >> inputData;
    std::cout << GetSolution(inputData) << std::endl;

    return 0;
}
