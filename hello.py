import plotly.graph_objects as go
import pandas as pd
import json
import requests
import os
import inquirer
from colorama import Fore, Style


# TODO: Implement Showcases
# TODO: Make Sankey Colorful
# TODO: Implement Sunburst Chart(s) For combined_df

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def introduction():
    """
    Greets the user and provides a brief introduction to the program as well as the usage of the Wikidata API.

    Args:
        None

    Returns:
        None
    """
    clear_screen()
    print(f"{Fore.GREEN}{Style.BRIGHT}Welcome to \"Hello, Wikipedia!\"{Style.RESET_ALL}")
    print("This tool allows you to compare common properties and values between two Wikidata entities.")
    print("You will be prompted to enter the names or IDs of the entities you want to compare.")

    print("\nHow Wikidata Information is Organized:")
    print(f"  - An {Fore.RED}item{Style.RESET_ALL} represents a concept or object, identified by a unique identifier (QID), and has:")
    print(f"    - {Fore.BLUE}Properties{Style.RESET_ALL}: Claims or attributes about the item. These describe various aspects of the item.")
    print(f"    - {Fore.MAGENTA}Values{Style.RESET_ALL}: Simple (e.g., string or number) or complex (e.g., another {Fore.RED}item{Style.RESET_ALL} or date).")
    print(f"    - {Fore.GREEN}Datavalues{Style.RESET_ALL}: Provide detailed information about complex {Fore.MAGENTA}values{Style.RESET_ALL}. Datavalues help specify the nature of the value, such as the data type (e.g., time, quantity) and additional details.")

    print(f"{Fore.LIGHTBLUE_EX}{Style.BRIGHT}\nWikidata Licensing Information:{Style.RESET_ALL}")
    print("  - The data used in this tool is sourced from Wikidata, a freely available knowledge base.")
    print("  - Wikidata content is licensed under the Creative Commons Zero (CC0) License, making it effectively public domain and free to use for any purpose, without the need for attribution.")
    print("  - For more details on Wikidata licensing, please refer to: https://creativecommons.org/publicdomain/zero/1.0/")
    print("\n")

    input("Press Enter to continue...")
    print("\n")


def get_wikidata_suggestions(search_term):
    """
    Get suggestions for Wikidata items based on the given search term.

    Args:
        search_term (str): The search term to query Wikidata.

    Returns:
        list: A list of dictionaries containing suggestions for Wikidata items.
    """
    base_url = "https://www.wikidata.org/w/api.php"
    params = {
        "action": "wbsearchentities",
        "format": "json",
        "language": "en",
        "search": search_term
    }

    response = requests.get(base_url, params=params)
    data = response.json()

    suggestions = []
    for result in data.get("search", []):
        suggestions.append({
            "id": result["id"],
            "label": result["label"],
            "description": result.get("description", "")
        })

    return suggestions

def select_item(suggestions):
    """
    Prompts the user to select from a list of Wikidata suggestions and returns the selected ID.

    Args:
        suggestions (list): A list of Wikidata suggestions to be presented to the user.

    Returns:
        str: The selected Wikidata ID chosen by the user.
    """
    questions = [
        inquirer.List(
            "selected_item",
            message="Select an item",
            choices=[f"({item['id']}) {item['label']} - {item['description']}" for item in suggestions],
        ),
    ]

    answers = inquirer.prompt(questions)
    selected_item = answers["selected_item"]

    item_id = selected_item.split(" ")[0][1:-1]

    return item_id

def get_wikidata_item_data(item_id):
    """
    Get data for a specific Wikidata item based on its ID.

    Args:
        item_id (str): The ID of the Wikidata item.

    Returns:
        dict: A dictionary containing data for the specified Wikidata item.
    """
    base_url = "https://www.wikidata.org/w/api.php"
    params = {
        "action": "wbgetentities",
        "format": "json",
        "ids": item_id,
        "props": "claims",
    }

    response = requests.get(base_url, params=params)
    data = response.json()

    filtered_item_data = {
        property_id: claims
        for property_id, claims in data.get("entities", {}).get(item_id, {}).get("claims", {}).items()
        if any(claim.get("mainsnak", {}).get("datatype") == "wikibase-item" for claim in claims)
    }

    return filtered_item_data

def get_item_labels(item_ids):
    """
    Get labels for Wikidata items based on their IDs.

    Args:
        item_ids (list): A list of Wikidata item IDs.

    Returns:
        dict: A dictionary mapping item IDs to their corresponding labels.
    """
    base_url = "https://www.wikidata.org/w/api.php"
    labels = {}
    item_ids = [item_id for item_id in item_ids if item_id]
    batch_size = 50

    for i in range(0, len(item_ids), batch_size):
        batch_ids = "|".join(item_ids[i:i + batch_size])
        params = {
            "action": "wbgetentities",
            "format": "json",
            "ids": batch_ids,
            "props": "labels",
            "languages": "en"
        }

        response = requests.get(base_url, params=params)
        data = response.json()

        for item_id, item_data in data.get("entities", {}).items():
            label = item_data.get("labels", {}).get("en", {}).get("value", item_id)
            labels[item_id] = label

    return labels


def create_dataframe(item_data, item_label):
    """
    Create a Pandas DataFrame from Wikidata item data.

    Args:
        item_data (dict): Data for a Wikidata item.
        item_label (str): The label of the Wikidata item.

    Returns:
        pandas.DataFrame: A DataFrame containing the item data.
    """
    value_data = []

    property_ids = list(item_data.keys())
    property_labels = get_item_labels(property_ids)

    for property_id, claims in item_data.items():
        property_label = property_labels.get(property_id, property_id)
        for claim in claims:
            mainsnak = claim.get('mainsnak', {})
            if mainsnak.get('datatype') == 'wikibase-item':
                value_id = mainsnak.get('datavalue', {}).get('value', {}).get('id')
                value_data.append({'Item': item_label, 'Property': property_label, 'Value': value_id})

    value_ids = [entry['Value'] for entry in value_data]
    value_labels = get_item_labels(value_ids)

    for entry in value_data:
        value_id = entry['Value']
        value_label = value_labels.get(value_id, value_id)
        entry['Value'] = value_label

    dataframe = pd.DataFrame(value_data)
    return dataframe


def compare_dataframes(item1_df, item2_df):
    """
    Compare two Pandas DataFrames containing Wikidata item data.

    Args:
        item1_df (pandas.DataFrame): The DataFrame for the first Wikidata item.
        item2_df (pandas.DataFrame): The DataFrame for the second Wikidata item.

    Returns:
        tuple: A tuple containing the merged DataFrame, combined DataFrame,
        DataFrame of common properties with identical values, and DataFrame of
        common properties with different values.
    """
    merged_df = pd.merge(item1_df, item2_df, on='Property', suffixes=('_item1', '_item2'))
    combined_df = pd.concat([item1_df, item2_df], ignore_index=True)
    common_df = merged_df[merged_df['Value_item1'] == merged_df['Value_item2']]
    different_df = merged_df[merged_df['Value_item1'] != merged_df['Value_item2']]

    return merged_df, combined_df, common_df, different_df

def dumps(item1_id, item1_data, item1_df, item2_id, item2_data, item2_df, common_df, different_df, combined_df, combined_json, folder_name='wikidata_data'):
    """
    Dump data to JSON and CSV files.

    Args:
        item1_id (str): The ID of the first Wikidata item.
        item1_data (dict): Data for the first Wikidata item.
        item1_df (pandas.DataFrame): The DataFrame for the first Wikidata item.
        item2_id (str): The ID of the second Wikidata item.
        item2_data (dict): Data for the second Wikidata item.
        item2_df (pandas.DataFrame): The DataFrame for the second Wikidata item.
        common_df (pandas.DataFrame): DataFrame of common properties with identical values.
        different_df (pandas.DataFrame): DataFrame of common properties with different values.
        combined_df (pandas.DataFrame): Combined DataFrame of both Wikidata items.
        combined_json (str): JSON representation of the combined DataFrame.
        folder_name (str, optional): Name of the folder to save the files. Defaults to 'wikidata_data'.
    """
    script_dir = os.path.dirname(__file__)
    folder_path = os.path.join(script_dir, folder_name)

    json_folder_name = os.path.join(folder_path, 'json')
    os.makedirs(json_folder_name, exist_ok=True)

    with open(os.path.join(json_folder_name, 'data1.json'), "w") as file: json.dump({"entities": {item1_id: {"claims": item1_data}}}, file, indent=2)
    with open(os.path.join(json_folder_name, 'data2.json'), "w") as file: json.dump({"entities": {item2_id: {"claims": item2_data}}}, file, indent=2)
    with open(os.path.join(json_folder_name, 'combined.json'), "w") as file: file.write(combined_json)

    csv_folder_name = os.path.join(folder_path, 'csv')
    os.makedirs(csv_folder_name, exist_ok=True)

    item1_df.to_csv(os.path.join(csv_folder_name, 'data1.csv'), index=False)
    item2_df.to_csv(os.path.join(csv_folder_name, 'data2.csv'), index=False)
    combined_df.to_csv(os.path.join(csv_folder_name, 'combined.csv'), index=False)
    common_df.to_csv(os.path.join(csv_folder_name, 'common.csv'), index=False)
    different_df.to_csv(os.path.join(csv_folder_name, 'different.csv'), index=False)

    print("\nData is saved as .json and .csv under 'wikidata_data' folder.\n")


def statistics(common_df, different_df):
    """
    Calculate statistics on common and different properties/values between two Wikidata items.

    Args:
        common_df (pandas.DataFrame): DataFrame of common properties with identical values.
        different_df (pandas.DataFrame): DataFrame of common properties with different values.

    Returns:
        dict: A dictionary containing statistics on common and different properties/values.
    """
    combined_statistics = {}

    common_properties = common_df['Property'].unique()
    combined_statistics['common_properties'] = len(common_properties)

    common_values_item1 = common_df['Value_item1'].unique()
    common_values_item2 = common_df['Value_item2'].unique()
    common_values = set(common_values_item1).intersection(common_values_item2)
    combined_statistics['common_values'] = len(common_values)

    different_properties = different_df['Property'].unique()
    combined_statistics['different_properties'] = len(different_properties)

    different_values_item1 = different_df['Value_item1'].unique()
    different_values_item2 = different_df['Value_item2'].unique()
    different_values = set(different_values_item1).symmetric_difference(different_values_item2)
    combined_statistics['different_values'] = len(different_values)

    return combined_statistics

def conversion(combined_df):
    """
    Convert a Pandas DataFrame to a JSON string.

    Args:
        combined_df (pandas.DataFrame): The DataFrame to convert.

    Returns:
        str: The JSON representation of the DataFrame.
    """
    combined_json = combined_df.to_json(orient='records', lines=True)
    return "[" + combined_json.replace('\n', ',') + "]"


def create_sankey_diagram(combined_df):
    """
    Create a Sankey diagram using Plotly based on Wikidata item data.

    Args:
        combined_df (pandas.DataFrame): The combined DataFrame of Wikidata items.
    """
    items = combined_df['Item'].unique()
    properties = combined_df['Property'].unique()
    values = combined_df['Value'].unique()

    item_indices = {item: i for i, item in enumerate(items)}
    property_indices = {prop: i + len(items) for i, prop in enumerate(properties)}
    value_indices = {value: i + len(items) + len(properties) for i, value in enumerate(values)}

    sources = []
    targets = []

    for _, row in combined_df.iterrows():
        sources.append(item_indices[row['Item']])
        targets.append(property_indices[row['Property']])
        sources.append(property_indices[row['Property']])
        targets.append(value_indices[row['Value']])

    labels = list(item_indices.keys()) + list(property_indices.keys()) + list(value_indices.keys())

    fig = go.Figure(data=[go.Sankey(
        node=dict(
            pad=15,
            thickness=20,
            line=dict(color="black", width=0.5),
            label=labels,
            color="blue"
        ),
        link=dict(
            source=sources,
            target=targets,
            value=[1]*len(sources)
        ))])

    fig.update_layout(title_text="Wikidata Sankey Diagram", font_size=10)
    fig.show()


def main():
    """Main function to run the Wikidata tool."""
    introduction()

    user_search1 = input(f"{Fore.GREEN}{Style.BRIGHT}Enter the ID or name for the first Wikidata object: {Style.RESET_ALL}")
    suggestions1 = get_wikidata_suggestions(user_search1)
    item1_id = select_item(suggestions1)
    item1_label = get_item_labels([item1_id])[item1_id]
    item1_data = get_wikidata_item_data(item1_id)

    user_search2 = input(f"{Fore.GREEN}{Style.BRIGHT}Enter the ID or name for the second Wikidata object: {Style.RESET_ALL}")
    suggestions2 = get_wikidata_suggestions(user_search2)
    item2_id = select_item(suggestions2)
    item2_label = get_item_labels([item2_id])[item2_id]
    item2_data = get_wikidata_item_data(item2_id)

    item1_df = create_dataframe(item1_data, item1_label)
    item2_df = create_dataframe(item2_data, item2_label)
    merged_df, combined_df, common_df, different_df = compare_dataframes(item1_df, item2_df)

    combined_json = conversion(combined_df)
    dumps(item1_id, item1_data, item1_df, item2_id, item2_data, item2_df, common_df, different_df, combined_df, combined_json)

    combined_statistics = statistics(common_df, different_df)

    print(combined_statistics)
    print("\nCommon Properties with identical Values: ")
    print(common_df[['Property', 'Value_item1', 'Value_item2']])
    print("\nCommon Properties with different Values: ")
    print(different_df)

    create_sankey_diagram(combined_df)


if __name__ == "__main__":
    main()
