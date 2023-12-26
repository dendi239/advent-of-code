workspace(name = "dendi239-advent-of-code")

load("@bazel_tools//tools/build_defs/repo:http.bzl", "http_archive")

http_archive(
    name = "rules_rust",
    sha256 = "75177226380b771be36d7efc538da842c433f14cd6c36d7660976efb53defe86",
    urls = ["https://github.com/bazelbuild/rules_rust/releases/download/0.34.1/rules_rust-v0.34.1.tar.gz"],
)

load("@rules_rust//rust:repositories.bzl", "rules_rust_dependencies", "rust_register_toolchains")

rules_rust_dependencies()


rust_register_toolchains(
    edition = "2021",
    versions = [
        "1.66.1",
    ],
)

load("@rules_rust//tools/rust_analyzer:deps.bzl", "rust_analyzer_dependencies")

rust_analyzer_dependencies()
