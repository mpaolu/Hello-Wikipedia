import requests
import inquirer
import pandas as pd
import json
import os
import plotly.graph_objects as go
import plotly.express as px
import networkx as nx
from colorama import Style, Fore


def clear_screen():
    """
    Clear the terminal screen based on the operating system.
    """
    os.system('cls' if os.name == 'nt' else 'clear')

def introduction():
    """
    Print an introduction to the program, explaining its purpose, usage, and disclaimer.
    """
    clear_screen()

    print(f"{Fore.GREEN}{Style.BRIGHT}Welcome to \"Hello, Wikipedia!\"{Style.RESET_ALL}")
    print("\n")
    print("\033[4mA comparison tool from Maximilian Paolucci at Chemnitz University of Technology\033[0m: ")
    print("This tool allows you to compare common properties and values between two Wikidata entities.")
    print("You will be prompted to enter the names or IDs of the entities you want to compare.")
    print("Once you have selected the two Wikidata items from the lists, the program fetches thier data and information via the Wikidata API and statistics, tables and visualisations are beeing created.")
    print("The results are stored locally for further use in the program's location in the \"wikidata_data\" folder.")


    print("\nHow to read Wikidata Information:")
    print(f"  - A {Fore.RED}Wikidata item{Style.RESET_ALL} represents a concept or object, identified by a unique identifier (QID), and contains:")
    print(f"    - {Fore.BLUE}Properties{Style.RESET_ALL}: Attributes or characteristics of the item, providing various aspects of its description.")
    print(f"    - {Fore.MAGENTA}Values{Style.RESET_ALL}: Data associated with the properties, which can be simple (e.g., strings or numbers) or complex (e.g., another Wikidata item or date).")
    print(f"    - {Fore.GREEN}Datavalues{Style.RESET_ALL}: Additional details specifying the nature of complex values, such as data type and precision.")

    print(f"{Fore.LIGHTBLUE_EX}{Style.BRIGHT}\nWikidata Licensing Information:{Style.RESET_ALL}")
    print("  - The data utilized in this tool is sourced from Wikidata, a freely available knowledge base.")
    print("  - Wikidata content is licensed under the Creative Commons Zero (CC0) License, making it effectively public domain and free to use for any purpose, without attribution requirements.")
    print("  - For more details on Wikidata licensing, please refer to: https://www.wikidata.org/wiki/Wikidata:Licensing")
    print("\n")

    print(f"{Fore.LIGHTRED_EX}{Style.BRIGHT}Disclaimer:{Style.RESET_ALL}")
    print("    All results and visualizations provided by this tool are based on Wikidata's structured datasets and should therefore not be seen as a representation of reality.")
    print("    The creation and editing of these datasets on Wikidata.org relies on the collaboration of many editors worldwide and in some cases cannot represent a complete or truthful statement of facts.")
    print("    Please keep this in mind when using this tool!")
    print("    -> For more information see readme.txt")

    print("\n")
    print(f"{Fore.GREEN}Let's get started!{Style.RESET_ALL}")


def get_wikidata_suggestions(search_term):
    """
    Get suggestions for Wikidata entities based on the search term.

    Args:
    - search_term (str): The search term entered by the user.

    Returns:
    - suggestions (list): A list of dictionaries containing suggestions for Wikidata entities, including ID, label, and description.
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
    Prompt the user to select an item from a list of suggestions.

    Args:
    - suggestions (list): A list of dictionaries containing suggestions for Wikidata entities.

    Returns:
    - item_id (str): The ID of the selected Wikidata item.
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
    Fetch data for a Wikidata item using its ID.

    Args:
    - item_id (str): The ID of the Wikidata item.

    Returns:
    - filtered_item_data (dict): Filtered data for the Wikidata item, including claims.
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
    - item_ids (list): A list of item IDs.

    Returns:
    - labels (dict): A dictionary mapping item IDs to their corresponding labels.
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
    Create a pandas DataFrame from Wikidata item data.

    Args:
    - item_data (dict): Data for the Wikidata item, including claims.
    - item_label (str): The label of the Wikidata item.

    Returns:
    - dataframe (pd.DataFrame): A pandas DataFrame containing the item's data.
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
    Compare data between two pandas DataFrames representing Wikidata items.

    Args:
    - item1_df (pd.DataFrame): DataFrame for the first Wikidata item.
    - item2_df (pd.DataFrame): DataFrame for the second Wikidata item.

    Returns:
    - merged_df (pd.DataFrame): Merged DataFrame containing data from both items.
    - combined_df (pd.DataFrame): Combined DataFrame containing data from both items.
    - common_df (pd.DataFrame): DataFrame containing common data between the items.
    - different_df (pd.DataFrame): DataFrame containing different data between the items.
    - common_combined_df (pd.DataFrame): Combined DataFrame of common data between the items.
    """
    merged_df = pd.merge(item1_df, item2_df, on='Property', suffixes=('_item1', '_item2'))
    combined_df = pd.concat([item1_df, item2_df], ignore_index=True)
    common_df = merged_df[merged_df['Value_item1'] == merged_df['Value_item2']]
    different_df = merged_df[merged_df['Value_item1'] != merged_df['Value_item2']]

    common_combined_df = pd.concat([
        common_df[['Item_item1', 'Property', 'Value_item1']].rename(
            columns={'Item_item1': 'Item', 'Value_item1': 'Value'}),
        common_df[['Item_item2', 'Property', 'Value_item2']].rename(
            columns={'Item_item2': 'Item', 'Value_item2': 'Value'})
    ], ignore_index=True)

    common_combined_df.columns = ['Item', 'Property', 'Value']

    return merged_df, combined_df, common_df, different_df, common_combined_df



def dumps(item1_id, item1_data, item1_df, item2_id, item2_data, item2_df, common_df, different_df, combined_df, common_combined_df, merged_df, folder_name='wikidata_data'):
    """
    Dump data and statistics to JSON and CSV files.

    Args:
    - item1_id (str): ID of the first Wikidata item.
    - item1_data (dict): Data for the first Wikidata item.
    - item1_df (pd.DataFrame): DataFrame for the first Wikidata item.
    - item2_id (str): ID of the second Wikidata item.
    - item2_data (dict): Data for the second Wikidata item.
    - item2_df (pd.DataFrame): DataFrame for the second Wikidata item.
    - common_df (pd.DataFrame): DataFrame containing common data between the items.
    - different_df (pd.DataFrame): DataFrame containing different data between the items.
    - combined_df (pd.DataFrame): Combined DataFrame containing data from both items.
    - common_combined_df (pd.DataFrame): Combined DataFrame of common data between the items.
    - merged_df (pd.DataFrame): Merged DataFrame containing data from both items.
    - folder_name (str, optional): Name of the folder to save data. Defaults to 'wikidata_data'.
    """
    script_dir = os.path.dirname(__file__)
    folder_path = os.path.join(script_dir, folder_name)

    json_folder_name = os.path.join(folder_path, 'json')
    os.makedirs(json_folder_name, exist_ok=True)

    with open(os.path.join(json_folder_name, 'data1.json'), "w") as file: json.dump({"entities": {item1_id: {"claims": item1_data}}}, file, indent=2)
    with open(os.path.join(json_folder_name, 'data2.json'), "w") as file: json.dump({"entities": {item2_id: {"claims": item2_data}}}, file, indent=2)

    csv_folder_name = os.path.join(folder_path, 'csv')
    os.makedirs(csv_folder_name, exist_ok=True)

    item1_df.to_csv(os.path.join(csv_folder_name, 'data1.csv'), index=False)
    item2_df.to_csv(os.path.join(csv_folder_name, 'data2.csv'), index=False)
    combined_df.to_csv(os.path.join(csv_folder_name, 'combined.csv'), index=False)
    common_df.to_csv(os.path.join(csv_folder_name, 'common.csv'), index=False)
    different_df.to_csv(os.path.join(csv_folder_name, 'different.csv'), index=False)
    common_combined_df.to_csv(os.path.join(csv_folder_name, 'common_combined.csv'), index=False)
    merged_df.to_csv(os.path.join(csv_folder_name, 'merged.csv'), index=False)

    print(f"{Fore.GREEN}\nData is saved as .json and .csv under 'wikidata_data' folder.\n{Style.RESET_ALL}")


def statistics(common_df, different_df):
    """
    Compute statistics based on common and different data between two items.

    Args:
    - common_df (pd.DataFrame): DataFrame containing common data between the items.
    - different_df (pd.DataFrame): DataFrame containing different data between the items.

    Returns:
    - combined_statistics (dict): Dictionary containing computed statistics.
    """
    combined_statistics = {}

    common_properties = common_df['Property'].unique()
    combined_statistics['Common Properties'] = len(common_properties)

    common_values_item1 = common_df['Value_item1'].unique()
    common_values_item2 = common_df['Value_item2'].unique()
    common_values = set(common_values_item1).intersection(common_values_item2)
    combined_statistics['Common Values'] = len(common_values)

    different_properties = different_df['Property'].unique()
    combined_statistics['Different Properties'] = len(different_properties)

    different_values_item1 = different_df['Value_item1'].unique()
    different_values_item2 = different_df['Value_item2'].unique()
    different_values = set(different_values_item1).symmetric_difference(different_values_item2)
    combined_statistics['Different Values'] = len(different_values)

    for key, value in combined_statistics.items():
        print(f"{key}: {value}")

    return combined_statistics


def create_sankey_diagram(df, df_name):
    """
    Create a Sankey diagram based on data in a pandas DataFrame.

    Args:
    - df (pd.DataFrame): DataFrame containing data for the Sankey diagram.
    - df_name (str): Name of the DataFrame used for the diagram.
    """
    items = df['Item'].unique()
    properties = df['Property'].unique()
    values = df['Value'].unique()

    item_indices = {item: i for i, item in enumerate(items)}
    property_indices = {prop: i + len(items) for i, prop in enumerate(properties)}
    value_indices = {value: i + len(items) + len(properties) for i, value in enumerate(values)}

    sources = []
    targets = []

    for _, row in df.iterrows():
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
            color="lightblue",
        ),
        link=dict(
            source=sources,
            target=targets,
            value=[1] * len(sources),
            color="rgba(0, 0, 255, 0.2)",
        ))])

    fig.update_layout(
        title=f"Sankey Diagram for {df_name}",
        font=dict(size=12, color='black'),
        plot_bgcolor='white',
        margin=dict(l=10, r=10, t=40, b=10),
    )

    fig.update_xaxes(showgrid=False, zeroline=False)
    fig.update_yaxes(showgrid=False, zeroline=False)

    fig.show()


def sunburst(df):
    """
    Create a sunburst plot based on data in a pandas DataFrame.

    Args:
    - df (pd.DataFrame): DataFrame containing data for the sunburst plot.
    """
    fig = px.sunburst(df, path=['Item', 'Property', 'Value'])
    fig.show()


def create_network_graph(combined_df, df_name):
    """
    Create a network graph based on data in a pandas DataFrame.

    Args:
    - combined_df (pd.DataFrame): DataFrame containing data for the network graph.
    - df_name (str): Name of the DataFrame used for the graph.
    """
    G = nx.DiGraph()

    nodes = set()
    edges = []

    for _, row in combined_df.iterrows():
        nodes.add(row['Item'])
        nodes.add(row['Property'])
        nodes.add(row['Value'])
        edges.append((row['Item'], row['Property']))
        edges.append((row['Property'], row['Value']))

    G.add_nodes_from(nodes)
    G.add_edges_from(edges)

    pos = nx.spring_layout(G)

    x_values = [pos[node][0] for node in nodes]
    y_values = [pos[node][1] for node in nodes]

    node_trace = go.Scatter(
        x=x_values,
        y=y_values,
        mode='markers+text',
        marker=dict(
            size=20,
            color='skyblue',
            line=dict(width=2, color='black')
        ),
        text=list(nodes),
        hoverinfo='text',
        name='Nodes',
        textposition="bottom center",
        textfont=dict(size=12)
    )

    edge_x = []
    edge_y = []
    for edge in edges:
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])

    edge_trace = go.Scatter(
        x=edge_x,
        y=edge_y,
        mode='lines',
        line=dict(width=1, color='gray'),
        hoverinfo='none',
        name='Edges'
    )

    fig = go.Figure(
        data=[node_trace, edge_trace],
        layout=dict(
            title=f'Network Graph for {df_name}',
            showlegend=False,
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)
        )
    )

    fig.show()


def main():
    """
    Main function to orchestrate the execution of the program.
    """
    introduction()

    user_search1 = input("Enter the ID or name for the first Wikidata object: ")
    suggestions1 = get_wikidata_suggestions(user_search1)
    item1_id = select_item(suggestions1)
    item1_label = get_item_labels([item1_id])[item1_id]
    item1_data = get_wikidata_item_data(item1_id)

    user_search2 = input("Enter the ID or name for the second Wikidata object: ")
    suggestions2 = get_wikidata_suggestions(user_search2)
    item2_id = select_item(suggestions2)
    item2_label = get_item_labels([item2_id])[item2_id]
    item2_data = get_wikidata_item_data(item2_id)

    item1_df = create_dataframe(item1_data, item1_label)
    item2_df = create_dataframe(item2_data, item2_label)
    merged_df, combined_df, common_df, different_df, common_combined_df = compare_dataframes(item1_df, item2_df)

    dumps(item1_id, item1_data, item1_df, item2_id, item2_data, item2_df, common_df, different_df, combined_df, common_combined_df, merged_df)

    combined_statistics = statistics(common_df, different_df)

    print("\n")
    print(f"{Fore.GREEN}Common Properties with common Values: {Style.RESET_ALL}")
    print(f"For more information see common.csv in the wikidata_data folder")
    print(common_df[['Property', 'Value_item1', 'Value_item2']])
    print("\n")
    print(f"{Fore.GREEN}Common Properties with different Values: {Style.RESET_ALL}")
    print(f"For more information see different.csv in the wikidata_data folder")
    print(different_df[['Property', 'Value_item1', 'Value_item2']])
    print("\n")

    create_sankey_diagram(common_combined_df, "common Properties with common Values (common_combined_df)")
    create_sankey_diagram(combined_df, "all Properties and with their Values (combined_df)")

    create_network_graph(common_combined_df, 'common Properties with common Values (common_combined_df)')
    create_network_graph(combined_df, 'all Properties and with their Values (combined_df)')

    sunburst(item1_df)
    sunburst(item2_df)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"{Fore.RED}\nExiting the program. Goodbye!{Style.RESET_ALL}")

