# Code by md_shadab_alam@outlook.com

import polars as pl
import matplotlib.pyplot as plt
import numpy as np
import mpld3


# Define a custom renaming logic based on column indices
def rename_logic(index):
    # Example renaming logic: prepend "new_" to each name
    return f"new_{index}"


# Function to process a column and calculate percentages and counts
def process_column(data):
    option_counts = {}
    for row in data:
        options = [option.strip().lower() for option in row.split(',')]
        for option in options:
            option_counts[option] = option_counts.get(option, 0) + 1
    total_participants = len(data)
    option_percentages = {option: (count / total_participants) * 100 for option, count in option_counts.items()}
    return option_percentages, option_counts


def gender_distribution(df):
    # Count the occurrences of each gender
    gender_counts = df.groupby('Gender').agg(pl.count('Gender').alias('count')).collect()

    # Extract data for plotting
    genders = gender_counts['Gender'].to_list()
    counts = gender_counts['count'].to_list()

    # Plot the counts
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.bar(genders, counts, width=0.8, color=['pink', 'blue'], edgecolor='black')
    ax.set_title('Gender Count')
    ax.set_xlabel('Gender')
    ax.set_ylabel('Count')
    ax.set_xticks(range(len(genders)))
    ax.set_xticklabels(genders, rotation=0)

    # Save the figure in different formats
    plt.savefig("plots/gender.eps")
    plt.savefig("plots/gender.png")

    # Save the figure as an HTML file
    mpld3.save_html(fig, "plots/gender.html")
    plt.show()


def age_distribution(df):
    # Count the occurrences of each gender
    age_counts = df.group_by('Age').agg(pl.count('Age').alias('count')).collect()

    # Extract data for plotting
    age = age_counts['Age'].to_list()
    counts = age_counts['count'].to_list()

    # Plot the counts
    plt.figure(figsize=(8, 6))
    plt.bar(age, counts, width=0.8, edgecolor='black')
    plt.title('Age Distribition')
    plt.xlabel('Age (in years)')
    plt.ylabel('Count')
    plt.xticks(rotation=0)
    plt.savefig("plots/age.eps")
    plt.savefig("plots/age.html")
    plt.savefig("plots/age.png")


def demographic_distribution(df):
    # Group by country and count occurrences
    age_counts = df.group_by('Country').agg(pl.count('Country').alias('count')).collect()

    # Extract data for plotting
    age = age_counts['Country'].to_list()
    counts = age_counts['count'].to_list()

    # Plot the counts
    plt.figure(figsize=(8, 6))
    plt.bar(age, counts, width=0.8, edgecolor='black')
    plt.title('Age Distribition')
    plt.xlabel('Age (in years)')
    plt.ylabel('Count')
    plt.xticks(rotation=0)
    plt.savefig("plots/country.eps")
    plt.savefig("plots/country.html")
    plt.savefig("plots/country.png")


def use_micro_mobility(df):
    frequency_counts = df.group_by("Micro-mobillity frequency").agg(pl.count(
        'Micro-mobillity frequency').alias('count')).collect()

    # Extract data for plotting
    frequency = frequency_counts['Micro-mobillity frequency'].to_list()
    counts = frequency_counts['count'].to_list()

    # Plot the counts
    fig, ax = plt.subplots()
    explode = (0, 0, 0, 0, 0.1, 0)
    ax.pie(counts, explode=explode, labels=frequency, autopct='%1.1f%%',
           shadow={'ox': -0.04, 'edgecolor': 'none', 'shade': 0.9}, startangle=90)
    plt.title('Use of micro-mobility')
    plt.savefig("plots/micro-mobility.eps")
    plt.savefig("plots/micro-mobility.html")
    plt.savefig("plots/micro-mobility.png")


def use_bus(df):
    frequency_counts = df.group_by("Bus frequency").agg(pl.count(
        'Bus frequency').alias('count')).collect()

    # Extract data for plotting
    frequency = frequency_counts['Bus frequency'].to_list()
    counts = frequency_counts['count'].to_list()

    # Plot the counts
    fig, ax = plt.subplots()
    explode = (0, 0, 0, 0, 0.1)
    ax.pie(counts, explode=explode, labels=frequency, autopct='%1.1f%%',
           shadow={'ox': -0.04, 'edgecolor': 'none', 'shade': 0.9}, startangle=90)

    plt.title('Use of public bus (per week)')
    plt.savefig("plots/bus_use.eps")
    plt.savefig("plots/bus_use.html")
    plt.savefig("plots/bus_use.png")


def viewing_assistance(df):
    frequency_counts = df.group_by("Assistance feature valuable?").agg(pl.count(
        'Assistance feature valuable?').alias('count')).collect()

    # Extract data for plotting
    frequency = frequency_counts['Assistance feature valuable?'].to_list()
    counts = frequency_counts['count'].to_list()

    # Plot the counts
    fig, ax = plt.subplots()
    explode = (0, 0, 0, 0.1)
    ax.pie(counts, explode=explode, labels=frequency, autopct='%1.1f%%',
           shadow={'ox': -0.04, 'edgecolor': 'none', 'shade': 0.9}, startangle=90)

    plt.title('The Role of Viewing Assistance in Enhancing Navigation and Overcoming Language Barriers')
    plt.savefig("plots/viewing_assistance.eps")
    plt.savefig("plots/viewing_assistance.html")
    plt.savefig("plots/viewing_assistance.png")


def NFC(df):
    frequency_counts = df.group_by("NFC feature valuable").agg(pl.count(
        'NFC feature valuable').alias('count')).collect()

    # Extract data for plotting
    frequency = frequency_counts['NFC feature valuable'].to_list()
    counts = frequency_counts['count'].to_list()

    # Plot the counts
    fig, ax = plt.subplots()
    explode = (0, 0, 0, 0.1)
    ax.pie(counts, explode=explode, labels=frequency, autopct='%1.1f%%',
           shadow={'ox': -0.04, 'edgecolor': 'none', 'shade': 0.9}, startangle=90)

    plt.title('The Role of NFC while boarding')
    plt.savefig("plots/NFC.eps")
    plt.savefig("plots/NFC.html")
    plt.savefig("plots/NFC.png")


def info_preboarding(df):
    # Extract and process data from both columns
    column_10_data = df.select('Information required preboarding (mobile screen)').collect().to_series()
    column_11_data = df.select('Information required preboarding (public screen)').collect().to_series()

    percentages_10, counts_10 = process_column(column_10_data)
    percentages_11, counts_11 = process_column(column_11_data)

    # Get a sorted list of unique options from both columns
    unique_options = sorted(set(percentages_10.keys()).union(set(percentages_11.keys())))

    # Create lists for plotting
    values_10 = [percentages_10.get(option, 0) for option in unique_options]
    values_11 = [percentages_11.get(option, 0) for option in unique_options]

    counts_values_10 = [counts_10.get(option, 0) for option in unique_options]
    counts_values_11 = [counts_11.get(option, 0) for option in unique_options]

    # Define bar width
    bar_width = 0.35
    index = np.arange(len(unique_options))

    # Plot the data
    plt.figure(figsize=(14, 8))
    bar1 = plt.barh(index, values_10, bar_width, color='skyblue', label='Mobile Screen')  # noqa:F841
    bar2 = plt.barh(index + bar_width, values_11, bar_width, color='salmon', label='Public Screen')  # noqa:F841

    # Add text labels at the end of each bar
    for i in range(len(index)):
        plt.text(values_10[i], index[i], str(counts_values_10[i]),
                 va='center', ha='left', color='black', fontweight='bold')
        plt.text(values_11[i], index[i] + bar_width, str(counts_values_11[i]),
                 va='center', ha='left', color='black', fontweight='bold')

    plt.xlabel('Percentage')
    # plt.ylabel('Option')
    # plt.title('Percentage of Participants Choosing Each Option')
    plt.yticks(index + bar_width / 2, unique_options)
    plt.xticks(range(0, 101, 10))  # Set x-axis ticks to come at every 10 units
    plt.legend(title='Screen Type')

    plt.tight_layout()  # Adjust layout to prevent label cutoff
    plt.savefig("plots/info_mobile_pre.eps")
    plt.savefig("plots/info_mobile_pre.html")
    plt.savefig("plots/info_mobile_pre.png")
    plt.show()


def info_onboarding(df):
    # Extract and process data from both columns
    column_10_data = df.select('Information required onboarding (public screen)').collect().to_series()
    column_11_data = df.select('Information required onboarding (private screen)').collect().to_series()
    column_12_data = df.select('Information required onboarding (mobile screen)').collect().to_series()

    percentages_10, counts_10 = process_column(column_10_data)
    percentages_11, counts_11 = process_column(column_11_data)
    percentages_12, counts_12 = process_column(column_12_data)

    # Get a sorted list of unique options from both columns
    unique_options = sorted(set(percentages_10.keys()).union(set(
        percentages_11.keys()).union(set(percentages_12.keys()))))

    # Create lists for plotting
    values_10 = [percentages_10.get(option, 0) for option in unique_options]
    values_11 = [percentages_11.get(option, 0) for option in unique_options]
    values_12 = [percentages_12.get(option, 0) for option in unique_options]

    counts_values_10 = [counts_10.get(option, 0) for option in unique_options]
    counts_values_11 = [counts_11.get(option, 0) for option in unique_options]
    counts_values_12 = [counts_12.get(option, 0) for option in unique_options]

    # Define bar width
    bar_width = 0.25  # Adjusted the bar width to fit three bars
    index = np.arange(len(unique_options))

    # Plot the data
    plt.figure(figsize=(14, 8))
    bar1 = plt.barh(index, values_10, bar_width, color='skyblue', label='Public Screen')
    bar2 = plt.barh(index + bar_width, values_11, bar_width, color='salmon', label='Private Screen')
    bar3 = plt.barh(index + (2 * bar_width), values_12, bar_width, color='lightgreen', label='Mobile Screen')

    # Add text labels at the end of each bar
    for i in range(len(index)):
        plt.text(values_10[i], index[i], str(counts_values_10[i]),
                 va='center', ha='left', color='black', fontweight='bold')
        plt.text(values_11[i], index[i] + bar_width, str(counts_values_11[i]),
                 va='center', ha='left', color='black', fontweight='bold')
        plt.text(values_12[i], index[i] + (2 * bar_width), str(counts_values_12[i]),
                 va='center', ha='left', color='black', fontweight='bold')

    plt.xlabel('Percentage')
    # plt.ylabel('Option')
    # plt.title('Percentage of participants choosing information after boarding on the shuttle bus')
    plt.yticks(index + bar_width, unique_options)
    plt.xticks(range(0, 101, 10))  # Set x-axis ticks to come at every 10 units
    plt.legend(title='Screen Type')

    plt.tight_layout()  # Adjust layout to prevent label cutoff
    plt.savefig("plots/info_onboard.eps")
    plt.savefig("plots/info_onboard.html")
    plt.savefig("plots/info_onboard.png")
    plt.show()


csv_file_path = 'response.csv'

# Read the CSV file into a Polars LazyFrame
dataframe = pl.scan_csv(csv_file_path)

# Filter out the responses who haven't read the instruction or doesn't gave the consent
dataframe = dataframe.filter((pl.col("Have you read and understood the above instructions?") == "Yes")
                             & (pl.col("Consent to participate") == "Yes"))

# Replace all variation of Netherlands to maintain consistency
dataframe = dataframe.with_columns(pl.col("Country").str.replace_many(
    ["NL", "The Netherlands", "netherlands", "Netherlands "], "Netherlands"))

# Replace all variation of Germany to maintain consistency
dataframe = dataframe.with_columns(pl.col("Country").str.replace_many(
    ["Germany "], "Germany"))

# Replace all variation of India to maintain consistency
dataframe = dataframe.with_columns(pl.col("Country").str.replace_many(
    ["India "], "India"))

gender_distribution(dataframe)
# age_distribution(dataframe)
# demographic_distribution(dataframe)
# use_micro_mobility(dataframe)
# use_bus(dataframe)
# viewing_assistance(dataframe)
# NFC(dataframe)
# info_preboarding(dataframe)
# info_onboarding(dataframe)

print("Execution Completed")
