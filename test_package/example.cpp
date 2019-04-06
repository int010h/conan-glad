#include <iostream>

#include <glad/glad.h>

int main() {
    if (!gladLoadGL()) {
        std::cout << "Cannot initialize GL! But that's okay :)\n";
    }

    return 0;
}
