#include <iostream>
#include <fstream>
#include <filesystem>
#include "json.hpp"

namespace fs = std::filesystem;
using json = nlohmann::json;

void readJSONFilesInDirectory(const std::string& directoryPath) {
    fs::path directory(directoryPath);
    if (!fs::exists(directory) || !fs::is_directory(directory)) {
        std::cerr << "Error: Invalid directory path." << std::endl;
        return;
    }

    for (const auto& entry : fs::directory_iterator(directory)) {
        if (fs::is_regular_file(entry) && entry.path().extension() == ".json") {
            std::ifstream file(entry.path().string());
            if (file) {
                json jsonData;
                file >> jsonData;

                // Process the JSON data here
                // Example: Print the content of 'data' key in each JSON file
                std::cout << "File: " << entry.path().filename().string() << std::endl;
                std::cout << "Content of 'data' key: " << jsonData["test"].get<std::string>() << std::endl;
                std::cout << "-----------------------" << std::endl;
            }
        }
    }
}

int main() {
    std::cout << " working on this" << std::endl;
    std::string directoryPath = "Writing/";  // Replace with your directory path
    std::cout << directoryPath << std::endl;
    readJSONFilesInDirectory(directoryPath);

    return 0;
}

