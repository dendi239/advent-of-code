# advent of code

This is my sources for [avent of code](https://adventofcode.com) challenges.
Idk if I keep doing it next year, but let's try doing it now.

For most of the tasks, it used to contain `input.txt` in respective directory, however it's (not permitted](https://adventofcode.com/about#faq_copying).
Therefore `input.txt` was included to `.gitignore`, excluded from history, but I'm too lazy to update the code.
Here's how to run some of tasks:
```sh
export TASK="08-haunted-wasteland"  # choosing random task
pbpaste > "${TASK}"/input.txt  # 
bazel run "${TASK}:part-one"
bazel run "${TASK}:part-two"
```
