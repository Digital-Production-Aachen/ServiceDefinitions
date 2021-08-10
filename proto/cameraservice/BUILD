load("@io_bazel_rules_go//go:def.bzl", "go_library")
load("@rules_proto_grpc//cpp:defs.bzl", "cpp_grpc_library")
load("@rules_proto//proto:defs.bzl", "proto_library")
load("@io_bazel_rules_go//proto:def.bzl", "go_proto_library")

cc_proto_library(
    name = "proto_cpp",
    deps = [":camera_service_proto"],
    visibility = ["//visibility:public"],
)

cpp_grpc_library(
    name = "camera_service_grpc",
    deps = ["//proto/cameraservice:camera_service_proto"],
    visibility = ["//visibility:public"],
)

proto_library(
    name = "camera_service_proto",
    srcs = ["cameraservice.proto"],
    visibility = ["//visibility:public"],
    deps = ["@com_google_protobuf//:any_proto"],
)

go_library(
    name = "go_default_library",
    embed = [":cameraservice_go_proto"],
    importpath = "coe-sops/proto/cameraservice",
    visibility = ["//visibility:public"],
)

proto_library(
    name = "cameraservice_proto",
    srcs = ["cameraservice.proto"],
    visibility = ["//visibility:public"],
)

go_proto_library(
    name = "cameraservice_go_proto",
    compilers = ["@io_bazel_rules_go//proto:go_grpc"],
    importpath = "coe-sops/proto/cameraservice",
    proto = ":cameraservice_proto",
    visibility = ["//visibility:public"],
)
