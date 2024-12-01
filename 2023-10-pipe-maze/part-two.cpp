#include <deque>
#include <fstream>
#include <iostream>
#include <set>

using G = std::vector<std::vector<ssize_t>>;

struct TableIndexer {
  ssize_t n, m;

  ssize_t X(ssize_t i) const { return i / n; }
  ssize_t Y(ssize_t i) const { return i % n; }
  ssize_t Index(ssize_t x, ssize_t y) const { return x * n + y; }

  ssize_t Size() const { return n * m; }

  ssize_t Left(ssize_t i) const { return X(i) == 0 ? -1 : i - n; }
  ssize_t Right(ssize_t i) const { return X(i) == m - 1 ? -1 : i + n; }
  ssize_t Up(ssize_t i) const { return Y(i) == 0 ? -1 : i - 1; }
  ssize_t Down(ssize_t i) const { return Y(i) == n - 1 ? -1 : i + 1; }

  struct TableIndex {
    ssize_t i;
    const TableIndexer &t;

    friend auto &operator<<(std::ostream &os, const TableIndex &i) {
      if (i.i == -1) return os << "brkn";
      return os << "(" << i.t.X(i.i) << ", " << i.t.Y(i.i) << ")";
    }
  };

  TableIndex F(ssize_t i) const { return TableIndex{i, *this}; }
};

struct TableEnumerator {
  ssize_t n, m;
  const std::vector<std::string> &table;

  char At(ssize_t i) const { return i == -1 ? '.' : table[Y(i)][X(i)]; }

  ssize_t X(ssize_t i) const { return i / n; }
  ssize_t Y(ssize_t i) const { return i % n; }
  ssize_t Index(ssize_t x, ssize_t y) const { return x * n + y; }

  ssize_t Size() const { return n * m; }

  ssize_t Left(ssize_t i) const { return X(i) == 0 ? -1 : i - n; }
  ssize_t Right(ssize_t i) const { return X(i) == m - 1 ? -1 : i + n; }
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

struct GraphBuilder {
  virtual ~GraphBuilder() = default;
  virtual void OnCreate(size_t n, size_t m) = 0;
  virtual void OnConnect(ssize_t x1, ssize_t y1, ssize_t x2, ssize_t y2) = 0;
  virtual void OnFinish() = 0;
};

void BuildGraph(const TableEnumerator &t, GraphBuilder *builder) {
  builder->OnCreate(t.n, t.m);

  std::set<char> ups{'S', '|', 'L', 'J'}, downs{'S', '|', 'F', '7'},
      lefts{'S', '7', 'J', '-'}, rights{'S', 'F', 'L', '-'};

  using T = std::tuple<std::set<char>, std::set<char>,
                       std::function<ssize_t(ssize_t)>>;

  for (ssize_t i = 0; i < t.Size(); ++i) {
    std::cerr << "Inside " << t.F(i) << " " << t.At(i) << "\n";
    for (auto [opts, oposite, dir] : {
             T(ups, downs, [&](ssize_t x) { return t.Up(x); }),
             T(downs, ups, [&](ssize_t x) { return t.Down(x); }),
             T(lefts, rights, [&](ssize_t x) { return t.Left(x); }),
             T(rights, lefts, [&](ssize_t x) { return t.Right(x); }),
         }) {
      if (dir(i) != -1) {
        std::cerr << "  dir: " << t.F(dir(i)) << " sym: " << t.At(dir(i))
                  << "\n";
      }
      if (opts.count(t.At(i)) && dir(i) != -1 && oposite.count(t.At(dir(i)))) {
        builder->OnConnect(t.X(i), t.Y(i), t.X(dir(i)), t.Y(dir(i)));
      }
    }
  }

  builder->OnFinish();
}

template <class F>
auto FindSingleCycle(ssize_t start, const G &g, F on_enter) {
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

    on_enter(v);

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

  std::cerr << "gsize: " << g.size() << "\n";
  std::cerr << "tv:" << tv << std::endl;

  std::vector<ssize_t> cycle;
  for (ssize_t v = tv; v != start; v = prev[v]) {
    std::cerr << " v: " << v << " prev: " << prev[v];
    cycle.push_back(v);
  }
  std::cerr << std::endl;

  cycle.push_back(start);
  std::reverse(cycle.begin(), cycle.end());
  for (ssize_t v = tu; v != start; v = prev[v]) cycle.push_back(v);

  std::cerr << "here" << std::endl;

  return cycle;
}

struct ClassicGraphBuilder : GraphBuilder {
  const TableEnumerator &t;
  G *g;

  ClassicGraphBuilder(const TableEnumerator &_t, G *_g) : t(_t), g(_g) {}
  ~ClassicGraphBuilder() = default;

  virtual void OnCreate(size_t n, size_t m) override { *g = G(n * m); }
  virtual void OnConnect(ssize_t x1, ssize_t y1, ssize_t x2,
                         ssize_t y2) override {
    (*g)[t.Index(x1, y1)].push_back(t.Index(x2, y2));
    (*g)[t.Index(x2, y2)].push_back(t.Index(x1, y1));
  }
  virtual void OnFinish() override {
    for (auto &level : *g) {
      std::sort(level.begin(), level.end());
      level.erase(unique(level.begin(), level.end()), level.end());
    }
  }
};

struct DoubleGraphBuilder : GraphBuilder {
  const TableIndexer &t;
  G *g;

  DoubleGraphBuilder(const TableIndexer &_t, G *_g) : t(_t), g(_g) {}

  virtual void OnCreate(size_t n, size_t m) override { *g = G(t.Size()); }
  virtual void OnConnect(ssize_t x1, ssize_t y1, ssize_t x2,
                         ssize_t y2) override {
    std::cerr << "  Connect " << x1 << ", " << y1 << " and " << x2 << " " << y2
              << "\n";
    auto fst = t.Index(2 * x1, 2 * y1);
    auto snd = t.Index(x1 + x2, y1 + y2);
    auto trd = t.Index(2 * x2, 2 * y2);
    (*g)[fst].push_back(snd);
    (*g)[snd].push_back(fst);
    (*g)[snd].push_back(trd);
    (*g)[trd].push_back(snd);
  }
  virtual void OnFinish() override {
    for (auto &level : *g) {
      std::sort(level.begin(), level.end());
      level.erase(unique(level.begin(), level.end()), level.end());
    }
  }
};

signed main() {
  std::ifstream f("2023-10-pipe-maze/input.txt");

  std::vector<std::string> table;
  std::string row;
  while (std::getline(f, row)) {
    table.push_back(row);
  }

  const size_t n = table.size(), m = table[0].size();
  TableEnumerator t{static_cast<ssize_t>(n), static_cast<ssize_t>(m), table};
  TableIndexer dt{static_cast<ssize_t>(2 * n), static_cast<ssize_t>(2 * m)};
  G g;

  DoubleGraphBuilder builder{dt, &g};
  BuildGraph(t, &builder);

  const ssize_t start = [&] {
    for (ssize_t i = 0; i < dt.Size(); ++i)
      if (t.At(i) == 'S') return dt.Index(2 * t.X(i), 2 * t.Y(i));
    return static_cast<ssize_t>(-1);
  }();

  auto cycle = FindSingleCycle(start, g, [&](ssize_t i) {
    std::cerr << "Enter " << dt.F(i);
    std::cerr << "  Edges to: ";
    for (auto v : g[i]) std::cerr << " " << dt.F(v);
    std::cerr << std::endl;
  });
  std::vector<int> is_cycle(g.size());
  for (auto u : cycle) is_cycle[u] = 1;

  std::vector<ssize_t> q;

  for (ssize_t i = 0; i < dt.Size(); ++i) {
    if (is_cycle[i]) continue;
    if (dt.X(i) == 0 || dt.X(i) == dt.m - 1 || dt.Y(i) == 0 ||
        dt.Y(i) == dt.n - 1) {
      q.push_back(i);
      is_cycle[i] = 2;
    }
  }

  while (!q.empty()) {
    auto u = q.back();
    q.pop_back();

    for (auto v : {dt.Up(u), dt.Left(u), dt.Right(u), dt.Down(u)}) {
      if (v != -1 && !is_cycle[v]) {
        is_cycle[v] = 2;
        q.push_back(v);
      }
    }
  }

  size_t answer = 0;
  for (ssize_t y = 0; y < dt.n; ++y) {
    for (ssize_t x = 0; x < dt.m; ++x) {
      if (x % 2 == 0 && y % 2 == 0 && is_cycle[dt.Index(x, y)] == 0) ++answer;
      std::cerr << ".bx"[is_cycle[dt.Index(x, y)]];
    }
    std::cerr << "\n";
  }

  std::cout << answer << "\n";
}
