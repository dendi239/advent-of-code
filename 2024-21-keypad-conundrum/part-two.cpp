#include <fstream>
#include <iostream>
#include <queue>
#include <string>
#include <vector>

using namespace std;

auto GetCodes() -> vector<string> {
  ifstream file("2024-21-keypad-conundrum/input.txt");
  string line;
  vector<string> codes;
  while (getline(file, line)) {
    if (!line.empty()) {
      codes.push_back(line);
    }
  }
  return codes;
}

auto NumericPart(string_view code) {
  int64_t result = 0;
  for (auto c : code) {
    if (c != 'A') {
      result *= 10;
      result += c - '0';
    }
  }
  return result;
}

struct Pos {
  int x = -1, y = -1;

  bool operator<(const Pos& other) const {
    return x != other.x ? x < other.x : y < other.y;
  }

  bool operator==(const Pos& other) const {
    return x == other.x && y == other.y;
  }

  Pos Shift(char c) const {
    switch (c) {
      case '<':
        return {x - 1, y};
      case '>':
        return {x + 1, y};
      case '^':
        return {x, y + 1};
      case 'v':
        return {x, y - 1};
    }
    return *this;
  }
};

struct Keypad {
  vector<string> keys;

  int width() const { return keys[0].size(); }
  int height() const { return keys.size(); }

  bool is_valid(int x, int y) const {
    return 0 <= x && x < width() && 0 <= y && y < height() && keys[y][x] != ' ';
  }

  bool is_valid(Pos p) const { return is_valid(p.x, p.y); }

  char at(int x, int y) const { return keys[y][x]; }
  char at(Pos p) const { return at(p.x, p.y); }

  Pos Index(char c) const {
    for (int i = 0; i < width(); ++i) {
      for (int j = 0; j < height(); ++j) {
        if (at(i, j) == c) {
          return {i, j};
        }
      }
    }
    return {-1, -1};
  }

  void Print(Pos p) const {
    for (int y = height() - 1; y >= 0; --y) {
      for (int x = 0; x < width(); ++x) {
        cerr << (p == Pos{x, y} ? 'X' : at(x, y));
      }
      cerr << "\n";
    }
    cerr << "\n";
  }

  Pos Start() const { return Index('A'); }

  static Keypad Dpad() { return Keypad{{"<v>", " ^A"}}; }
  static Keypad Keyboard() { return {{" 0A", "123", "456", "789"}}; };
};

auto ValidKeys(const Keypad& kp) {
  vector<Pos> keys;
  for (int i = 0; i < kp.width(); ++i) {
    for (int j = 0; j < kp.height(); ++j) {
      if (kp.is_valid(i, j)) {
        keys.push_back({i, j});
      }
    }
  }
  return keys;
}

struct Mapping {
  int64_t total_indices, total_height;
  vector<int64_t> steps;

  explicit Mapping(const Keypad& kp, int64_t default_value)
      : total_indices(kp.width() * kp.height()),
        total_height(kp.height()),
        steps(total_indices * total_indices, default_value) {}

  int64_t Index(Pos p) const { return p.x * total_height + p.y; }

  int64_t Index(Pos p, Pos q) const {
    return Index(p) * total_indices + Index(q);
  }

  int64_t& operator()(Pos from, Pos to) { return steps[Index(from, to)]; }
  int64_t operator()(Pos from, Pos to) const { return steps[Index(from, to)]; }
};

/**
  Returns distances between each keys on keypad such that
    after traveling from one to another all previous keys
    will be pointing to A.
 */
Mapping WalkKeypad(const Mapping& from, const Keypad& keypad) {
  Mapping to(keypad, -1);
  auto update_to = [&](Pos p1, Pos p2, int64_t d) {
    if (to(p1, p2) == -1 || to(p1, p2) > d) {
      to(p1, p2) = d;
    }
  };

  static auto dpad = Keypad::Dpad();
  static auto dpad_start = dpad.Start();
  static auto valid_dpad_pos = ValidKeys(dpad);

  for (auto pos : ValidKeys(keypad)) {
    Mapping dist(keypad, -1);
    priority_queue<tuple<int64_t, Pos, Pos>> queue;

    auto put = [&](int64_t d, Pos p, Pos pl) {
      if (dist(p, pl) != -1 && dist(p, pl) <= d) return;

      dist(p, pl) = d;
      queue.push({-d, p, pl});
    };

    put(0, pos, dpad_start);

    while (!queue.empty()) {
      auto [dpos, p, pl] = queue.top();
      queue.pop();
      dpos = -dpos;

      if (dist(p, pl) != -1 && dist(p, pl) < dpos) continue;
      dist(p, pl) = dpos;

      if (dpad.at(pl) != 'A') {
        auto next_pos = p.Shift(dpad.at(pl));

        if (keypad.is_valid(next_pos)) {
          put(dpos + 1, next_pos, pl);
        }
      } else {
        update_to(pos, p, dpos);
      }

      for (auto dpad_pos : valid_dpad_pos) {
        if (from(pl, dpad_pos) != -1) {
          put(dpos + from(pl, dpad_pos), p, dpad_pos);
        }
      }
    }
  }

  return to;
}

int main() {
  auto codes = GetCodes();
  int64_t sum = 0;

  Mapping m(Keypad::Dpad(), 0);
  for (int i = 0; i < 25; ++i) {
    m = WalkKeypad(m, Keypad::Dpad());
  }
  m = WalkKeypad(m, Keypad::Keyboard());

  for (auto code : codes) {
    int64_t score = 0;
    Pos p = Keypad::Keyboard().Start();

    for (auto c : code) {
      auto np = Keypad::Keyboard().Index(c);
      score += m(p, np) + 1;
      p = np;
    }

    sum += score * NumericPart(code);
  }

  cout << sum << '\n';
}
