# Code by md_shadab_alam@outlook.com

import polars as pl
import numpy as np
import os
import plotly.graph_objects as go
import plotly.io as pio
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.preprocessing import MultiLabelBinarizer
import common
from custom_logger import CustomLogger
from logmod import logs

logs(show_level='info', show_color=True)
logger = CustomLogger(__name__)  # use custom logger

# set template for plotly output
template = common.get_configs('plotly_template')


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


def process_options(series):
    # Split the comma-separated values, strip whitespace, convert to lowercase, and capitalize first letter
    options_list = series.map_elements(lambda x: [opt.strip().lower().capitalize() for opt in x.split(",")],
                                       return_dtype=pl.List).to_list()

    # Define a mapping for longer option names to shorter versions
    option_mapping = {
        "Safety information and protocols and emergency call option": "Safety information",
    }

    # Apply the mapping and capitalize the first letter of each option
    options_list = [[option_mapping.get(opt, opt).capitalize() for opt in sublist] for sublist in options_list]

    return options_list


def shorten_label(label, col_mapping):
    for long_col, short_col in col_mapping.items():
        label = label.replace(long_col, short_col)
    return label


def gender_distribution_bar(df):
    # Count the occurrences of each gender
    gender_counts = df.group_by('Gender').agg(pl.count('Gender').alias('count')).collect()

    # Extract data for plotting
    genders = gender_counts['Gender'].to_list()
    counts = gender_counts['count'].to_list()

    # Create the bar plot
    fig = go.Figure(data=[
        go.Bar(name='Gender', x=genders, y=counts, marker_color=['red', 'blue'])
    ])

    # Update layout
    fig.update_layout(
        # title='Gender Count',
        xaxis_title='Gender',
        yaxis_title='Count',
        xaxis=dict(tickmode='array', tickvals=genders, ticktext=genders)
    )

    # Save the figure in different formats
    fig.write_image("plots/gender_bar.eps")
    fig.write_image("plots/gender_bar.png", width=1600, height=900, scale=3)

    # Save plot as HTML
    pio.write_html(fig, file="plots/gender.html", auto_open=True)


def gender_distribution_pie(df):
    # Count the occurrences of each gender
    gender_counts = df.group_by('Gender').agg(pl.count('Gender').alias('count')).collect()

    # Extract data for plotting
    genders = gender_counts['Gender'].to_list()
    counts = gender_counts['count'].to_list()

    # Create the pie chart
    fig = go.Figure(data=[
        go.Pie(labels=genders, values=counts, hole=0.0, marker=dict(colors=['red', 'blue']), showlegend=True)
    ])

    # Update layout
    fig.update_layout(
        # title='Gender Distribution',
        legend_title_text="Gender"
    )

    # Save the figure in different formats
    fig.write_image("plots/gender_pie.eps")
    fig.write_image("plots/gender_pie.png", width=1600, height=900, scale=3)

    # Save plot as HTML
    pio.write_html(fig, file="plots/gender_pie.html", auto_open=True)


def age_distribution(df):
    # Count the occurrences of each age
    age_counts = df.group_by('Age').agg(pl.count('Age').alias('count')).collect()

    # Extract data for plotting
    age = age_counts['Age'].to_list()
    counts = age_counts['count'].to_list()

    # Create the bar plot
    fig = go.Figure(data=[
        go.Bar(name='Age', x=age, y=counts, marker_color='blue')
    ])

    # Update layout
    fig.update_layout(
        # title='Age Distribution',
        xaxis_title='Age (in years)',
        yaxis_title='Count',
        xaxis=dict(tickmode='array', tickvals=age, ticktext=age)
    )

    # Save the figure in different formats
    fig.write_image("plots/age.eps")
    fig.write_image("plots/age.png", width=1600, height=900, scale=3)

    # Save plot as HTML
    pio.write_html(fig, file="plots/age.html", auto_open=True)


def demographic_distribution_bar(df):
    # Group by country and count occurrences
    country_counts = df.group_by('Country').agg(pl.count('Country').alias('count')).collect()

    # Extract data for plotting
    countries = country_counts['Country'].to_list()
    counts = country_counts['count'].to_list()

    # Define a list of colors
    colors = ['blue', 'green', 'red', 'purple', 'orange', 'cyan', 'magenta', 'yellow', 'brown', 'pink']

    # If there are more countries than colors, extend the colors list
    while len(colors) < len(countries):
        colors.extend(colors)

    # Create the bar plot
    fig = go.Figure(data=[
        go.Bar(name='Country', x=countries, y=counts, marker_color=colors[:len(countries)])
    ])

    # Update layout
    fig.update_layout(
        # title='Country Distribution',
        xaxis_title='Country',
        yaxis_title='Count',
        xaxis=dict(tickmode='array', tickvals=countries, ticktext=countries)
    )

    # Save the figure in different formats
    fig.write_image("plots/country_bar.eps")
    fig.write_image("plots/country_bar.png", width=1600, height=900, scale=3)

    # Save plot as HTML
    pio.write_html(fig, file="plots/country_bar.html", auto_open=True)


def demographic_distribution_pie(df):
    frequency_counts = df.group_by("Country").agg(pl.count(
        'Country').alias('count')).collect()
    # Extract data for plotting
    frequency = frequency_counts['Country'].to_list()
    counts = frequency_counts['count'].to_list()

    # Create the pie chart
    fig = go.Figure(data=[
        go.Pie(labels=frequency, values=counts, hole=0.0, pull=[0, 0, 0, 0, 0, 0, 0])
    ])

    # Update layout
    fig.update_layout(
        # title='Country Distribution'
        legend_title_text="Country"
    )

    # Save the figure in different formats
    fig.write_image("plots/country_pie.eps")
    fig.write_image("plots/country_pie.png", width=1600, height=900, scale=3)

    # Save plot as HTML
    pio.write_html(fig, file="plots/country_pie.html", auto_open=True)


def use_micro_mobility(df):
    frequency_counts = df.group_by("Micro-mobillity frequency").agg(pl.count(
        'Micro-mobillity frequency').alias('count')).collect()

    # Extract data for plotting
    frequency = frequency_counts['Micro-mobillity frequency'].to_list()
    counts = frequency_counts['count'].to_list()

    # Desired order of the legend items
    desired_order = [
        "Everyday",
        "4 to 6 days a week",
        "1 to 3 days a week",
        "Once a month to once a week",
        "Less than once a month",
        "Never"
    ]

    # Ensure the desired order is respected
    ordered_indices = [frequency.index(item) for item in desired_order if item in frequency]
    ordered_frequency = [frequency[i] for i in ordered_indices]
    ordered_counts = [counts[i] for i in ordered_indices]

    # Create the pie chart
    fig = go.Figure(data=[
        go.Pie(labels=ordered_frequency, values=ordered_counts, hole=0.0,
               pull=[0] * len(ordered_frequency), sort=False)])

    # Update layout
    fig.update_layout(
        legend_title_text='Micro-mobility usage frequency',
        legend=dict(itemsizing='constant', font=dict(size=12))
    )

    # Save the figure in different formats
    fig.write_image("plots/micro-mobility.eps")
    fig.write_image("plots/micro-mobility.png", width=1600, height=900, scale=3)

    # Save plot as HTML
    pio.write_html(fig, file="plots/micro-mobility.html", auto_open=True)


def use_bus(df):
    frequency_counts = df.group_by("Bus frequency").agg(pl.count(
        'Bus frequency').alias('count')).collect()

    # Extract data for plotting
    frequency = frequency_counts['Bus frequency'].to_list()
    counts = frequency_counts['count'].to_list()

    # Desired order of the legend items
    desired_order = [
        "0 times",
        "1–2 times",
        "3–4 times",
        "5–6 times",
        "7 or more times"
    ]

    # Ensure the desired order is respected
    ordered_indices = [frequency.index(item) for item in desired_order if item in frequency]
    ordered_frequency = [frequency[i] for i in ordered_indices]
    ordered_counts = [counts[i] for i in ordered_indices]

    # Create the pie chart
    fig = go.Figure(data=[
        go.Pie(labels=ordered_frequency, values=ordered_counts, hole=0.0,
               pull=[0] * len(ordered_frequency), sort=False)])

    # Update layout
    fig.update_layout(
        legend_title_text='Bus usage frequency (in weeks)',
        legend=dict(itemsizing='constant', font=dict(size=12))
    )

    # Save the figure in different formats
    fig.write_image("plots/bus_use.eps")
    fig.write_image("plots/bus_use.png", width=1600, height=900, scale=3)

    # Save plot as HTML
    pio.write_html(fig, file="plots/bus_use.html", auto_open=True)


def viewing_assistance(df):
    frequency_counts = df.group_by("Assistance feature valuable?").agg(pl.count(
        'Assistance feature valuable?').alias('count')).collect()

    # Extract data for plotting
    frequency = frequency_counts['Assistance feature valuable?'].to_list()
    counts = frequency_counts['count'].to_list()

    # Desired order of the legend items
    desired_order = [
        "Strongly disagree",
        "Disagree",
        "Neither disagree nor agree",
        "Agree",
        "Strongly agree"
    ]

    # Ensure the desired order is respected and include zero counts for missing items
    ordered_frequency = []
    ordered_counts = []
    for item in desired_order:
        if item in frequency:
            index = frequency.index(item)
            ordered_frequency.append(frequency[index])
            ordered_counts.append(counts[index])
        else:
            ordered_frequency.append(item)
            ordered_counts.append(0)

    # Create the pie chart
    fig = go.Figure(data=[
        go.Pie(
            labels=ordered_frequency,
            values=ordered_counts,
            hole=0.0,
            pull=[0] * len(ordered_frequency),
            sort=False,
            textinfo='percent',
            insidetextorientation='horizontal',
            hoverinfo='label+percent'
        )
    ])

    # Update layout
    fig.update_layout(
        legend_title_text='Viewing assistance necessity',
        legend=dict(itemsizing='constant', font=dict(size=12))
    )

    # Customizing the text to hide 0% labels
    fig.update_traces(texttemplate=[
        f'{percent:.2f}%' if percent > 0 else ''
        for label, percent in zip(ordered_frequency, [c / sum(ordered_counts) * 100 for c in ordered_counts])
    ])

    # Save the figure in different formats
    fig.write_image("plots/viewing_assistance.eps")
    fig.write_image("plots/viewing_assistance.png", width=1600, height=900, scale=3)

    # Save plot as HTML
    pio.write_html(fig, file="plots/viewing_assistance.html", auto_open=True)


def NFC(df):
    frequency_counts = df.group_by("NFC feature valuable").agg(pl.count(
        'NFC feature valuable').alias('count')).collect()

    # Extract data for plotting
    frequency = frequency_counts['NFC feature valuable'].to_list()
    counts = frequency_counts['count'].to_list()

    # Desired order of the legend items
    desired_order = [
        "Strongly disagree",
        "Disagree",
        "Neither disagree nor agree",
        "Agree",
        "Strongly agree"
    ]

    # Ensure the desired order is respected and include zero counts for missing items
    ordered_frequency = []
    ordered_counts = []
    for item in desired_order:
        if item in frequency:
            index = frequency.index(item)
            ordered_frequency.append(frequency[index])
            ordered_counts.append(counts[index])
        else:
            ordered_frequency.append(item)
            ordered_counts.append(0)

    # Create the pie chart
    fig = go.Figure(data=[
        go.Pie(
            labels=ordered_frequency,
            values=ordered_counts,
            hole=0.0,
            pull=[0] * len(ordered_frequency),
            sort=False,
            textinfo='percent',
            insidetextorientation='horizontal',
            hoverinfo='label+percent'
        )
    ])

    # Update layout
    fig.update_layout(
        legend_title_text='NFC necessity',
        legend=dict(itemsizing='constant', font=dict(size=12))
    )

    # Customizing the text to hide 0% labels
    fig.update_traces(texttemplate=[
        f'{percent:.2f}%' if percent > 0 else ''
        for label, percent in zip(ordered_frequency, [c / sum(ordered_counts) * 100 for c in ordered_counts])
    ])

    # Save the figure in different formats
    fig.write_image("plots/NFC.eps")
    fig.write_image("plots/NFC.png", width=1600, height=900, scale=3)

    # Save plot as HTML
    pio.write_html(fig, file="plots/NFC.html", auto_open=True)


def info_preboarding(df):
    # Extract and process data from both columns
    column_10_data = df.select('Information required preboarding (mobile screen)').collect().to_series()
    column_11_data = df.select('Information required preboarding (public screen)').collect().to_series()

    percentages_10, counts_10 = process_column(column_10_data)
    percentages_11, counts_11 = process_column(column_11_data)

    # Get a sorted list of unique options from both columns
    unique_options = sorted(set(percentages_10.keys()).union(set(percentages_11.keys())))

    # Capitalize the first letter of each option
    unique_options = [option.capitalize() for option in unique_options]

    # Create lists for plotting
    values_10 = [percentages_10.get(option.lower(), 0) for option in unique_options]
    values_11 = [percentages_11.get(option.lower(), 0) for option in unique_options]

    counts_values_10 = [counts_10.get(option.lower(), 0) for option in unique_options]
    counts_values_11 = [counts_11.get(option.lower(), 0) for option in unique_options]

    # Define bar width
    bar_width = 0.3
    index = np.arange(len(unique_options))

    # Create the horizontal bar plot
    fig = go.Figure()

    fig.add_trace(go.Bar(y=index, x=values_10, orientation='h', name='Mobile screen',
                         marker_color='lightgreen'))

    fig.add_trace(go.Bar(y=index + bar_width, x=values_11, orientation='h', name='Public screen',
                         marker_color='skyblue'))

    # Update layout
    fig.update_layout(
        xaxis=dict(
            title='Percentage of participants choosing each option',
            title_font=dict(size=22),  # Increase x-axis title font size
            tickfont=dict(size=24)  # Increase x-axis label font size
        ),
        yaxis=dict(
            tickmode='array',
            tickvals=index + bar_width / 2,
            ticktext=unique_options,
            tickfont=dict(size=20)  # Increase y-axis label font size
        ),
        barmode='group',
        legend_title_text='Screen type',
        legend=dict(x=0.84, y=0.04, font=dict(size=18))  # Increase legend font size
    )

    # Add annotations for each bar to change the font size of the text
    annotations = []
    for i in range(len(values_10)):
        annotations.append(dict(
            x=values_10[i],
            y=index[i],
            text=str(counts_values_10[i]),
            font=dict(size=22),
            showarrow=False,
            xanchor='left'
        ))
    for i in range(len(values_11)):
        annotations.append(dict(
            x=values_11[i],
            y=index[i] + bar_width,
            text=str(counts_values_11[i]),
            font=dict(size=22),
            showarrow=False,
            xanchor='left'
        ))

    fig.update_layout(annotations=annotations)

    # Save the figure in different formats
    fig.write_image("plots/info_mobile_pre.eps")
    fig.write_image("plots/info_mobile_pre.png", width=1600, height=900, scale=3)

    # Save plot as HTML
    pio.write_html(fig, file="plots/info_mobile_pre.html", auto_open=True)


def info_onboarding(df):
    # Extract and process data from both columns
    column_10_data = df.select('Information required onboarding (public screen)').collect().to_series()
    column_11_data = df.select('Information required onboarding (private screen)').collect().to_series()
    column_12_data = df.select('Information required onboarding (mobile screen)').collect().to_series()

    # Process options
    percentages_10, counts_10 = process_column(column_10_data)
    percentages_11, counts_11 = process_column(column_11_data)
    percentages_12, counts_12 = process_column(column_12_data)

    # Get a sorted list of unique options from both columns
    unique_options = sorted(set(percentages_10.keys()).union(
        set(percentages_11.keys()).union(set(percentages_12.keys()))))

    # Capitalize the first letter of each option for y-axis labels
    unique_options_capitalized = [opt.capitalize() for opt in unique_options]

    # Replace 'safety information and protocols' with 'safety protocols'
    unique_options_capitalized = ['Safety protocols' if opt ==
                                  'Safety information and protocols and emergency call option' else
                                  opt for opt in unique_options_capitalized]

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

    # Create the horizontal bar plot
    fig = go.Figure()

    fig.add_trace(go.Bar(y=index, x=values_10, orientation='h', name='Public screen',
                         marker_color='skyblue'))

    fig.add_trace(go.Bar(y=index + bar_width, x=values_11, orientation='h', name='Private screen',
                         marker_color='salmon'))

    fig.add_trace(go.Bar(y=index + 2 * bar_width, x=values_12, orientation='h', name='Mobile screen',
                         marker_color='lightgreen'))

    # Update layout
    fig.update_layout(
        xaxis=dict(
            title='Percentage of participants choosing each option',
            title_font=dict(size=22),  # Increase x-axis title font size
            tickfont=dict(size=24)  # Increase x-axis label font size
        ),
        yaxis=dict(tickmode='array',
                   tickvals=index + bar_width,
                   ticktext=unique_options_capitalized,
                   tickfont=dict(size=20)  # Increase y-axis label font size
                   ),
        barmode='group',
        legend_title_text='Screen type',
        legend=dict(x=0.84, y=0.04, font=dict(size=18))  # Increase legend font size
    )

    # Add annotations for each bar to change the font size of the text
    annotations = []
    for i in range(len(values_10)):
        annotations.append(dict(
            x=values_10[i] + 1,  # Shift the text to the right of the bar
            y=index[i],
            text=str(counts_values_10[i]),
            font=dict(size=22),
            showarrow=False,
            xanchor='left'
        ))
    for i in range(len(values_11)):
        annotations.append(dict(
            x=values_11[i] + 1,  # Shift the text to the right of the bar
            y=index[i] + bar_width,
            text=str(counts_values_11[i]),
            font=dict(size=22),
            showarrow=False,
            xanchor='left'
        ))
    for i in range(len(values_12)):
        annotations.append(dict(
            x=values_12[i] + 1,  # Shift the text to the right of the bar
            y=index[i] + (2 * bar_width),
            text=str(counts_values_12[i]),
            font=dict(size=22),
            showarrow=False,
            xanchor='left'
        ))

    fig.update_layout(annotations=annotations)

    # Save the figure in different formats
    fig.write_image("plots/info_onboard.eps")
    fig.write_image("plots/info_onboard.png", width=1600, height=900, scale=3)  # Add width, height, and scale

    # Save plot as HTML
    pio.write_html(fig, file="plots/info_onboard.html", auto_open=True)


def create_combined_correlation_matrix(df):
    columns = [
        'Information required preboarding (mobile screen)',
        'Information required preboarding (public screen)',
        'Information required onboarding (public screen)',
        'Information required onboarding (private screen)',
        'Information required onboarding (mobile screen)'
    ]

    # Mapping of long column names to shorter labels
    col_mapping = {
        'Information required preboarding (mobile screen)': 'Pre-Mob',
        'Information required preboarding (public screen)': 'Pre-Pub',
        'Information required onboarding (public screen)': 'On-Pub',
        'Information required onboarding (private screen)': 'On-Pvt',
        'Information required onboarding (mobile screen)': 'On-Mob'
    }

    all_binary_matrices = []
    all_column_labels = []

    for col in columns:
        column_data = df.select(col).collect().to_series()
        options = process_options(column_data)
        mlb = MultiLabelBinarizer()
        binary_matrix = pd.DataFrame(mlb.fit_transform(options), columns=[f"{col}: {opt}" for opt in mlb.classes_],
                                     dtype=int)
        all_binary_matrices.append(binary_matrix)
        all_column_labels.extend(binary_matrix.columns)

    # Combine all binary matrices
    combined_matrix = pd.concat(all_binary_matrices, axis=1)
    combined_matrix = combined_matrix.loc[:, ~combined_matrix.columns.duplicated()]

    # Calculate pairwise correlation
    correlation_matrix = combined_matrix.corr()

    # Shorten the labels for better readability
    shortened_labels = [shorten_label(label, col_mapping) for label in correlation_matrix.columns]

    # Create the correlation matrix heatmap
    fig = px.imshow(correlation_matrix,
                    labels=dict(color="Correlation"),
                    x=shortened_labels,
                    y=shortened_labels,
                    color_continuous_scale='RdBu_r',
                    zmin=-1, zmax=1,
                    text_auto='.4f')

    # Update layout for better readability
    fig.update_layout(
        # title='Combined Correlation Matrix of Information Required Preboarding and Onboarding',
        autosize=False,
        width=1500,
        height=1000,
        margin=dict(l=160, r=160, t=160, b=160),
        xaxis=dict(tickangle=45, tickfont=dict(size=8)),  # Reduce the font size of x-axis labels
        yaxis=dict(tickfont=dict(size=8))  # Reduce the font size of y-axis labels
    )
    # Save the figure in different formats
    fig.write_image("plots/combined_correlation_matrix.eps")
    fig.write_image("plots/combined_correlation_matrix.png", width=1600, height=900, scale=3)

    # Show the plot
    fig.show()

    # Save plot as HTML
    fig.write_html("plots/combined_correlation_matrix.html", auto_open=False)


def create_combined_correlation_matrix_triangle(df):
    columns = [
        'Information required preboarding (mobile screen)',
        'Information required preboarding (public screen)',
        'Information required onboarding (public screen)',
        'Information required onboarding (private screen)',
        'Information required onboarding (mobile screen)'
    ]

    # Mapping of long column names to shorter labels
    col_mapping = {
        'Information required preboarding (mobile screen)': 'Pre-Mob',
        'Information required preboarding (public screen)': 'Pre-Pub',
        'Information required onboarding (public screen)': 'On-Pub',
        'Information required onboarding (private screen)': 'On-Pvt',
        'Information required onboarding (mobile screen)': 'On-Mob'
    }

    all_binary_matrices = []
    all_column_labels = []

    for col in columns:
        column_data = df.select(col).collect().to_series()
        options = process_options(column_data)
        mlb = MultiLabelBinarizer()
        binary_matrix = pd.DataFrame(mlb.fit_transform(options), columns=[f"{col}: {opt}" for opt in mlb.classes_],
                                     dtype=int)
        all_binary_matrices.append(binary_matrix)
        all_column_labels.extend(binary_matrix.columns)

    # Combine all binary matrices
    combined_matrix = pd.concat(all_binary_matrices, axis=1)
    combined_matrix = combined_matrix.loc[:, ~combined_matrix.columns.duplicated()]

    # Calculate pairwise correlation
    correlation_matrix = combined_matrix.corr()

    # Shorten the labels for better readability
    shortened_labels = [shorten_label(label, col_mapping) for label in correlation_matrix.columns]
    correlation_matrix.columns = shortened_labels
    correlation_matrix.index = shortened_labels

    # Mask the upper triangle
    mask = np.triu(np.ones_like(correlation_matrix, dtype=bool))

    # Create the correlation matrix heatmap using seaborn
    plt.figure(figsize=(16, 12))
    sns.heatmap(correlation_matrix, mask=mask, annot=True, fmt=".2f", annot_kws={"size": 6}, cmap='RdBu_r',
                vmin=-1, vmax=1, linewidths=.5, cbar_kws={"shrink": .5})

    # plt.title('Lower Triangular Correlation Matrix of Information Required Preboarding and Onboarding', size=15)
    plt.xticks(rotation=45, ha='right', fontsize=8)
    plt.yticks(fontsize=8)
    plt.tight_layout()

    # Save the figure
    plt.savefig("plots/combined_correlation_matrix_lower_triangle.png", dpi=300)
    plt.savefig("plots/combined_correlation_matrix_lower_triangle.eps")

    plt.show()


def create_combined_correlation_matrix_triangle_plotly(df):
    columns = [
        'Information required preboarding (mobile screen)',
        'Information required preboarding (public screen)',
        'Information required onboarding (public screen)',
        'Information required onboarding (private screen)',
        'Information required onboarding (mobile screen)'
    ]

    # Mapping of long column names to shorter labels
    col_mapping = {
        'Information required preboarding (mobile screen)': 'Pre-Mob',
        'Information required preboarding (public screen)': 'Pre-Pub',
        'Information required onboarding (public screen)': 'On-Pub',
        'Information required onboarding (private screen)': 'On-Pvt',
        'Information required onboarding (mobile screen)': 'On-Mob'
    }

    all_binary_matrices = []
    all_column_labels = []

    for col in columns:
        column_data = df.select(col).collect().to_series()
        options = process_options(column_data)
        mlb = MultiLabelBinarizer()
        binary_matrix = pd.DataFrame(mlb.fit_transform(options), columns=[f"{col}: {opt}" for opt in mlb.classes_],
                                     dtype=int)
        all_binary_matrices.append(binary_matrix)
        all_column_labels.extend(binary_matrix.columns)

    # Combine all binary matrices
    combined_matrix = pd.concat(all_binary_matrices, axis=1)
    combined_matrix = combined_matrix.loc[:, ~combined_matrix.columns.duplicated()]

    # Calculate pairwise correlation
    correlation_matrix = combined_matrix.corr()

    # Shorten the labels for better readability
    shortened_labels = [shorten_label(label, col_mapping) for label in correlation_matrix.columns]

    # Mask the upper triangle
    mask = np.triu(np.ones_like(correlation_matrix, dtype=bool))

    # Apply the mask to the correlation matrix
    correlation_matrix_masked = correlation_matrix.mask(mask)

    # Create the correlation matrix heatmap
    fig = px.imshow(correlation_matrix_masked,
                    labels=dict(color="Correlation"),
                    x=shortened_labels,
                    y=shortened_labels,
                    color_continuous_scale='RdBu_r',
                    zmin=-1, zmax=1,
                    text_auto='.4f')

    # Update layout for better readability
    fig.update_layout(
        # title='Lower Triangular Correlation Matrix of Information Required Preboarding and Onboarding',
        autosize=False,
        width=1500,
        height=1000,
        margin=dict(l=160, r=160, t=160, b=160),
        xaxis=dict(tickangle=45, tickfont=dict(size=8)),  # Reduce the font size of x-axis labels
        yaxis=dict(tickfont=dict(size=8))  # Reduce the font size of y-axis labels
    )
    # Save the figure in different formats
    fig.write_image("plots/combined_correlation_matrix_lower_triangle_plotly.eps")
    fig.write_image("plots/combined_correlation_matrix_lower_triangle_plotly.png", width=1600, height=900, scale=3)

    # Show the plot
    fig.show()

    # Save plot as HTML
    fig.write_html("plots/combined_correlation_matrix_lower_triangle_plotly.html", auto_open=False)


def pre_and_on_mobile_and_pre_public(df):
    preboarding_mobile_column = 'Information required preboarding (mobile screen)'
    preboarding_public_column = 'Information required preboarding (public screen)'
    onboarding_mobile_column = 'Information required onboarding (mobile screen)'

    columns = [
        preboarding_mobile_column,
        preboarding_public_column,
        onboarding_mobile_column
    ]

    # Mapping of long column names to shorter labels
    col_mapping = {
        'Information required preboarding (mobile screen)': 'Pre-Mob',
        'Information required preboarding (public screen)': 'Pre-Pub',
        'Information required onboarding (mobile screen)': 'On-Mob'
    }

    mlb = MultiLabelBinarizer()

    # Process columns
    binary_matrices = {}
    for col in columns:
        column_data = df.select(col).collect().to_series()
        options = process_options(column_data)
        binary_matrix = pd.DataFrame(mlb.fit_transform(options), columns=[f"{col}: {opt}" for opt in mlb.classes_],
                                     dtype=int)
        binary_matrices[col] = binary_matrix

    # Get binary matrices for specific columns
    binary_preboarding_mobile = binary_matrices[preboarding_mobile_column]
    binary_preboarding_public = binary_matrices[preboarding_public_column]
    binary_onboarding_mobile = binary_matrices[onboarding_mobile_column]

    # Combine the necessary matrices
    combined_matrix = pd.concat([binary_preboarding_mobile, binary_preboarding_public, binary_onboarding_mobile],
                                axis=1)
    combined_matrix = combined_matrix.loc[:, ~combined_matrix.columns.duplicated()]

    # Calculate pairwise correlation
    correlation_matrix = combined_matrix.corr()

    # Shorten the labels for better readability
    y_labels = [shorten_label(label, col_mapping) for label in binary_preboarding_mobile.columns]
    x_labels = [shorten_label(label, col_mapping) for label in list(binary_preboarding_public.columns)
                + list(binary_onboarding_mobile.columns)]

    # Make sure to rename the correlation matrix columns and index for proper indexing
    correlation_matrix.columns = [shorten_label(label, col_mapping) for label in correlation_matrix.columns]
    correlation_matrix.index = [shorten_label(label, col_mapping) for label in correlation_matrix.index]

    heatmap_data = correlation_matrix.loc[y_labels, x_labels]

    # Create the heatmap using Plotly
    fig = go.Figure(data=go.Heatmap(
        z=heatmap_data.values,
        x=heatmap_data.columns,
        y=heatmap_data.index,
        colorscale='RdBu_r',
        zmin=-1, zmax=1,
        text=heatmap_data.values,
        hovertemplate='%{y} - %{x}: %{z:.2f}<extra></extra>',
        showscale=True
    ))

    fig.update_layout(
        xaxis=dict(
            tickangle=45,
            tickfont=dict(size=14),  # Increase x-axis tick label font size
        ),
        yaxis=dict(
            tickfont=dict(size=14),  # Increase y-axis tick label font size
        ),
        autosize=False,
        width=1500,
        height=1000,
        margin=dict(l=160, r=160, t=160, b=160),
    )

    # Add text annotations
    for i in range(len(heatmap_data.index)):
        for j in range(len(heatmap_data.columns)):
            fig.add_annotation(
                x=heatmap_data.columns[j],
                y=heatmap_data.index[i],
                text=f"{heatmap_data.values[i, j]:.2f}",
                showarrow=False,
                font=dict(size=10)  # Increase text size in the cell
            )

    # Save the figure as an HTML file
    fig.write_html("plots/pre_and_on_mobile_and_pre_public.html")

    # Save the figure in different formats
    fig.write_image("plots/pre_and_on_mobile_and_pre_public.png", width=1600, height=900, scale=3)
    fig.write_image("plots/pre_and_on_mobile_and_pre_public.eps")

    # Show the plot
    fig.show()


def new_merged_pie_plot(df):
    # Create a 1x4 subplot figure with domain type for pie charts
    fig = make_subplots(rows=1, cols=4,
                        specs=[[{'type': 'domain'}, {'type': 'domain'}, {'type': 'domain'}, {'type': 'domain'}]])

    # Micro-mobility usage
    frequency_counts = df.group_by("Micro-mobillity frequency").agg(pl.count(
        'Micro-mobillity frequency').alias('count')).collect()
    frequency = frequency_counts['Micro-mobillity frequency'].to_list()
    counts = frequency_counts['count'].to_list()
    desired_order = ["Everyday", "4 to 6 days a week", "1 to 3 days a week",
                     "Once a month to once a week", "Less than once a month", "Never"]
    ordered_indices = [frequency.index(item) for item in desired_order if item in frequency]
    ordered_frequency = [frequency[i] for i in ordered_indices]
    ordered_counts = [counts[i] for i in ordered_indices]
    fig.add_trace(go.Pie(labels=ordered_frequency, values=ordered_counts, hole=0.0, pull=[0] * len(ordered_frequency),
                         sort=False, textinfo='label+percent', textfont=dict(size=10)), row=1, col=1)

    # Bus usage
    frequency_counts = df.group_by("Bus frequency").agg(pl.count('Bus frequency').alias('count')).collect()
    frequency = frequency_counts['Bus frequency'].to_list()
    counts = frequency_counts['count'].to_list()
    desired_order = ["0 times", "1–2 times", "3–4 times", "5–6 times", "7 or more times"]
    ordered_indices = [frequency.index(item) for item in desired_order if item in frequency]
    ordered_frequency = [frequency[i] for i in ordered_indices]
    ordered_counts = [counts[i] for i in ordered_indices]
    # Append "in a week" to each label
    ordered_frequency = [label + " in a week" for label in ordered_frequency]
    fig.add_trace(go.Pie(labels=ordered_frequency, values=ordered_counts, hole=0.0, pull=[0] * len(ordered_frequency),
                         sort=False, textinfo='label+percent', textfont=dict(size=10)), row=1, col=2)

    # Viewing assistance necessity
    frequency_counts = df.group_by("Assistance feature valuable?").agg(pl.count(
        'Assistance feature valuable?').alias('count')).collect()
    frequency = frequency_counts['Assistance feature valuable?'].to_list()
    counts = frequency_counts['count'].to_list()
    desired_order = ["Strongly disagree", "Disagree", "Neither disagree nor agree", "Agree", "Strongly agree"]
    ordered_indices = [frequency.index(item) for item in desired_order if item in frequency]
    ordered_frequency = [frequency[i] for i in ordered_indices]
    ordered_counts = [counts[i] for i in ordered_indices]
    fig.add_trace(go.Pie(labels=ordered_frequency, values=ordered_counts, hole=0.0, pull=[0] * len(ordered_frequency),
                         sort=False, textinfo='label+percent', textfont=dict(size=10)), row=1, col=3)

    # NFC necessity
    frequency_counts = df.group_by("NFC feature valuable").agg(pl.count(
        'NFC feature valuable').alias('count')).collect()
    frequency = frequency_counts['NFC feature valuable'].to_list()
    counts = frequency_counts['count'].to_list()
    desired_order = ["Strongly disagree", "Disagree", "Neither disagree nor agree", "Agree", "Strongly agree"]
    ordered_indices = [frequency.index(item) for item in desired_order if item in frequency]
    ordered_frequency = [frequency[i] for i in ordered_indices]
    ordered_counts = [counts[i] for i in ordered_indices]
    fig.add_trace(go.Pie(labels=ordered_frequency, values=ordered_counts, hole=0.0, pull=[0] * len(ordered_frequency),
                         sort=False, textinfo='label+percent', textfont=dict(size=10)), row=1, col=4)

    # Update layout for the entire figure and add annotations for centered subplot titles
    fig.update_layout(
        showlegend=False,  # Hide the legend for all subplots
        annotations=[
            dict(text="Micro-Mobility Usage", x=0.065, y=0.5, xref='paper',
                 yref='paper', showarrow=False, font=dict(size=12)),
            dict(text="Bus Usage", x=0.375, y=0.5, xref='paper',
                 yref='paper', showarrow=False, font=dict(size=12)),
            dict(text="Viewing Assistance", x=0.625, y=0.5, xref='paper',
                 yref='paper', showarrow=False, font=dict(size=12)),
            dict(text="NFC Necessity", x=0.92, y=0.5, xref='paper',
                 yref='paper', showarrow=False, font=dict(size=12))
        ]
    )

    # Save the figure in different formats
    fig.write_image("plots/merged_pie_plots.eps")
    fig.write_image("plots/merged_pie_plots.png", width=1600, height=400, scale=3)

    # Save plot as HTML
    pio.write_html(fig, file="plots/merged_pie_plots.html", auto_open=True)


# Execute analysis
if __name__ == "__main__":

    # Create directory if it doesn't exist
    output_folder = "plots"
    os.makedirs(output_folder, exist_ok=True)

    logger.info("Analysis started.")
    common.get_configs('data')

    # Read the CSV file into a Polars LazyFrame
    dataframe = pl.scan_csv(common.get_configs('data'))

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

    gender_distribution_bar(dataframe)
    gender_distribution_pie(dataframe)
    age_distribution(dataframe)
    demographic_distribution_bar(dataframe)
    demographic_distribution_pie(dataframe)
    use_micro_mobility(dataframe)
    use_bus(dataframe)
    viewing_assistance(dataframe)
    NFC(dataframe)
    info_preboarding(dataframe)
    info_onboarding(dataframe)
    create_combined_correlation_matrix(dataframe)
    create_combined_correlation_matrix_triangle(dataframe)
    create_combined_correlation_matrix_triangle_plotly(dataframe)
    pre_and_on_mobile_and_pre_public(dataframe)
    new_merged_pie_plot(dataframe)

    logger.info("Analysis completed.")
