load("@io_bazel_rules_go//go:def.bzl", "go_library")
load("@rules_proto_grpc//cpp:defs.bzl", "cpp_grpc_library")
load("@rules_proto//proto:defs.bzl", "proto_library")
load("@io_bazel_rules_go//proto:def.bzl", "go_proto_library")

cc_proto_library(
    name = "proto_cpp",
    deps = [":videoservice_proto"],
    visibility = ["//visibility:public"],
)

cpp_grpc_library(
    name = "videoservice_grpc",
    deps = ["//proto/cameraservice:hardware_controller_proto"],
    visibility = ["//visibility:public"],
)

proto_library(
    name = "videoservice_proto",
    srcs = ["videoservice.proto"],
    visibility = ["//visibility:public"],
)

go_proto_library(
    name = "videoservice_go_proto",
    compilers = ["@io_bazel_rules_go//proto:go_grpc"],
    importpath = "coe-sops/proto/videoservice",
    proto = ":videoservice_proto",
    visibility = ["//visibility:public"],
)

go_library(
    name = "go_default_library",
    embed = [":videoservice_go_proto"],
    importpath = "coe-sops/proto/videoservice",
    visibility = ["//visibility:public"],
)
