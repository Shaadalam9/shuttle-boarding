# Code by md_shadab_alam@outlook.com

import polars as pl
import numpy as np
import plotly.graph_objects as go
import plotly.io as pio
import plotly.express as px
import pandas as pd
from sklearn.preprocessing import MultiLabelBinarizer


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
    options_list = series.apply(lambda x: [opt.strip().lower().capitalize() for opt in x.split(",")],
                                return_dtype=pl.List).to_list()

    # Define a mapping for longer option names to shorter versions
    option_mapping = {
        "Safety information and protocols and emergency call option": "Safety information",
    }

    # Apply the mapping
    options_list = [[option_mapping.get(opt, opt) for opt in sublist] for sublist in options_list]

    return options_list


def gender_distribution_bar(df):
    # Count the occurrences of each gender
    gender_counts = df.groupby('Gender').agg(pl.count('Gender').alias('count')).collect()

    # Extract data for plotting
    genders = gender_counts['Gender'].to_list()
    counts = gender_counts['count'].to_list()

    # Create the bar plot
    fig = go.Figure(data=[
        go.Bar(name='Gender', x=genders, y=counts, marker_color=['pink', 'blue'])
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
    gender_counts = df.groupby('Gender').agg(pl.count('Gender').alias('count')).collect()

    # Extract data for plotting
    genders = gender_counts['Gender'].to_list()
    counts = gender_counts['count'].to_list()

    # Create the pie chart
    fig = go.Figure(data=[
        go.Pie(labels=genders, values=counts, hole=0.0, marker=dict(colors=['pink', 'blue']))
    ])

    # Update layout
    fig.update_layout(
        # title='Gender Distribution',
        xaxis=dict(tickangle=0)
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

    # Create the pie chart
    fig = go.Figure(data=[
        go.Pie(labels=frequency, values=counts, hole=0.0, pull=[0, 0, 0, 0, 0, 0])])

    # Update layout
    fig.update_layout(
        # title='Use of Micro-mobility'
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

    # Create the pie chart
    fig = go.Figure(data=[
        go.Pie(labels=frequency, values=counts, hole=0.0, pull=[0, 0, 0, 0, 0])
    ])

    # Update layout
    fig.update_layout(
        # title='Use of public bus (per week)'
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

    # Create the pie chart
    fig = go.Figure(data=[
        go.Pie(labels=frequency, values=counts, hole=0.0, pull=[0, 0, 0, 0])
    ])

    # Update layout
    fig.update_layout(
        # title='The Role of Viewing Assistance in Enhancing Navigation and Overcoming Language Barriers'
    )

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

    # Create the pie chart
    fig = go.Figure(data=[
        go.Pie(labels=frequency, values=counts, hole=0.0, pull=[0, 0, 0, 0])
    ])

    # Update layout
    fig.update_layout(
        # title='The Role of NFC while boarding'
    )

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

    fig.add_trace(go.Bar(y=index, x=values_10, orientation='h', name='Mobile Screen',
                         marker_color='lightgreen', text=counts_values_10, textposition='outside'))

    fig.add_trace(go.Bar(y=index + bar_width, x=values_11, orientation='h', name='Public Screen',
                         marker_color='skyblue', text=counts_values_11, textposition='outside'))

    # Update layout
    fig.update_layout(
        # title='Information Required Preboarding',
        xaxis_title='Percentage',
        yaxis=dict(tickmode='array', tickvals=index + bar_width / 2, ticktext=unique_options),
        barmode='group',
        legend_title_text='Screen Type'
    )

    # Save the figure in different formats
    fig.write_image("plots/info_mobile_pre.eps")
    fig.write_image("plots/info_mobile_pre.png", width=1600, height=900, scale=3)

    # Save plot as HTML
    pio.write_html(fig, file="plots/info_preboard.html", auto_open=True)


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

    # Capitalize the first letter of each option
    unique_options = [option.capitalize() for option in unique_options]

    # Create lists for plotting
    values_10 = [percentages_10.get(option.lower(), 0) for option in unique_options]
    values_11 = [percentages_11.get(option.lower(), 0) for option in unique_options]
    values_12 = [percentages_12.get(option.lower(), 0) for option in unique_options]

    counts_values_10 = [counts_10.get(option.lower(), 0) for option in unique_options]
    counts_values_11 = [counts_11.get(option.lower(), 0) for option in unique_options]
    counts_values_12 = [counts_12.get(option.lower(), 0) for option in unique_options]

    # Define bar width
    bar_width = 0.25  # Adjusted the bar width to fit three bars
    index = np.arange(len(unique_options))

    # Create the horizontal bar plot
    fig = go.Figure()

    fig.add_trace(go.Bar(y=index, x=values_10, orientation='h', name='Public Screen',
                         marker_color='skyblue', text=counts_values_10, textposition='outside'))

    fig.add_trace(go.Bar(y=index + bar_width, x=values_11, orientation='h', name='Private Screen',
                         marker_color='salmon', text=counts_values_11, textposition='outside'))

    fig.add_trace(go.Bar(y=index + 2 * bar_width, x=values_12, orientation='h', name='Mobile Screen',
                         marker_color='lightgreen', text=counts_values_12, textposition='outside'))

    # Update layout
    fig.update_layout(
        # title='Information Required Onboarding',
        xaxis_title='Percentage',
        yaxis=dict(tickmode='array', tickvals=index + bar_width, ticktext=unique_options),
        barmode='group',
        legend_title_text='Screen Type'
    )

    # Save the figure in different formats
    fig.write_image("plots/info_onboard.eps")
    fig.write_image("plots/info_onboard.png", width=1600, height=900, scale=3)

    # Save plot as HTML
    pio.write_html(fig, file="plots/info_onboard.html", auto_open=True)


def correlation_matrix_1(df):
    # Extract and process the relevant columns
    column_10_data = df.select('Information required preboarding (mobile screen)').collect().to_series()
    column_11_data = df.select('Information required preboarding (public screen)').collect().to_series()

    # Process columns to get lists of options
    options_10 = process_options(column_10_data)
    options_11 = process_options(column_11_data)

    # Create binary matrices for each column using MultiLabelBinarizer
    mlb = MultiLabelBinarizer()
    binary_matrix_10 = pd.DataFrame(mlb.fit_transform(options_10), columns=mlb.classes_, dtype=int)
    binary_matrix_11 = pd.DataFrame(mlb.fit_transform(options_11), columns=mlb.classes_, dtype=int)

    # Ensure both DataFrames have the same columns
    all_columns = sorted(set(binary_matrix_10.columns).union(set(binary_matrix_11.columns)))
    binary_matrix_10 = binary_matrix_10.reindex(columns=all_columns, fill_value=0)
    binary_matrix_11 = binary_matrix_11.reindex(columns=all_columns, fill_value=0)

    # Calculate the pairwise correlation between the two columns
    correlation_matrix = pd.DataFrame(index=binary_matrix_10.columns, columns=binary_matrix_11.columns)
    for col_10 in binary_matrix_10.columns:
        for col_11 in binary_matrix_11.columns:
            correlation_matrix.at[col_10, col_11] = binary_matrix_10[col_10].corr(binary_matrix_11[col_11])

    correlation_matrix = correlation_matrix.astype(float)

    # Create the correlation matrix heatmap
    fig = px.imshow(correlation_matrix,
                    labels=dict(x="Public Screen Options", y="Mobile Screen Options", color="Correlation"),
                    x=correlation_matrix.columns,
                    y=correlation_matrix.index,
                    color_continuous_scale='RdBu_r',
                    zmin=-1, zmax=1)

    # Update layout for better readability
    fig.update_layout(
        title='Correlation Matrix between Mobile and Public Screen Options before boarding on Shuttle bus',
        autosize=False,
        width=1500,
        height=1000,
        margin=dict(l=160, r=160, t=160, b=160),
        xaxis=dict(tickangle=90)  # Ensure the x-axis labels are vertical
    )
    # Save the figure in different formats
    fig.write_image("plots/correlation_matrix_1.eps")
    fig.write_image("plots/correlation_matrix_1.png", width=1600, height=900, scale=3)

    # Show the plot
    fig.show()

    # Save plot as HTML
    fig.write_html("plots/correlation_matrix_1.html", auto_open=False)


def correlation_matrix_2(df):
    # Extract and process the relevant columns
    column_10_data = df.select('Information required preboarding (mobile screen)').collect().to_series()
    column_11_data = df.select('Information required onboarding (mobile screen)').collect().to_series()

    # Process columns to get lists of options
    options_10 = process_options(column_10_data)
    options_11 = process_options(column_11_data)

    # Create binary matrices for each column using MultiLabelBinarizer
    mlb = MultiLabelBinarizer()
    binary_matrix_10 = pd.DataFrame(mlb.fit_transform(options_10),
                                    columns=[f"{col}" for col in mlb.classes_], dtype=int)
    binary_matrix_11 = pd.DataFrame(mlb.fit_transform(options_11),
                                    columns=[f"{col}" for col in mlb.classes_], dtype=int)

    # Calculate the pairwise correlation between the two columns
    correlation_matrix = pd.DataFrame(index=binary_matrix_10.columns, columns=binary_matrix_11.columns)
    for col_10 in binary_matrix_10.columns:
        for col_11 in binary_matrix_11.columns:
            correlation_matrix.at[col_10, col_11] = binary_matrix_10[col_10].corr(binary_matrix_11[col_11])

    correlation_matrix = correlation_matrix.astype(float)

    # Create the correlation matrix heatmap
    fig = px.imshow(correlation_matrix,
                    labels=dict(x="Mobile Screen Options (After Boarding)",
                                y="Mobile Screen Options (Before Boarding)", color="Correlation"),
                    color_continuous_scale='RdBu_r',
                    zmin=-1, zmax=1)

    # Update layout for better readability
    fig.update_layout(
        title='Correlation Matrix between Mobile Screen Options before and after boarding on Shuttle bus',
        autosize=False,
        width=1500,
        height=1000,
        margin=dict(l=160, r=160, t=160, b=160),
        xaxis=dict(tickangle=90)  # Ensure the x-axis labels are vertical
    )

    # Save the figure in different formats
    fig.write_image("plots/correlation_matrix_2.eps")
    fig.write_image("plots/correlation_matrix_2.png", width=1600, height=900, scale=3)

    # Show the plot
    fig.show()

    # Save plot as HTML
    fig.write_html("plots/correlation_matrix_2.html", auto_open=False)


def correlation_matrix_3(df):
    # Extract and process the relevant columns
    column_10_data = df.select('Information required preboarding (mobile screen)').collect().to_series()
    column_11_data = df.select('Information required onboarding (private screen)').collect().to_series()

    # Process columns to get lists of options
    options_10 = process_options(column_10_data)
    options_11 = process_options(column_11_data)

    # Create binary matrices for each column using MultiLabelBinarizer
    mlb = MultiLabelBinarizer()
    binary_matrix_10 = pd.DataFrame(mlb.fit_transform(options_10),
                                    columns=[f"{col}" for col in mlb.classes_], dtype=int)
    binary_matrix_11 = pd.DataFrame(mlb.fit_transform(options_11),
                                    columns=[f"{col}" for col in mlb.classes_], dtype=int)

    # Calculate the pairwise correlation between the two columns
    correlation_matrix = pd.DataFrame(index=binary_matrix_10.columns, columns=binary_matrix_11.columns)
    for col_10 in binary_matrix_10.columns:
        for col_11 in binary_matrix_11.columns:
            correlation_matrix.at[col_10, col_11] = binary_matrix_10[col_10].corr(binary_matrix_11[col_11])

    correlation_matrix = correlation_matrix.astype(float)

    # Create the correlation matrix heatmap
    fig = px.imshow(correlation_matrix,
                    labels=dict(x="Private Screen Options (After Boarding)",
                                y="Mobile Screen Options (Before Boarding)", color="Correlation"),
                    color_continuous_scale='RdBu_r',
                    zmin=-1, zmax=1)

    # Update layout for better readability
    fig.update_layout(
        title='Correlation Matrix between Mobile Screen Options before boarding on Shuttle bus and Private Screen Option after boarding on Shuttle bus',  # noqa:E501
        autosize=False,
        width=1500,
        height=1000,
        margin=dict(l=160, r=160, t=160, b=160),
        xaxis=dict(tickangle=90)  # Ensure the x-axis labels are vertical
    )

    # Save the figure in different formats
    fig.write_image("plots/correlation_matrix_3.eps")
    fig.write_image("plots/correlation_matrix_3.png", width=1600, height=900, scale=3)

    # Show the plot
    fig.show()

    # Save plot as HTML
    fig.write_html("plots/correlation_matrix_3.html", auto_open=False)


def correlation_matrix_4(df):
    # Extract and process the relevant columns
    column_10_data = df.select('Information required preboarding (mobile screen)').collect().to_series()
    column_11_data = df.select('Information required onboarding (public screen)').collect().to_series()

    # Process columns to get lists of options
    options_10 = process_options(column_10_data)
    options_11 = process_options(column_11_data)

    # Create binary matrices for each column using MultiLabelBinarizer
    mlb = MultiLabelBinarizer()
    binary_matrix_10 = pd.DataFrame(mlb.fit_transform(options_10),
                                    columns=[f"{col}" for col in mlb.classes_], dtype=int)
    binary_matrix_11 = pd.DataFrame(mlb.fit_transform(options_11),
                                    columns=[f"{col}" for col in mlb.classes_], dtype=int)

    # Calculate the pairwise correlation between the two columns
    correlation_matrix = pd.DataFrame(index=binary_matrix_10.columns, columns=binary_matrix_11.columns)
    for col_10 in binary_matrix_10.columns:
        for col_11 in binary_matrix_11.columns:
            correlation_matrix.at[col_10, col_11] = binary_matrix_10[col_10].corr(binary_matrix_11[col_11])

    correlation_matrix = correlation_matrix.astype(float)

    # Create the correlation matrix heatmap
    fig = px.imshow(correlation_matrix,
                    labels=dict(x="Public Screen Options (After Boarding)",
                                y="Mobile Screen Options (Before Boarding)", color="Correlation"),
                    color_continuous_scale='RdBu_r',
                    zmin=-1, zmax=1)

    # Update layout for better readability
    fig.update_layout(
        title='Correlation Matrix between Mobile Screen Options before boarding on Shuttle bus and Public Screen Option after boarding on Shuttle bus',  # noqa:E501
        autosize=False,
        width=1500,
        height=1000,
        margin=dict(l=160, r=160, t=160, b=160),
        xaxis=dict(tickangle=90)  # Ensure the x-axis labels are vertical
    )

    # Save the figure in different formats
    fig.write_image("plots/correlation_matrix_4.eps")
    fig.write_image("plots/correlation_matrix_4.png", width=1600, height=900, scale=3)

    # Show the plot
    fig.show()

    # Save plot as HTML
    fig.write_html("plots/correlation_matrix_4.html", auto_open=False)


def correlation_matrix_5(df):
    # Extract and process the relevant columns
    column_10_data = df.select('Information required preboarding (public screen)').collect().to_series()
    column_11_data = df.select('Information required onboarding (private screen)').collect().to_series()

    # Process columns to get lists of options
    options_10 = process_options(column_10_data)
    options_11 = process_options(column_11_data)

    # Create binary matrices for each column using MultiLabelBinarizer
    mlb = MultiLabelBinarizer()
    binary_matrix_10 = pd.DataFrame(mlb.fit_transform(options_10),
                                    columns=[f"{col}" for col in mlb.classes_], dtype=int)
    binary_matrix_11 = pd.DataFrame(mlb.fit_transform(options_11),
                                    columns=[f"{col}" for col in mlb.classes_], dtype=int)

    # Calculate the pairwise correlation between the two columns
    correlation_matrix = pd.DataFrame(index=binary_matrix_10.columns, columns=binary_matrix_11.columns)
    for col_10 in binary_matrix_10.columns:
        for col_11 in binary_matrix_11.columns:
            correlation_matrix.at[col_10, col_11] = binary_matrix_10[col_10].corr(binary_matrix_11[col_11])

    correlation_matrix = correlation_matrix.astype(float)

    # Create the correlation matrix heatmap
    fig = px.imshow(correlation_matrix,
                    labels=dict(x="Private Screen Options (After Boarding)",
                                y="Public Screen Options (Before Boarding)", color="Correlation"),
                    color_continuous_scale='RdBu_r',
                    zmin=-1, zmax=1)

    # Update layout for better readability
    fig.update_layout(
        title='Correlation Matrix between Public Screen Options before boarding on Shuttle bus and Private Screen Option after boarding on Shuttle bus',  # noqa:E501
        autosize=False,
        width=1500,
        height=1000,
        margin=dict(l=160, r=160, t=160, b=160),
        xaxis=dict(tickangle=90)  # Ensure the x-axis labels are vertical
    )

    # Save the figure in different formats
    fig.write_image("plots/correlation_matrix_5.eps")
    fig.write_image("plots/correlation_matrix_5.png", width=1600, height=900, scale=3)

    # Show the plot
    fig.show()

    # Save plot as HTML
    fig.write_html("plots/correlation_matrix_5.html", auto_open=False)


def correlation_matrix_6(df):
    # Extract and process the relevant columns
    column_10_data = df.select('Information required preboarding (public screen)').collect().to_series()
    column_11_data = df.select('Information required onboarding (public screen)').collect().to_series()

    # Process columns to get lists of options
    options_10 = process_options(column_10_data)
    options_11 = process_options(column_11_data)

    # Create binary matrices for each column using MultiLabelBinarizer
    mlb = MultiLabelBinarizer()
    binary_matrix_10 = pd.DataFrame(mlb.fit_transform(options_10),
                                    columns=[f"{col}" for col in mlb.classes_], dtype=int)
    binary_matrix_11 = pd.DataFrame(mlb.fit_transform(options_11),
                                    columns=[f"{col}" for col in mlb.classes_], dtype=int)

    # Calculate the pairwise correlation between the two columns
    correlation_matrix = pd.DataFrame(index=binary_matrix_10.columns, columns=binary_matrix_11.columns)
    for col_10 in binary_matrix_10.columns:
        for col_11 in binary_matrix_11.columns:
            correlation_matrix.at[col_10, col_11] = binary_matrix_10[col_10].corr(binary_matrix_11[col_11])

    correlation_matrix = correlation_matrix.astype(float)

    # Create the correlation matrix heatmap
    fig = px.imshow(correlation_matrix,
                    labels=dict(x="Public Screen Options (After Boarding)",
                                y="Public Screen Options (Before Boarding)", color="Correlation"),
                    color_continuous_scale='RdBu_r',
                    zmin=-1, zmax=1)

    # Update layout for better readability
    fig.update_layout(
        title='Correlation Matrix between Public Screen Options before and after boarding on Shuttle bus',  # noqa:E501
        autosize=False,
        width=1500,
        height=1000,
        margin=dict(l=160, r=160, t=160, b=160),
        xaxis=dict(tickangle=90)  # Ensure the x-axis labels are vertical
    )

    # Save the figure in different formats
    fig.write_image("plots/correlation_matrix_6.eps")
    fig.write_image("plots/correlation_matrix_6.png", width=1600, height=900, scale=3)

    # Show the plot
    fig.show()

    # Save plot as HTML
    fig.write_html("plots/correlation_matrix_6.html", auto_open=False)


def correlation_matrix_7(df):
    # Extract and process the relevant columns
    column_10_data = df.select('Information required preboarding (public screen)').collect().to_series()
    column_11_data = df.select('Information required onboarding (mobile screen)').collect().to_series()

    # Process columns to get lists of options
    options_10 = process_options(column_10_data)
    options_11 = process_options(column_11_data)

    # Create binary matrices for each column using MultiLabelBinarizer
    mlb = MultiLabelBinarizer()
    binary_matrix_10 = pd.DataFrame(mlb.fit_transform(options_10),
                                    columns=[f"{col}" for col in mlb.classes_], dtype=int)
    binary_matrix_11 = pd.DataFrame(mlb.fit_transform(options_11),
                                    columns=[f"{col}" for col in mlb.classes_], dtype=int)

    # Calculate the pairwise correlation between the two columns
    correlation_matrix = pd.DataFrame(index=binary_matrix_10.columns, columns=binary_matrix_11.columns)
    for col_10 in binary_matrix_10.columns:
        for col_11 in binary_matrix_11.columns:
            correlation_matrix.at[col_10, col_11] = binary_matrix_10[col_10].corr(binary_matrix_11[col_11])

    correlation_matrix = correlation_matrix.astype(float)

    # Create the correlation matrix heatmap
    fig = px.imshow(correlation_matrix,
                    labels=dict(x="Mobile Screen Options (After Boarding)",
                                y="Public Screen Options (Before Boarding)", color="Correlation"),
                    color_continuous_scale='RdBu_r',
                    zmin=-1, zmax=1)

    # Update layout for better readability
    fig.update_layout(
        title='Correlation Matrix between Public Screen Options before boarding on Shuttle bus and Mobile Screen Option after boarding on Shuttle bus',  # noqa:E501
        autosize=False,
        width=1500,
        height=1000,
        margin=dict(l=160, r=160, t=160, b=160),
        xaxis=dict(tickangle=90)  # Ensure the x-axis labels are vertical
    )

    # Save the figure in different formats
    fig.write_image("plots/correlation_matrix_7.eps")
    fig.write_image("plots/correlation_matrix_7.png", width=1600, height=900, scale=3)

    # Show the plot
    fig.show()

    # Save plot as HTML
    fig.write_html("plots/correlation_matrix_7.html", auto_open=False)


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
correlation_matrix_1(dataframe)
correlation_matrix_2(dataframe)
correlation_matrix_3(dataframe)
correlation_matrix_4(dataframe)
correlation_matrix_5(dataframe)
correlation_matrix_6(dataframe)
correlation_matrix_7(dataframe)

print("Execution Completed")
