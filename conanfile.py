from conans import ConanFile, Meson, tools
import glob
import os
import shutil


class Openh264Conan(ConanFile):
    name = "openh264"
    version = "1.9.0.1806"
    git_hash = "c81d7f6"
    license = "https://raw.githubusercontent.com/cisco/openh264/master/LICENSE"
    author = "KudzuRunner"
    url = "https://github.com/kudzurunner/conan-openh264"
    description = "Open Source H.264 Codec"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=True"
    generators = "pkg_config"
    suffix = ""

    def build_requirements(self):
        self.build_requires("meson_installer/0.49.0@bincrafters/stable")
        if self.settings.os == "Windows":
            self.build_requires("nasm_installer/2.13.02@bincrafters/stable")


    def source(self):
        git = tools.Git(folder=self.name)
        git.clone("https://github.com/cisco/openh264.git", branch="master")
        git.checkout(self.git_hash)
        tools.replace_in_file("{}/meson.build".format(self.name), "version : '1.8.0'", "version : '1.9.0'")

    def build(self):
        args = ["--default-library={}".format("shared" if self.options.shared else "static")]
        meson = Meson(self, build_type=self.settings.build_type, backend="ninja")
        meson.configure(source_folder=self.name, build_folder="build", args=args)
        meson.build()

    def package(self):
        self.copy(pattern="LICENSE", dst="licenses", src=self.name)
        self.copy("*.h", dst="include/wels", src="build/include/wels")
        self.copy("*.dll", dst="bin", keep_path=False)
        self.copy("*.dylib*", dst="lib", keep_path=False)
        self.copy("*.so", dst="lib", keep_path=False)
        self.copy("*openh264*.a", dst="lib", keep_path=False)

        self.suffix = ("_d" if self.settings.build_type == "Debug" else "")
        if self.settings.compiler == "Visual Studio":
            with tools.chdir(os.path.join(self.package_folder, "lib")):
                libs = glob.glob("lib*.a")
                for lib in libs:
                    vslib = lib[3:-2] + self.suffix + ".lib"
                    self.output.info('renaming %s into %s' % (lib, vslib))
                    shutil.move(lib, vslib)
            with tools.chdir(os.path.join(self.package_folder, "bin")):
                dlls = glob.glob("*.dll")
                for dll in dlls:
                    vsdll = dll[:-6] + self.suffix + ".dll"
                    self.output.info('renaming %s into %s' % (dll, vsdll))
                    shutil.move(dll, vsdll)

    def package_info(self):
        self.cpp_info.libs = ['openh264' + self.suffix]
        if self.settings.os == "Linux":
            self.cpp_info.libs.append('pthread')
