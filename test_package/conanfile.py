import os
from io import StringIO
from conan import ConanFile
from conan.tools.cmake import CMake, cmake_layout


class TestPackageConan(ConanFile):
    settings = "os", "arch", "compiler", "build_type"
    generators = "CMakeToolchain", "VirtualBuildEnv"

    def build_requirements(self):
        self.tool_requires(self.tested_reference_str)
        self.tool_requires("cmake/3.31.5")

    def layout(self):
        cmake_layout(self)

    def build(self):
        cmake = CMake(self)
        cmake.configure(variables={"CMAKE_TRY_COMPILE_TARGET_TYPE": "STATIC_LIBRARY"})
        cmake.build()

    def test(self):
        toolchain = "arm-none-eabi"
        self.run(f"{toolchain}-gcc --version")
        test_file = os.path.join(self.cpp.build.bindirs[0], "libtest.a")
        stdout = StringIO()
        self.run(f"objdump -a {test_file}", stdout=stdout)
        assert "elf32-little" in stdout.getvalue()
