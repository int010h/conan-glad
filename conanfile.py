from conans import ConanFile, CMake, tools

class GladConan(ConanFile):
    name = "glad"
    version = "0.1.29"
    license = "MIT"
    url = "https://github.com/int010h/conan-glad"
    description = "Multi-Language GL/GLES/EGL/GLX/WGL Loader-Generator based on the official specs."
    settings = "os", "compiler", "build_type", "arch"
    options = {
        "profile": ["core", "compatibility"],
        "api": "ANY",
        "spec": ["gl", "egl", "glx", "wgl"],
        "generator": ["c", "c-debug", "d", "volt"],
        "no-loader": [True, False],
        "extensions": "ANY",
        "PIC": [True, False]
    }
    default_options = '''
profile=core
api=gl=2.1
spec=gl
generator=c
no-loader=False
extensions=
PIC=True
'''
    generators = "cmake"

    def source(self):
        project_header = "project(GLAD VERSION %s LANGUAGES C)" % self.version
        self.run("git clone -b 'v%s' --single-branch --depth 1 https://github.com/Dav1dde/glad.git" % self.version)
        self.run("cd glad && git checkout v%s" % self.version)
        tools.replace_in_file("glad/CMakeLists.txt", project_header, '''%s
include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()''' % project_header)

        if self.options["PIC"] == True:
            tools.replace_in_file("glad/CMakeLists.txt", project_header, '''%s
set(CMAKE_POSITION_INDEPENDENT_CODE ON)''' % project_header)

    def build(self):
        cmake = CMake(self)
        params = [
            "-DGLAD_PROFILE=%s" % self.options.profile,
            "-DGLAD_API=%s" % self.options.api,
            "-DGLAD_SPEC=%s" % self.options.spec,
            "-DGLAD_GENERATOR=%s" % self.options.generator,
            "-DGLAD_EXTENSIONS=%s" % self.options.extensions,
        ]

        if self.options["no-loader"] == True:
            params.append("-DGLAD_NO_LOADER")

        self.run('cmake glad %s %s' % (cmake.command_line, " ".join(params)))
        self.run("cmake --build . %s" % cmake.build_config)

    def package(self):
        self.copy("*.h", dst="include/glad", src="include/glad")
        self.copy("*.h", dst="include/KHR", src="include/KHR")
        self.copy("*.lib", dst="lib", src="lib", keep_path=False)
        self.copy("*.a", dst="lib", src="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ["glad"]
