import os
import requests
from conan import ConanFile
from conan.errors import ConanInvalidConfiguration
from conan.tools.scm import Version
from conan.tools.files import get, copy


class ArmGNUToolchain(ConanFile):
    name = "arm-gnu-toolchain"
    version = "14.2"

    settings = "os", "arch"
    package_type = "application"

    @property
    def archs(self):
        return ["armv7"]

    @property
    def toolchain(self):
        return "arm-none-eabi"

    def validate(self):
        if self.settings.arch != "x86_64" or self.settings.os != "Linux":
            raise ConanInvalidConfiguration(
                f"This toolchain is not compatible with {self.settings.os}-{self.settings.arch}. "
                "It can only run on Linux-x86_64."
            )
        target_os = self.settings_target.os
        target_arch = self.settings_target.arch
        if target_os != "baremetal" or target_arch not in self.archs:
            raise ConanInvalidConfiguration(
                f"This toolchain only supports building for baremetal-{self.archs.join(',')}. "
                f"{self.settings_target.os}-{self.settings_target.arch} is not supported."
            )
        if self.settings_target.compiler != "gcc":
            raise ConanInvalidConfiguration(
                f"The compiler is set to '{self.settings_target.compiler}', but this "
                "toolchain only supports building with gcc."
            )
        target_compiler_ver = Version(self.settings_target.compiler.version)
        if target_compiler_ver >= Version("15") or target_compiler_ver < Version("14"):
            raise ConanInvalidConfiguration(
                f"Invalid gcc version '{self.settings_target.compiler.version}'. "
                "Only 14.X versions are supported for the compiler."
            )

    def build(self):
        api_endpoint = 'https://cloud-api.yandex.net/v1/disk/public/resources/download?public_key={}'
        sharing_link = 'https://disk.yandex.ru/d/rOY2piT7dbrc_A'
        pk_request = requests.get(api_endpoint.format(sharing_link))
        direct_link = pk_request.json()['href']
        filename = "arm-gnu-toolchain-14.2.rel1-x86_64-arm-none-eabi.tar.xz"
        sha256 = "62a63b981fe391a9cbad7ef51b17e49aeaa3e7b0d029b36ca1e9c3b2a9b78823"
        get(self, direct_link, filename=filename, sha256=sha256, strip_root=True)


    def package(self):
        dirs_to_copy = ["arm-none-eabi", "bin", "include", "lib", "libexec"]
        for dir_name in dirs_to_copy:
            copy(
                self,
                pattern=f"{dir_name}/*",
                src=self.build_folder,
                dst=self.package_folder,
                keep_path=True,
            )
        copy(
            self,
            "LICENSE",
            src=self.build_folder,
            dst=os.path.join(self.package_folder, "licenses"),
            keep_path=False,
        )

    def package_info(self):
        self.cpp_info.bindirs.append(
            os.path.join(self.package_folder, self.toolchain, "bin")
        )
        self.conf_info.define(
            "tools.build:compiler_executables",
            {
                "c": f"{self.toolchain}-gcc",
                "cpp": f"{self.toolchain}-g++",
                "asm": f"{self.toolchain}-as",
            },
        )
