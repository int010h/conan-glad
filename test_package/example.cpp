#include <iostream>

#include <glad/glad.h>

int main() {
    if (!gladLoadGL()) {
        std::cout << "Cannot initialize GL! But that's okay :)\n";
    }

    std::cout << "GL version: " << GLVersion.major << "." << GLVersion.minor << "\n";
    return 0;
}
