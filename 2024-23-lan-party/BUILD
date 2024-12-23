load("@pypi//:requirements.bzl", "requirement")
load("@rules_python//python:py_binary.bzl", "py_binary")

py_binary(
    name = "part-one",
    srcs = ["part-one.py"],
    data = ["input.txt"],
    main = "part-one.py",
    deps = [
        requirement("numpy"),
    ],
)

py_binary(
    name = "part-two",
    srcs = ["part-two.py"],
    data = ["input.txt"],
    main = "part-two.py",
    deps = [
        requirement("numpy"),
        requirement("networkx"),
    ],
)
