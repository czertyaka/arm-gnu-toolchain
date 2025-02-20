cmake_minimum_required(VERSION 3.31)
set(CMAKE_TRY_COMPILE_TARGET_TYPE STATIC_LIBRARY)
project(ArmGNUToolchainTest)
add_library(test STATIC main.cpp)
