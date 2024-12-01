#include <fstream>
#include <iostream>
#include <sstream>
#include <string_view>

template <class T, class F>
T BinSearch(T l, T r, F f) {
  for (T m; m = (l + r) / 2, m != l && m != r;) (f(m) ? l : r) = m;
  return l;
}

int64_t BeatRecord(int64_t duration, int64_t current) {
  auto cond = [&](int64_t wait_time) {
    return wait_time * (duration - wait_time) > current;
  };
  auto l = BinSearch(duration / 2, static_cast<int64_t>(-1), cond);
  auto r = BinSearch(duration / 2, duration + 1, cond);

  return r - l + 1;
}

std::string WithoutSpaces(std::string s) {
  std::stringstream ss(s);
  std::string res, curr;
  while (ss >> curr) {
    if (res.empty()) {
      res += curr;
      res += " ";
    } else {
      res += curr;
    }
  }
  return res;
}

signed main() {
  std::ifstream f("2023-06-wait-for-it/input.txt");
  std::string time_string, distance_string;

  std::getline(f, time_string);
  std::getline(f, distance_string);

  std::stringstream time_s(WithoutSpaces(time_string)),
      distance_s(WithoutSpaces(distance_string));
  std::string crap;
  time_s >> crap;
  distance_s >> crap;

  std::vector<std::pair<int64_t, int64_t>> records;
  int64_t time, distance, answer = 1;
  while (time_s >> time && distance_s >> distance) {
    answer *= BeatRecord(time, distance);
  }

  std::cout << answer << "\n";
}
