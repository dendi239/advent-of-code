#include <fstream>
#include <iostream>
#include <string>

struct Parser {
  int64_t left = 0, right = 0;
  int mul_p = 0, do_p = 0, dont_p = 0;
  bool is_enabled = true;
  void (*on_parsed)(int64_t);
};

int ParserMul = 1 << 1;
int ParserDo = 1 << 2;
int ParserDont = 1 << 3;

int ParserButMul = ParserDo | ParserDont;
int ParserButDont = ParserMul | ParserDo;
int ParserFull = ParserMul | ParserDo | ParserDont;

void reset(Parser *p, int flags) {
  if (flags & ParserMul) {
    p->left = p->right = 0;
    p->mul_p = 0;
  }

  if (flags & ParserDo) p->do_p = 0;
  if (flags & ParserDont) p->dont_p = 0;
}

void _expect(int *state, int value) {
  if (*state != value) {
    *state = 0;
  } else {
    ++*state;
  }
}

void parse(Parser *p, char c) {
  //   std::cerr << c;
  switch (c) {
    case 'm':
      reset(p, ParserFull);
      ++p->mul_p;
      break;
    case 'u':
      _expect(&p->mul_p, 1);
      reset(p, ParserButMul);
      break;
    case 'l':
      _expect(&p->mul_p, 2);
      reset(p, ParserButMul);
      break;

    case 'd':
      reset(p, ParserFull);
      ++p->do_p;
      ++p->dont_p;
      break;
    case 'o':
      _expect(&p->do_p, 1);
      _expect(&p->dont_p, 1);
      reset(p, ParserMul);
      break;

    case 'n':
      _expect(&p->dont_p, 2);
      reset(p, ParserButDont);
      break;

    case '\'':
      _expect(&p->dont_p, 3);
      reset(p, ParserButDont);
      break;

    case 't':
      _expect(&p->dont_p, 4);
      reset(p, ParserButDont);
      break;

    case '(':
      _expect(&p->do_p, 2);
      _expect(&p->dont_p, 5);
      _expect(&p->mul_p, 3);
      break;

    case ')':
      _expect(&p->do_p, 3);
      _expect(&p->dont_p, 6);
      _expect(&p->mul_p, 5);

      if (p->do_p == 4) p->is_enabled = true;
      if (p->dont_p == 7) p->is_enabled = false;

      if (p->mul_p == 6 && p->is_enabled) p->on_parsed(p->left * p->right);

      reset(p, ParserFull);
      break;

    case ',':
      _expect(&p->mul_p, 4);
      reset(p, ParserButMul);
      break;

    case '0':
    case '1':
    case '2':
    case '3':
    case '4':
    case '5':
    case '6':
    case '7':
    case '8':
    case '9': {
      int64_t *value = &(p->mul_p == 4 ? p->left : p->right);
      *value = *value * 10 + c - '0';
      reset(p, ParserButMul);
      break;
    }

    default:
      reset(p, ParserFull);
  }
}

int64_t sum = 0;
void add(int64_t value) { sum += value; }

int main() {
  std::string line;
  std::ifstream in("2024-03-mull-it-over/input.txt");

  Parser p{.on_parsed = add};
  while (std::getline(in, line)) {
    for (char c : line) parse(&p, c);
  }
  std::cout << sum << '\n';
}
