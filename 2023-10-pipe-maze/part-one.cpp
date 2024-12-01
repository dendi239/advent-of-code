#include <algorithm>
#include <deque>
#include <fstream>
#include <iostream>
#include <iterator>
#include <ostream>
#include <set>
#include <string>
#include <vector>

using G = std::vector<std::vector<ssize_t>>;

struct TableEnumerator {
  ssize_t n, m;
  const std::vector<std::string> &table;

  char At(ssize_t i) const { return i == -1 ? '.' : table[Y(i)][X(i)]; }

  ssize_t X(ssize_t i) const { return i / n; }
  ssize_t Y(ssize_t i) const { return i % n; }
  ssize_t Index(ssize_t x, ssize_t y) { return x * n + y; }

  ssize_t Size() const { return n * m; }

  ssize_t Left(ssize_t i) const { return X(i) == 0 ? -1 : i - m; }
  ssize_t Right(ssize_t i) const { return X(i) == m - 1 ? -1 : i + m; }
  ssize_t Up(ssize_t i) const { return Y(i) == 0 ? -1 : i - 1; }
  ssize_t Down(ssize_t i) const { return Y(i) == n - 1 ? -1 : i + 1; }

  struct TableIndex {
    ssize_t i;
    const TableEnumerator &t;

    friend auto &operator<<(std::ostream &os, const TableIndex &i) {
      if (i.i == -1) return os << "brkn";
      return os << "(" << i.t.X(i.i) << ", " << i.t.Y(i.i) << ")";
    }
  };

  TableIndex F(ssize_t i) const { return TableIndex{i, *this}; }
};

auto BuildGraph(const TableEnumerator &t) {
  G g(t.n * t.m);

  std::set<char> ups{'S', '|', 'L', 'J'}, downs{'S', '|', 'F', '7'},
      lefts{'S', '7', 'J', '-'}, rights{'S', 'F', 'L', '-'};

  using T = std::tuple<std::set<char>, std::set<char>,
                       std::function<ssize_t(ssize_t)>>;

  for (ssize_t i = 0; i < t.Size(); ++i) {
    for (auto [opts, oposite, dir] : {
             T(ups, downs, [&](ssize_t x) { return t.Up(x); }),
             T(downs, ups, [&](ssize_t x) { return t.Down(x); }),
             T(lefts, rights, [&](ssize_t x) { return t.Left(x); }),
             T(rights, lefts, [&](ssize_t x) { return t.Right(x); }),
         }) {
      if (opts.count(t.At(i)) && dir(i) != -1 && oposite.count(t.At(dir(i)))) {
        g[i].push_back(dir(i));
        g[dir(i)].push_back(i);
      }
    }
  }

  for (auto &lvl : g) {
    std::sort(lvl.begin(), lvl.end());
    lvl.erase(std::unique(lvl.begin(), lvl.end()), lvl.end());
  }

  return g;
}

auto FindSingleCycle(ssize_t start, const G &g) {
  std::vector<size_t> dist(g.size(), g.size() * 10);
  std::vector<ssize_t> prev(g.size(), -1);

  std::deque<ssize_t> q{start};
  dist[start] = 0;
  prev[start] = start;
  size_t cycle_len = 0;
  ssize_t tu, tv;

  while (!q.empty()) {
    auto v = q.front();
    q.pop_front();

    for (auto u : g[v]) {
      if (prev[v] == u) continue;
      if (dist[u] > dist[v] + 1) {
        dist[u] = dist[v] + 1;
        prev[u] = v;
        q.push_back(u);
        continue;
      }

      std::tie(tu, tv, cycle_len) = std::tuple{u, v, dist[u] + dist[v] + 1};
      break;
    }

    if (cycle_len > 0) break;
  }

  std::vector<int> on_cycle(g.size());
  for (ssize_t v = tv, i = 1; v != start; v = prev[v], ++i) on_cycle[v] = i;
  for (ssize_t v = tu, i = 1; v != start; v = prev[v], ++i) on_cycle[v] = i;

  std::vector<ssize_t> cycle;
  for (ssize_t v = tv; v != start; v = prev[v]) cycle.push_back(v);
  cycle.push_back(start);
  std::reverse(cycle.begin(), cycle.end());
  for (ssize_t v = tu; v != start; v = prev[v]) cycle.push_back(v);

  return cycle;
}

signed main() {
  std::ifstream f("2023-10-pipe-maze/input.txt");

  std::vector<std::string> table;
  std::string row;
  while (std::getline(f, row)) {
    table.push_back(row);
  }

  const size_t n = table.size(), m = table[0].size();
  TableEnumerator t{static_cast<ssize_t>(n), static_cast<ssize_t>(m), table};
  G g = BuildGraph(t);

  ssize_t start = [&] {
    for (ssize_t i = 0; i < t.Size(); ++i)
      if (t.At(i) == 'S') return i;
    return static_cast<ssize_t>(-1);
  }();

  auto cycle = FindSingleCycle(start, g);
  std::vector<int> on_cycle(t.Size());
  for (auto u : cycle) on_cycle[u] = true;

  std::cerr << "Here's maze:\n";
  for (ssize_t y = 0; y < n; ++y) {
    std::cerr << " ";
    for (ssize_t x = 0; x < m; ++x) {
      ssize_t i = t.Index(x, y);
      std::cerr << t.At(i);
    }
    std::cerr << "\n";
  }

  for (ssize_t y = 0; y < n; ++y) {
    std::cerr << "  ";
    for (ssize_t x = 0; x < m; ++x) {
      ssize_t i = t.Index(x, y);
      std::cerr << ((on_cycle[i] || i == start) ? t.At(i) : '.');
    }
    std::cerr << "\n";
  }

  std::cout << cycle.size() / 2 << '\n';
}
