#include <iostream>
#include <fstream>
#include <filesystem>
#include "json.hpp"
#include <unordered_map>
#include <tuple>
#include "CorrelationMatrix.h"
#include <algorithm>


namespace fs = std::filesystem;
using json = nlohmann::json;


//step 1, read all json files --TODO go through all 
//turn in a map <string(filename), json>
//That takes the 
//

//step 2 Make bigram and unigram
//file name <string(fileName)>
//bigram map <string, vector[filename]>>
//map file name <string, <unigram/bigram, string(bigrams)>> 


//step 3 create relation
//This might be just counting the associated unigram for now
//title might matter to

//This would be the lower part of a matrix?

//std::vector<json> readJSONFilesInDirectory(const std::string& directoryPath) {
//    std::vector<json> jsonDataList;  // List to store loaded JSON data
//
//    fs::path directory(directoryPath);
//    if (!fs::exists(directory) || !fs::is_directory(directory)) {
//        std::cerr << "Error: Invalid directory path." << std::endl;
//        return jsonDataList;  // Return empty list
//    }
//
//    for (const auto& entry : fs::directory_iterator(directory)) {
//        if (fs::is_regular_file(entry) && entry.path().extension() == ".json") {
//            std::ifstream file(entry.path().string());
//            if (file) {
//                json jsonData;
//                file >> jsonData;
//
//                // Process the JSON data here
//                // Example: Print the content of 'data' key in each JSON file
//                std::cout << "File: " << entry.path().filename().string() << std::endl;
//                std::cout << "Content of 'data' key: " << jsonData["test"].get<std::string>() << std::endl;
//                std::cout << "-----------------------" << std::endl;
//
//                // Add the loaded JSON data to the list
//                jsonDataList.push_back(jsonData);
//            }
//        }
//    }
//
//    return jsonDataList;
//}
//



std::unordered_map<std::string, std::unordered_map<std::string, int>> createUnigramsMap(const std::unordered_map<std::string, json>& jsonMap) {
    std::unordered_map<std::string, std::unordered_map<std::string, int>> result;

    for (const auto& [key, jsonData] : jsonMap) {
        std::unordered_map<std::string, int> wordMap;
        std::string text = jsonData["data"].get<std::string>();

        std::istringstream iss(text);
        std::string word;
        while (iss >> word) {
            wordMap[word]++;
        }

        std::cout << "Iterating over JSON data" << std::endl;

        result.emplace(key, std::move(wordMap));
    }

    return result;
}



//std::unordered_map<std::string,std::unordered_map<std::string, int > > createUnigramsMap(const std::unordered_map<std::string, json> jsonMap) {
//	//result return
//	std::unordered_map<std::string,std::unordered_map<std::string, int > > result;
//	//
//	std::unordered_map<std::string, json> fileNameToJson;
//	
//	//iterate through the map of file name and json
//	//this is similiar to pythons d.items()
//	for (const auto& pair : jsonMap) {
//	    //up pack key, value pair
//            const std::string& key = pair.first;
//            const json& jsonData = pair.second; 
//	    //create map that holds unigram counter
//	    std::unordered_map<std::string, int> wordMap;
//	    //get writing from text
//	    std::string text = jsonData["test"].get<std::string>();
//
//            // Tokenize the sentence into words
//	    std::istringstream iss(text);
//	    std::string word;
//	    while (iss >> word) {
//	        // Insert each word as a key in the map
//	        wordMap[word]++;
//	    }
//	    std :: cout << "Iterating over json data" << std::endl;
//            //add the count of unigrams to dictionary
//    	    result[key] = wordMap;
//	}
//	//finished
//	return result;
//}



std::unordered_map<std::string, json> readJSONFilesInDirectory2(const std::string& directoryPath) {
    std::vector<json> jsonDataList;  // List to store loaded JSON data
    std::unordered_map<std::string, json> fileNameToJson;
    fs::path directory(directoryPath);
    if (!fs::exists(directory) || !fs::is_directory(directory)) {
        std::cerr << "Error: Invalid directory path." << std::endl;
        return fileNameToJson;  // Return empty list
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
                std::cout << "Content of 'data' key: " << jsonData["data"].get<std::string>() << std::endl;
                std::cout << "-----------------------" << std::endl;
		
		std::string key = entry.path().filename().string();
		//add key and value
		fileNameToJson[key]=jsonData;
                // Add the loaded JSON data to the list
                jsonDataList.push_back(jsonData);
            }
        }
    }

    return  fileNameToJson;
}



//Note this function returns a map of key and score
//This is a lighter way of creating a correlation matrix
//The way it uses keys, is that it takes two keys from another map
//sorts them, then appends them together
//TODO make this more effcient
//This could be WAY MORE effcient
//I am double calculating here because I am being lazy
std::unordered_map<std::string, int> makeCorrelationMap(const std::unordered_map<std::string, std::unordered_map<std::string, int>>& gramScoreMap) {

	//return the 
	std::unordered_map<std::string, int> result;
	for (const auto& [key1, val1] : gramScoreMap ) {
		for (const auto& [key2, val2] :  gramScoreMap ) {
			//No need to find a correlation on the same files
			if (key1 != key2){//Makes sure not using the same files
				for (const auto& [word1, score1] :  val1 ) {
					//Check if word1 is in map2
					//c++ synatx for this is so ugly.....
					auto it = val2.find(word1);
					if (it != val2.end()) {
						// Key found
						// Now create master key
						std::vector<std::string> keys = {key1, key2};
						std::sort(keys.begin(), keys.end());
						//Sort the two keys
						std::string masterKey = std::accumulate(keys.begin(), keys.end(), std::string(), [](const std::string& a, const std::string& b) { return a + b; });
						//add the score it master list
						//Taking the min or intersection of word use
						int b = val1.at(word1);
						int a = val2.at(word1);
						auto it2 = result.find(masterKey);
						if (it2 != val2.end()) {result[masterKey]+= std::min(a, b);}
						else { result[masterKey]+= std::min(a, b);}
					}
				}

			}
        	}

	}
	return result;
}




int main() {
    
    std::unordered_map<std::string, int> biGramMap;	
    std::cout << "Working on this" << std::endl;
    std::string directoryPath = "Writing/";  // Replace with your directory path
    //std::unordered_map<std::string, json>    std::cout << directoryPath << std::endl;

    std::unordered_map<std::string, json> jsonDataFromFileDirectory = readJSONFilesInDirectory2(directoryPath);
    std::unordered_map<std::string, std::unordered_map<std::string, int>>  unigramMap  = createUnigramsMap( jsonDataFromFileDirectory );
    

    // Perform data analysis or any other operations with the loaded JSON data
    // Example: Create bigrams from the JSON data
  //  for (const auto& [key, jsonData] : jsonDataFromFileDirectory) {
  //        std :: cout << "This should be something" << std::endl;
  //  }
    
    std::unordered_map<std::string, int> masterUnigramMap = makeCorrelationMap(unigramMap);
    //TODO write to json, so haskell can read this.



    nlohmann::json jsonOutput;

    // Copy the unordered_map to the JSON object
    for (const auto& pair : masterUnigramMap ) {
        jsonOutput["unigram_score"] = pair.second;
	jsonOutput["pair"] = pair.first;
    }


    // Write the JSON object to a file
    std::ofstream outputFile("unigrampMap.json");
    outputFile << jsonOutput.dump(4); // Indent with 4 spaces
    outputFile.close();

    std::cout << "JSON file written successfully." << std::endl;
    return 0;
}
