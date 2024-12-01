load("@rules_rust//rust:defs.bzl", "rust_binary")

rust_binary(
    name = "part-one",
    data = ["input.txt"],
    srcs = ["part-one.rs"],
)

py_binary(
    name = "part-two",
    data = ["input.txt"],
    srcs = ["part-two.py"],
    main = "part-two.py",
)
