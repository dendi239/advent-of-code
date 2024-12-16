#include <cstdint>
#include <fstream>
#include <iostream>
#include <map>
#include <ostream>
#include <queue>
#include <set>
#include <string>

template <class T, class S, class C>
S &Container(std::priority_queue<T, S, C> &q) {
  struct HackedQueue : private std::priority_queue<T, S, C> {
    static S &Container(std::priority_queue<T, S, C> &q) {
      return q.*&HackedQueue::c;
    }
  };
  return HackedQueue::Container(q);
}

struct Index {
  int x, y, dx, dy;

  Index Forward() const { return {x + dx, y + dy, dx, dy}; }
  Index RotateRight() const { return {x, y, -dy, dx}; }
  Index RotateLeft() const { return {x, y, dy, -dx}; }

  bool operator<(const Index &other) const {
    if (x != other.x) {
      return x < other.x;
    } else if (y != other.y) {
      return y < other.y;
    } else if (dx != other.dx) {
      return dx < other.dx;
    } else {
      return dy < other.dy;
    }
  }

  bool operator==(const Index &other) const {
    return x == other.x && y == other.y && dx == other.dx && dy == other.dy;
  }

  bool AtPos(const Index &other) const { return x == other.x && y == other.y; }
};

std::ostream &operator<<(std::ostream &os, const Index &i) {
  return os << "Index{ x=" << i.x << ", y=" << i.y << ", dx=" << i.dx
            << ", dy=" << i.dy << " }";
}

struct Grid {
  const std::vector<std::string> &grid;

  int width() const { return grid[0].size(); }
  int height() const { return grid.size(); }

  char at(int x, int y) const { return grid[y][x]; }
  char at(const Index &i) const { return grid[i.y][i.x]; }

  bool valid(const Index &i) const {
    return 0 <= i.x && i.x < width() && 0 <= i.y && i.y < height() &&
           at(i) != '#';
  }
};

int main() {
  std::ifstream in("2024-16-reindeer-maze/input.txt");
  std::vector<std::string> lines;
  std::string line;

  while (std::getline(in, line)) {
    if (!line.empty()) {
      lines.push_back(line);
    }
  }

  auto grid = Grid{lines};

  auto find_me = [&](char target) {
    for (int x = 0; x < grid.width(); ++x) {
      for (int y = 0; y < grid.height(); ++y) {
        if (grid.at(x, y) == target) {
          return Index{x, y, +1, 0};
        }
      }
    }
    return Index{};
  };

  auto start = find_me('S'), finish = find_me('E');
  auto q = std::priority_queue<std::tuple<int64_t, Index, Index>>();
  std::map<Index, int64_t> seen;
  std::map<Index, std::set<Index>> prev;
  q.emplace(0, start, start);

  while (!q.empty()) {
    auto [d, i, pi] = q.top();
    q.pop();

    if (seen.count(i) && seen[i] < -d) continue;
    prev[i].insert(pi);

    if (seen.count(i)) continue;
    seen[i] = -d;

    if (i.AtPos(finish)) {
      std::set<Index> current = {i, i.RotateLeft(), i.RotateLeft().RotateLeft(),
                                 i.RotateRight()};
      std::set<std::pair<int, int>> reached;
      while (!current.empty()) {
        std::set<Index> next_;
        for (auto j : current) {
          if (!(j == start)) next_.insert(prev[j].begin(), prev[j].end());
          reached.emplace(j.x, j.y);
        }
        std::swap(current, next_);
      }

      for (int y = 0; y < grid.height(); ++y) {
        for (int x = 0; x < grid.width(); ++x) {
          std::cerr << (reached.count({x, y}) ? 'O' : grid.at(x, y));
        }
        std::cerr << "\n";
      }
      std::cout << reached.size() << " " << -d << "\n";
      return 0;
    }

    if (grid.valid(i.Forward())) q.emplace(d - 1, i.Forward(), i);
    if (grid.valid(i.RotateLeft())) q.emplace(d - 1000, i.RotateLeft(), i);
    if (grid.valid(i.RotateRight())) q.emplace(d - 1000, i.RotateRight(), i);
  }
}
