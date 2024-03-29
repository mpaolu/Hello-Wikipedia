# "Hello, Wikipedia!"

A Python tool for comparison, analysis and visualization between Wikidata articles.

## Table of Contents
1. [Overview](#overview)
2. [Features](#features)
3. [How to read Wikidata Data](#how-to-read-wikidata-data)
4. [Installation and Use](#installation-and-use)
5. [Contribution and Information about the Code](#contribution-and-information-about-the-code)
6. [License](#license)
7. [FAQs](#faqs)

## Overview
This Python program was created as part of the “Data Analysis and Visualization” course at Chemnitz University of Technology and is based on my own experience as a literature student in the humanities. I noticed that it can often be very complex to uncover certain properties or overarching connections between fields of knowledge in order to be able to use these later as a basis for further investigations. The Wikifoundation with their pages like Wikipedia, Wikidata, etc. can often provide a first access to these fields of knowledge, but are tied to individual entries per page and the nature of written language.

That's why I created this tool for comparing, analyzing and visualizing two Wikidata articles, making it easier and more comprehensive to dive into Wikidata's structured data. 

Since this is my first Python program and I would like to underline my enthusiasm and fascination for this field of work, I call the program "Hello, Wikipedia!"

In particular, this tool makes it possible to identify similarities and differences and to gain insights into the amount of knowledge stored in Wikidata. Whether you're researching, creating educational materials, or simply satisfying your curiosity, the Wikidata tool provides a versatile platform to harness the power of structured data. The tool was written in English and works with the English entries on Wikidata. On the one hand, this is because the internationality and open source idea of the platform should be underlined, and on the other hand, the English data set is the largest.

Wikidata Licensing Information:

The data utilized in this tool is sourced from Wikidata, a freely available knowledge base.")
Wikidata content is licensed under the Creative Commons Zero (CC0) License, making it effectively public domain and free to use for any purpose, without attribution requirements.")
For more details on Wikidata licensing, please refer to: https://www.wikidata.org/wiki/Wikidata:Licensing")



## Features
The program has three overarching parts:
1. Search for Wikidata articles: The user is asked to search for two Wikidata articles. These correspond to the correlating Wikipedia entries on the metadata page. After each entry, the user can choose from a list of actual Wikidata suggestions. On the one hand, this enables more targeted research into data sets and, on the other hand, guarantees a clear search basis for the API calls.

2. Data query and storage: Based on user requests, all relevant information such as labels, properties and values of the wikidata items are obtained via Wikidata API requests and initial filtering is for datatype is carried out. The results of the queries in .json format are converted into Pandas data frames, sortet according to similarities or differences and saved locally for quality control, deeper research or further use of the data sets. 

3. Statistics and visualizations: Various visualizations such as tables, Sankey diagrams, sunburst diagrams or network graphs are created based on different data frames. Each form of visualization offers its own advantages and disadvantages.


## How to read Wikidata Data:
Wikidata is a central repository of metadata accessible to others, such as the Wikimedia Foundation's wikis. That's why this data is not available in continuous text, but in different category forms.
The structural format of the data available at Wikidata can be viewed here:
https://www.wikidata.org/wiki/Wikidata:Introduction

![grafik](https://github.com/mpaolu/-Hello-Wikipedia-/assets/150439065/1e5dcefc-711b-4827-9b64-6169d9378a8f)


The main categories for this program are
- label = human-readable label of the Wikidata entry
- item identifier = wikidata internal identifier of the Wikidata entry
- description = human-readable description for contextualization of the Wikidata entry
- property = describes the data value of a statement of a wikidata entry
- value = value a property can take. values can in turn also be wikidata items (especially here, since only entries with datatype = 'wikibase-item' were included)


The following would certainly be interesting for further work on the program:
- rank = shows the rank of a value
- qualifier = includes further information in the analysis that is left out when considering property and value, such as start and end times, etc.


## Installation and use:
To use the program you must install the following Python libraries:

- requests==2.26.0
- inquirer==2.7.0
- pandas==1.3.3
- plotly==5.3.1
- networkx==2.7.2
- colorama==0.4.4

Then you can run the 'hello.py' program from the CMD via the 'python3 hello.py' command from the program's location. All necessary folders to back up the data locally are created for you when running the program.

Follow the on-screen instructions and enter your two search terms. After confirming with der Enter key creates the program documentation, save data files and display visualizations as needed.


## Contribution and information about the code:
Since this is my first Python program and I hope to do many more projects like this in the future, I would be very happy about any feedback or collaboration.

Here is a breakdown of my code:

1. Introduction Function: Provides a welcome message and introduction to the program, explaining its purpose and how to use it.
2. Wikidata API Functions:
- get_wikidata_suggestions: Retrieves suggestions from Wikidata based on a search term.
- select_item: Prompts the user to select an item from a list of suggestions.
- get_wikidata_item_data: Fetches data for a Wikidata item.
- get_item_labels: Retrieves labels for Wikidata items.
- create_dataframe: Creates a DataFrame from Wikidata item data.
- compare_dataframes: Compares data between two DataFrames.
3. Data Output Functions:
- dumps: Saves data and results in JSON and CSV formats.
- statistics: Computes and prints statistics about the compared data.
4. Visualization functions:
- create_sankey_diagram: Generates a Sankey diagram based on the data.
- create_network_graph: Creates a network graph based on the merged data.
- sunburst: Generates a sunburst chart based on the data.
5. Main Function: Executes the main logic of the program, prompting the user for input, fetching data, comparing it, and then displaying statistics and visualizations



If you have any questions or suggestions, please send me an email at: maximilian.paolucci@s2020.tu-chemnitz.de


## License
This project is licensed under the MIT License. See the LICENSE file for details. For any questions, issues, or suggestions, please contact "maximilian.paolucci@s2020.tu-chemnitz.de".
Project Coherence and Relevance


## FAQs
*How does the program fit into the current discourse?*

There is already a number of very interesting wiki tools. However, all of them focus on the analysis and/or presentation of individual pages or closed aspects, such as family trees or geographical locations. With this programs capability of comparing two articles, it represent a unique aspect that has not been published yet, last but not least because all articles can also be analyzed and compared without restrictions according to type, genre or concept.

*What are the future prospects for the program?*

In the future, the program will be accessible online. For this purpose, I am already testing various publication platforms, including wiki tools that make publication on their servers possible. However, new skills must be acquired, such as working in new environments such as "Flask" and creating new file formats such as CSS and HTML.

*Are further visualizations planned?*

Yes! The visualizations implemented so far already work quite well, but depending on the articles selected, they may pose problems in terms of insight potential due to the amount of data displayed. Unfortunately, the sunburst diagram cannot be implemented more elegantly because there are no shared entities in the plotly code at the base level (root).

*What are the advantages and disadvantages of the program?*

__Pros__:

- Model for further work on the Wikidata API: Represents an example of implementing the Wikidata API for other programs (= much simpler than the Wikidata documentation)
- Efficiency: Saves time and effort to explore new fields of knowledge
- Basis for constructive information gathering: Provides clues for further research
- Ease of use: Intuitive search and prepared presentation of Wikidata information
- Clarity: Quickly capture relevant information about Wikidata items via sunburst diagram
- Data visualization: Diagrams show the scope of items and relationships between items
- Flexibility: Possibility to query and display non-specific items

__Cons__:

- Dependency on Wikidata: Data set is fundamentally dependent on the availability and accuracy of Wikidata data, so it does not offer a guaranteed representation of reality
- Limited representation of data: So far, no representation has been implemented in other formats that show further connections between items, such as networks or statistical graphs
- Limited support for complex data: So far the data set only consists of statements with “datatype == wikibase-item”, i.e. other data types such as numbers, time information or geodata are not taken into account
- Not primarily suitable for serious science and research: Due to a lack of data integrity, the tool is not intended for professional discussion of information
- 

*Known issues*
- Network Graph breaks when not receiving any values for a node
