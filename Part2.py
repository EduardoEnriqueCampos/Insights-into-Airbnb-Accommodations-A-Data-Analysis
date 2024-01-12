import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import warnings

def read_data(file_path):
    return pd.read_csv(file_path)

def preprocess_data(data):
    data['city'] = data['city'].str.title()
    data.loc[data['country'] == 'Turkey', 'city'] = 'Istanbul'
    return data

def display_country_menu(data):
    filtered_countries = data['country'].loc[(data['country'].str.len() >= 3) & (data['country'] != 'Not Specified')].unique()

    for i, country in enumerate(filtered_countries, start=1):
        print(f"{i}. {country}")

    print(f"{len(filtered_countries) + 1}. I don't have an idea where to go. Please recommend countries with the highest satisfaction scores.")
    print(" ")

    while True:
        try:
            option1 = int(input("Please enter the number corresponding to the option for which you would like more information: "))

            if 1 <= option1 <= len(filtered_countries) + 1:
                if option1 == 56:
                    plot_top_countries(data)
                else:
                    explore_country(data, filtered_countries[option1 - 1])
                break
            else:
                print("Error: The option is not valid. Please check the option menu.")
        except ValueError:
            print("Error: Please enter a valid number.")

def plot_top_countries(data):
    filtered_df = data[data['country'].ne('Not Specified')]
    counts = filtered_df[filtered_df['Rating_Scale'].isin(['Very Satisfied', 'Satisfied'])].groupby('country').size()
    top_countries = counts.nlargest(5)

    fig, ax = plt.subplots(figsize=(8, 8))
    explode = [0.1, 0.3, 0.5, 0.7, 0]

    patches, texts, autotexts = ax.pie(top_countries, autopct='%1.1f%%', pctdistance=1.1, explode=explode, labeldistance=1.1, startangle=140, colors=sns.color_palette("pastel"), textprops=dict(size=14))
    plt.title('Top 5 Countries with the Highest Satisfaction Scores in Airbnb', fontsize=16)
    legend_labels = [f"{label} ({count})" for label, count in zip(top_countries.index, top_countries)]
    plt.legend(patches, legend_labels, loc="center left", bbox_to_anchor=(1, 0.5), title="Rating Scale Per Country", title_fontsize="12", fontsize=10)
    plt.show()

def explore_country(data, country_selection):
    print(" ")
    print(f"Country:{country_selection}")
    print("Search Recommendations for the Selected Country:\n 1. Explore accommodations based on cities and pricing scale with the highest rating.\n 2. Discover optimal single-person accommodations featuring 1 private room with a minimum stay of 7 nights, and the highest customer satisfaction scores.\n 3. Find entire homes or apartments suitable for families with more than 2 bedrooms, available for instant booking.\n 4. Connect with hosts with the most extensive portfolio of listings.")
    print(" ")

    while True:
        try:
            option2 = int(input("Enter the number corresponding to one of the displayed options: "))
            if 1 <= option2 <= 4:
                explore_option(data, country_selection, option2)
                break
            else:
                print("Error: The option is not valid. Please check the option menu.")
        except ValueError:
            print("Error: Please enter a valid number.")

def explore_option(data, country_selection, option2):
    if option2 == 1:
        plot_pricing_scale_per_city(data, country_selection)
    elif option2 == 2:
        plot_top_private_rooms(data, country_selection)
    elif option2 == 3:
        plot_top_family_rooms(data, country_selection)
    elif option2 == 4:
        plot_top_hosts(data, country_selection)

def plot_pricing_scale_per_city(data, country_selection):
    city_review_means = data[data['country'] == country_selection].groupby('city')['review_scores_value'].mean()
    top_cities = city_review_means.sort_values(ascending=False).head(50)
    ax = pd.crosstab(data[(data['country'] == country_selection) & (data['city'].isin(top_cities.index))]['city'],
                     data[(data['country'] == country_selection) & (data['city'].isin(top_cities.index))]['Scale_Price'],
                     normalize='index').plot(kind='bar', stacked=True, color=sns.color_palette("pastel"), figsize=(15, 5),
                                             title= f'Pricing Scale Per City in {country_selection} (Top 50 Cities by Review Score)',
                                             xlabel='Cities', ylabel='Percentage', width=0.8)
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')
    plt.tight_layout()
    plt.show()

def plot_top_private_rooms(data, country_selection):
    filtered_df2 = data[(data['room_type'] == "Private room") & (data['minimum_nights'] >= 7) & (data['country'] == country_selection) & (data['review_scores_value'] > 3)]
    if not filtered_df2.empty:
        top_rooms = filtered_df2.nlargest(10, 'review_scores_value')
        plt.figure(figsize=(10, 6))
        ax = sns.barplot(x="id", y="review_scores_value", data=top_rooms, palette=sns.color_palette("pastel"))
        plt.xticks(rotation=90)
        plt.xlabel("Accommodations' ID")
        plt.ylabel("Review Score Value")
        plt.title("Discover the Top 10 Accommodations Offering Private Rooms, Minimum 7-Night Stays, and the Highest Score Values")
        plt.show()
    else:
        print(f"There are no available rooms with the specified conditions in {country_selection}.")

def plot_top_family_rooms(data, country_selection):
    filtered_df3 = data[(data['room_type'] == "Entire home/apt") & (data['bedrooms'] >= 2) & (data['country'] == country_selection) & (data['review_scores_location'] > 3) & (data['instant_bookable'] == "t")]
    if not filtered_df3.empty:
        top_family_rooms = filtered_df3.nlargest(10, 'review_scores_location')
        plt.figure(figsize=(10, 6))
        ax = sns.barplot(x="id", y="review_scores_location", data=top_family_rooms, palette=sns.color_palette("pastel"))
        plt.xticks(rotation=90)
        plt.xlabel("Accommodations' ID")
        plt.ylabel("Review Location Score Value")
        plt.title("Discover the Top 10 Accommodations for Families with more than 2 bedrooms, available for instant booking, and Highest Location Score Values ")
        plt.show()
    else:
        print(f"There are no available rooms with the specified conditions in {country_selection}.")

def plot_top_hosts(data, country_selection):
    filtered_df4 = data[data['country'] == country_selection]
    host_listings_count = filtered_df4.groupby('host_id')['calculated_host_listings_count'].sum()
    top_hosts = host_listings_count.nlargest(5)
    fig, ax = plt.subplots(figsize=(8, 8))
    explode = [0.1, 0.1, 0.1, 0.1, 0.1]
    patches, texts, autotexts = ax.pie(top_hosts, autopct='%1.1f%%', pctdistance=1.1, explode=explode, labeldistance=1.1, startangle=140, colors=sns.color_palette("pastel"), textprops=dict(size=14))
    plt.title(f'Top 5 Host with the most extensive portfolio of listings in {country_selection}.', fontsize=16)
    legend_labels = [f"{label} ({count})" for label, count in zip(top_hosts.index, top_hosts)]
    plt.legend(patches, legend_labels, loc="center left", bbox_to_anchor=(1, 0.5), title="Host Rates", title_fontsize="12", fontsize=10)
    plt.show()

if __name__ == "__main__":
    warnings.simplefilter(action='ignore', category=FutureWarning)
    warnings.filterwarnings("ignore", message="The palette list has more values")

    df = read_data("airbnb_listings_modified.csv")
    df = preprocess_data(df)

    while True:
        display_country_menu(df)
        user_input = input("Do you want to continue? (yes/no): ").lower()
        if user_input != 'yes':
            print("Exiting the program. Goodbye!")
            break
