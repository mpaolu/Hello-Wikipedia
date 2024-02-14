# Wikidata Tool

## Table of Contents
1. [Overview](#overview)
2. [Features](#features)
3. [Installation](#installation)
4. [Usage](#usage)
5. [Dependencies](#dependencies)
6. [Contributing](#contributing)
7. [License](#license)
8. [Project Coherence and Relevance](#project-coherence-and-relevance)

---

## Overview

The Wikidata Tool is a Python program designed to facilitate the comparison and analysis of data from Wikidata, a free and open knowledge base maintained by the Wikimedia Foundation. The tool provides a user-friendly interface to interact with the vast amount of structured data available on Wikidata, enabling users to retrieve, compare, visualize, and analyze information about various entities, including people, places, events, and concepts.

Using the Wikidata Tool, users can efficiently explore relationships between different entities, identify commonalities and differences, and gain insights into the wealth of knowledge stored in Wikidata. Whether conducting research, creating educational materials, or simply satisfying curiosity, the Wikidata Tool offers a versatile platform for harnessing the power of structured data.

---

## Features

- **Search and Selection:** Retrieve suggestions for Wikidata items based on search terms and select items of interest using an interactive prompt.
- **Data Retrieval:** Fetch detailed data for selected Wikidata items, including properties, values, and metadata.
- **Comparison:** Compare data between two Wikidata items to identify common properties/values and differences.
- **Statistical Analysis:** Generate statistics on common and different properties/values to quantify similarities and discrepancies.
- **Visualization:** Create interactive visualizations, including Sankey diagrams and network graphs, to visualize relationships and patterns in the data.
- **Data Export:** Save data and analysis results in JSON and CSV formats for further exploration and documentation.
- **Modular and Extensible:** The codebase is highly modular and extensible, allowing for easy customization and integration with other projects.

---

## Installation

To use the Wikidata Tool, follow these steps:

- Clone or download the repository from GitHub.
- Ensure Python 3.x is installed on your system.

---

## Usage

To run the Wikidata Tool, execute the `hello.py` script:

python3 hello.py

Follow the on-screen instructions to enter search terms, select items, and analyze the data. The tool will generate documentation, save data files, and display visualizations as needed.
Dependencies

The Wikidata Tool relies on the following Python libraries:

Plotly: For creating interactive visualizations.
Pandas: For data manipulation and analysis.
Requests: For making HTTP requests to the Wikidata API.
Inquirer: For interactive user prompts.
JSON: For handling JSON data.
OS: For file system operations.

Ensure these dependencies are installed in your Python environment before running the Wikidata Tool.
Contributing

Contributions to the Wikidata Tool are welcome! Here is a breakdown of the code:

Introduction Function: Provides a welcome message and introduction to the program, explaining its purpose and how to use it.
Wikidata API Functions:
    get_wikidata_suggestions: Retrieves suggestions from Wikidata based on a search term.
    select_item: Prompts the user to select an item from a list of suggestions.
    get_wikidata_item_data: Fetches data for a Wikidata item.
    get_item_labels: Retrieves labels for Wikidata items.
    create_dataframe: Creates a DataFrame from Wikidata item data.
    compare_dataframes: Compares data between two DataFrames.
Data Output Functions:
    dumps: Saves data and results in JSON and CSV formats.
    statistics: Computes and prints statistics about the compared data.
Visualization Functions:
    create_sankey_diagram: Generates a Sankey diagram based on the data.
    create_network_graph: Creates a network graph based on the merged data.
    sunburst: Generates a sunburst chart based on the data.
Main Function: Executes the main logic of the program, prompting the user for input, fetching data, comparing it, and then displaying statistics and visualizations.

License

This project is licensed under the MIT License. See the LICENSE file for details. For any questions, issues, or suggestions, please contact "maximilian.paolucci@s2020.tu-chemnitz.de".
Project Coherence and Relevance

The Wikidata Tool addresses the growing need for efficient data analysis and exploration tools in the era of big data and open knowledge. By focusing on Wikidata, a central repository of structured data with broad coverage across domains, the tool offers a valuable resource for researchers, educators, developers, and enthusiasts seeking to leverage structured knowledge for various purposes.

The coherence and relevance of the Wikidata Tool stem from its alignment with key trends and challenges in the fields of data science, knowledge management, and information retrieval. In today's interconnected world, where information is abundant but often fragmented, tools like the Wikidata Tool play a crucial role in bridging the gap between data sources and end users, enabling seamless access to structured knowledge and insights.

Furthermore, the Wikidata Tool exemplifies best practices in software development, including modular design, extensibility, and usability. By adopting industry-standard libraries and following established coding conventions, the tool ensures reliability, maintainability, and interoperability, thereby enhancing its value and utility for a wide range of users.

Overall, the Wikidata Tool represents a coherent and relevant response to the evolving needs and challenges of data-driven research, education, and innovation. Through ongoing development, collaboration, and community engagement, the tool aims to empower users to harness the full potential of structured data for informed decision-making, knowledge discovery, and societal impact.
