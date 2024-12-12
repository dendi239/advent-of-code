#include <fstream>
#include <iostream>
#include <numeric>
#include <vector>

template <typename T, typename U>
struct DSU {
  DSU(int n, U updater = U())
      : parent(n), size(n, 1), data(n), updater(updater) {
    std::iota(parent.begin(), parent.end(), 0);
  }

  int Find(int a) const {
    if (a != parent[a]) {
      return parent[a] = Find(parent[a]);
    } else {
      return a;
    }
  }

  int Size(int a) const { return size[Find(a)]; }

  T Data(int a) const { return data[Find(a)]; }
  T& Data(int a) { return data[Find(a)]; }

  void Merge(int a, int b) {
    a = Find(a), b = Find(b);
    if (a != b) {
      if (size[a] < size[b]) {
        std::swap(a, b);
      }
      parent[b] = a;
      size[a] += size[b];
      data[a] = updater(data[a], data[b]);
    }
  }

 private:
  mutable std::vector<int> parent;
  std::vector<int> size;

  std::vector<T> data;
  U updater;
};

auto ReadGrid(std::string_view filename) {
  std::vector<std::string> grid;
  std::ifstream in(filename);
  std::string row;
  while (std::getline(in, row)) {
    grid.push_back(row);
  }
  return grid;
}

int main() {
  auto grid = ReadGrid("2024-12-garden-groups/input.txt");

  int n = grid.size(), m = grid[0].size();
  auto index = [&](int x, int y) {
    if (x < 0 || x >= n || y < 0 || y >= m) return n * m;
    return m * x + y;
  };
  auto get = [&](int x, int y) {
    if (x < 0 || x >= n || y < 0 || y >= m) return '$';
    return grid[x][y];
  };

  auto dsu = DSU<int64_t, std::plus<>>(n * m + 1);
  std::pair<int, int> dd[4]{{-1, 0}, {1, 0}, {0, -1}, {0, 1}};

  for (int i = 0; i < grid.size(); ++i) {
    for (int j = 0; j < grid[i].size(); ++j) {
      for (auto [di, dj] : dd) {
        if (get(i, j) != get(i + di, j + dj)) {
          dsu.Data(index(i, j)) += 1;
        } else {
          dsu.Merge(index(i, j), index(i + di, j + dj));
        }
      }
    }
  }

  int64_t ans = 0;
  for (int i = 0; i < n * m; ++i) {
    if (i == dsu.Find(i)) {
      ans += dsu.Data(i) * dsu.Size(i);
      std::cerr << "at (" << i / m << ", " << i % m
                << "): perimeter: " << dsu.Data(i) << " area: " << dsu.Size(i)
                << " root: (" << dsu.Find(i) / m << ", " << dsu.Find(i) % m
                << ")"
                << "\n";
    }
  }

  std::cout << ans << '\n';
  return 0;
}
