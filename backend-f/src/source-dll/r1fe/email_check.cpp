// pch.cpp: source file corresponding to the pre-compiled header

#include "pch.h"
#include "framework.h"

extern "C" __declspec(dllexport) bool IsEmail(const char* input) {
    std::string email(input);
    const std::regex emailPattern(R"(([\w\.-]+)@([\w\.-]+)\.([a-zA-Z\.]{2,6}))");
    return std::regex_match(email, emailPattern);
}


// When you are using pre-compiled headers, this source file is necessary for compilation to succeed.
