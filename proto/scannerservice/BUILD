load("@rules_proto//proto:defs.bzl", "proto_library")
load("@io_bazel_rules_go//go:def.bzl", "go_library")
load("@io_bazel_rules_go//proto:def.bzl", "go_proto_library")
load("@rules_proto_grpc//nodejs:defs.bzl", "nodejs_grpc_compile")

nodejs_grpc_compile(
    name = "scannerservice_nodejs_proto",
    deps = [":scannerservice_proto"],
)

proto_library(
    name = "scannerservice_proto",
    srcs = ["scannerservice.proto"],
    visibility = ["//visibility:public"],
    deps = ["@ovf//:openvectorformat_proto"],
)

filegroup(
    name = "scannerservice_file",
    srcs = ["scannerservice.proto"],
    visibility = ["//visibility:public"],
)

go_proto_library(
    name = "scannerservice_go_proto",
    compilers = ["@io_bazel_rules_go//proto:go_grpc"],
    importpath = "coe-sops/proto/scannerservice",
    proto = ":scannerservice_proto",
    visibility = ["//visibility:public"],
    deps = ["@ovf//:go_default_library"],
)

go_library(
    name = "go_default_library",
    embed = [":scannerservice_go_proto"],
    importpath = "coe-sops/proto/scannerservice",
    visibility = ["//visibility:public"],
)
