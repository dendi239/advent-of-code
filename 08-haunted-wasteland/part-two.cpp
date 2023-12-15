#include <array>
#include <bitset>
#include <fstream>
#include <iostream>
#include <string_view>
#include <unordered_map>
#include <vector>

#define D while (false)

namespace haunted_wasteland {

using NodeID = size_t;

enum class Command : int { LEFT = 0, RIGHT = 1 };

struct Links {
  NodeID left, right;

  NodeID operator()(Command cmd) const {
    return cmd == Command::LEFT ? left : right;
  }
};

struct Graph {
  std::vector<Links> graph;
  std::vector<std::string> labels;

  size_t Size() const { return labels.size(); }
};

auto GetGraph(std::string_view path) -> std::pair<Graph, std::vector<Command>> {
  std::ifstream f(path);

  std::string commands_str;
  f >> commands_str;
  std::vector<Command> commands;
  for (auto c : commands_str) {
    switch (c) {
      case 'L':
        commands.push_back(Command::LEFT);
        break;
      case 'R':
        commands.push_back(Command::RIGHT);
        break;
    }
  }

  std::unordered_map<std::string, NodeID> node_ids;
  std::vector<std::string> labels;

  auto get_node_id = [&](std::string node) -> NodeID {
    if (!node_ids.count(node)) {
      auto id = node_ids.size();
      node_ids[node] = id;
      labels.push_back(node);
    }
    return node_ids[node];
  };

  std::unordered_map<NodeID, Links> links;
  while (std::getline(f, commands_str)) {
    if (commands_str.size() < 16) continue;

    auto node = get_node_id(commands_str.substr(0, 3));
    auto left = get_node_id(commands_str.substr(7, 3));
    auto right = get_node_id(commands_str.substr(12, 3));

    links[node] = Links{left, right};
  }

  std::vector<Links> links_vec(links.size());
  for (NodeID i = 0; i < links_vec.size(); ++i) {
    links_vec[i] = links[i];
  }

  return {Graph{links_vec, labels}, commands};
}

template <size_t commands_size>
class CycleGraph {
  struct NodeInfo {
    NodeID next;
    int cycle_id = -1;
    std::bitset<commands_size> terminal;
  };

 public:
  CycleGraph(size_t size) : nodes_(size) {}

  auto next(NodeID node) -> NodeID { return nodes_[node].next; }

  bool on_cycle(NodeID node) { return nodes_[node].cycle_id != -1; }

  auto terminal_mask(NodeID node) const -> const std::bitset<commands_size> & {
    return nodes_[node];
  }

  auto terminal_mask(NodeID node) -> std::bitset<commands_size> & {
    return nodes_[node].terminal;
  }

  size_t cycle_len(NodeID node) const {
    return cycle_len_[nodes_[node].cycle_id];
  }

  void set_next(NodeID node, NodeID next) { nodes_[node].next = next; }

  void set_cycle_id(NodeID node, int cycle_id) {
    nodes_[node].cycle_id = cycle_id;
  }

  void set_cycle_lens(std::vector<int> cycle_len) {
    cycle_len_ = std::move(cycle_len);
  }

 private:
  std::vector<NodeInfo> nodes_;
  std::vector<int> cycle_len_;
};

template <class V>
class ShortMap {
 public:
  ShortMap(size_t size) : data_(size) {}

  auto operator[](size_t index) const { return data_[index]; }

  auto &operator[](size_t index) {
    changes_.emplace_back(index, data_[index]);
    return data_[index];
  }

  void Clear() {
    while (!changes_.empty()) {
      auto [i, v] = changes_.back();
      data_[i] = v;
      changes_.pop_back();
    }
  }

 private:
  std::vector<V> data_;
  std::vector<std::pair<size_t, V>> changes_;
};

template <size_t commands_size, class IsSource, class IsTerminal>
auto BuildCycleGraph(const Graph &graph, const std::vector<Command> &commands,
                     IsSource is_source, IsTerminal is_terminal)
    -> CycleGraph<commands_size> {
  const size_t n = graph.Size();
  CycleGraph<commands_size> cg(n);

  for (NodeID node = 0; node < n; ++node) {
    NodeID curr = node;
    for (size_t i = 0; i < commands_size; ++i) {
      cg.terminal_mask(node)[i] = is_terminal(curr);
      curr = graph.graph[curr](commands[i]);
    }
    cg.set_next(node, curr);
  }

  std::vector<int> cycle_len;
  ShortMap<int> used(n), index(n);

  for (NodeID node = 0; node < n; ++node) {
    if (index[node] != 0) {
      continue;
    }

    used.Clear();
    NodeID curr = node;
    int idx = 1;

    while (!used[curr] && !index[curr]) {
      index[curr] = idx++;
      used[curr] = 1;
      curr = cg.next(curr);
    }

    // Encounter old node.
    if (!used[curr]) continue;

    const int cycle_id = static_cast<int>(cycle_len.size());
    cycle_len.push_back(idx - index[curr]);

    for (size_t step = 0; step < cycle_len.back();
         ++step, curr = cg.next(curr)) {
      cg.set_cycle_id(curr, cycle_id);
    }
  }

  cg.set_cycle_lens(std::move(cycle_len));
  return cg;
}

}  // namespace haunted_wasteland

template <class Int>
auto LrpGcd(Int a, Int b) -> std::pair<Int, Int> {
  if (!a || !b) return std::pair(+1, +1);
  auto [x, y] = LrpGcd(b, a % b);
  return {y, x - (a / b) * y};
}

struct Remainder {
  size_t mod, rem;
};

size_t ChineeseRemainderTheorem(const std::vector<Remainder> &rems) {
  const size_t n = rems.size();

  std::vector<size_t> prefs(n + 1, 1), suffs(n + 1, 1);
  for (size_t i = 0, j = n - 1; i < n; ++i, --j) {
    prefs[i + 1] = rems[i].mod * prefs[i];
    suffs[j] = rems[j].mod * suffs[j + 1];
  }

  std::vector<size_t> all_but_one(n);
  for (size_t i = 0; i < n; ++i) {
    all_but_one[i] = prefs[i] * suffs[i + 1];
  }

  size_t result = 0;
  for (size_t i = 0; i < n; ++i) {
    size_t inv = LrpGcd<int64_t>(rems[i].mod, all_but_one[i]).second;
    // mod * x + P * inv = 1
    // inv = 1 / P (mod rems[i].mod)
    inv = (inv * rems[i].rem) % rems[i].mod;
    result += all_but_one[i] * inv;
  }

  return result;
}

template <size_t N>
size_t count_trailingzero(std::bitset<N> b) {
  // source: https://stackoverflow.com/a/72153216

  if (b.none()) return N;  // The whole bitset was zero

  const decltype(b) mask(-1ULL);  // Mask to get the lowest unsigned long long
  size_t tz = 0;                  // The number of trailing zero bits
  const int width = sizeof(unsigned long long) * CHAR_BIT;
  do {
    auto lsw = (b & mask).to_ullong();  // The least significant word
    auto lsb = __builtin_ctzll(lsw);    // Position of the least significant bit

    if (lsb < width)  // Found the first set bit from right
      return tz + lsb;

    // A set bit was not found because the lsw is all zero
    // so we'll increase the number of trailing zero bits
    tz += width;

    // Shift the bitset to get the next higher significant word
    b >>= width;
  } while (b.any());

  return tz;
}

signed main() {
  using namespace haunted_wasteland;
  constexpr const int kCommands = 283;

  Graph graph;
  std::vector<Command> commands;
  std::tie(graph, commands) = GetGraph("08-haunted-wasteland/input.txt");

  for (auto c : commands) {
    std::cout << "LR"[static_cast<int>(c)];
  }
  std::cout << "\n";
  for (NodeID node = 0; node < graph.Size(); ++node) {
    std::cout << graph.labels[node] << " = ("
              << graph.labels[graph.graph[node].left] << ", "
              << graph.labels[graph.graph[node].right] << ")\n";
  }

  auto cg = BuildCycleGraph<kCommands>(
      graph, commands,
      [&](NodeID node) { return graph.labels[node][2] == 'A'; },
      [&](NodeID node) { return graph.labels[node][2] == 'Z'; });

  std::vector<NodeID> sources;
  for (NodeID node = 0; node < graph.Size(); ++node) {
    if (graph.labels[node][2] == 'A') {
      sources.push_back(node);
    }
  }

  std::cout << "Sources:";
  for (auto source : sources) {
    std::cout << " " << graph.labels[source];
  }
  std::cout << "\n";

  const size_t n = graph.Size();
  ShortMap<int> used(n);

  // This is research tool to check that each source can encounter
  // only a single terminal state.
  for (auto source : sources) {
    std::cout << "Start: " << graph.labels[source] << "\n";
    used.Clear();
    for (NodeID curr = source; !used[curr];
         used[curr] = true, curr = cg.next(curr)) {
      auto &mask = cg.terminal_mask(curr);
      if (mask.any()) {
        std::cerr << "  " << graph.labels[curr] << ": " << mask << "\n";
      }
    }
  }

  size_t steps = 0;
  bool found = false;

  auto common_bit = [&]() -> int {
    auto mask = std::bitset<kCommands>();
    mask.flip();
    for (auto source : sources) mask &= cg.terminal_mask(source);

    if (mask.any()) return count_trailingzero(mask);
    return -1;
  };

  while (std::any_of(sources.begin(), sources.end(),
                     [&](NodeID node) { return !cg.on_cycle(node); })) {
    int bit = common_bit();
    if (bit != -1) {
      found = true;
      steps += bit;
      break;
    }

    steps += commands.size();
    for (auto &source : sources) source = cg.next(source);
  }

  if (found) {
    std::cout << steps << "\n";
    return 0;
  }

  std::vector<Remainder> rems;
  for (auto source : sources) {
    for (size_t i = 0; i < cg.cycle_len(source);
         ++i, source = cg.next(source)) {
      if (cg.terminal_mask(source).any()) {
        rems.push_back({cg.cycle_len(source), i});
      }
    }
  }

  auto cycle_steps = ChineeseRemainderTheorem(rems);
  for (auto &source : sources) {
    size_t steps = cycle_steps % cg.cycle_len(source);
    for (size_t i = 0; i < steps; ++i) source = cg.next(source);
  }

  steps += commands.size() * cycle_steps;
  steps += common_bit();

  std::cout << steps << "\n";
}
