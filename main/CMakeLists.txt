add_executable(${projectName} main.cpp)

set(CADMIUM_DIR $ENV{CADMIUM})

if(NOT CADMIUM_DIR)
    message(FATAL_ERROR "CADMIUM environment variable is not set.")
endif()

target_include_directories(${projectName} PUBLIC
    "."
    "../include"
    ${CADMIUM_DIR}
    "${CADMIUM_DIR}/.."
    "${CADMIUM_DIR}/../json/include"
)

target_compile_options(${projectName} PUBLIC -std=gnu++2b)