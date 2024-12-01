load("@rules_rust//rust:defs.bzl", "rust_binary", "rust_library")

rust_library(
    name = "broadcaster",
    srcs = ["broadcaster.rs"],
    deps = [":graph"],
)

rust_library(
    name = "crt",
    srcs = ["crt.rs"],
)

rust_library(
    name = "graph",
    srcs = ["graph.rs"],
)

rust_binary(
    name = "part-one",
    srcs = ["part-one.rs"],
    data = ["input.txt"],
    deps = [":broadcaster"],
)

rust_binary(
    name = "part-two",
    srcs = ["part-two.rs"],
    data = ["input.txt"],
    deps = [
        ":broadcaster",
        ":graph",
        ":crt",
    ],
)
