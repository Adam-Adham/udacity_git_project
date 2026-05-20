import time
import pandas as pd
import numpy as np

CITY_DATA = {
    'chicago': 'chicago.csv',
    'new york city': 'new_york_city.csv',
    'washington': 'washington.csv'
}

MONTHS = ['all', 'january', 'february', 'march', 'april', 'may', 'june']
DAYS = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']


def get_filters():
    """
    Ask user to specify a city, month, and day to analyze.

    Returns:
        city: name of the city to analyze
        month: name of the month to filter by, or "all"
        day: name of the day to filter by, or "all"
    """
    print("Hello! Let's explore some US bikeshare data together!")

    while True:
        city = input("Choose a city: Chicago, New York City, or Washington:\n")
        city = city.lower().strip()

        if city in CITY_DATA:
            break
        else:
            print("Invalid city. Please enter Chicago, New York City, or Washington.")

    while True:
        month = input("Choose a month: all, January, February, March, April, May, or June:\n")
        month = month.lower().strip()

        if month in MONTHS:
            break
        else:
            print("Invalid month. Please enter all, January, February, March, April, May, or June.")

    while True:
        day = input("Choose a day: all, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or Sunday:\n")
        day = day.lower().strip()

        if day in DAYS:
            break
        else:
            print("Invalid day. Please enter a valid day of the week.")

    print('-' * 40)
    return city, month, day


def load_data(city, month, day):
    """
    Load data for the selected city and filter by month and day.

    Args:
        city: name of the city to analyze
        month: name of the month to filter by, or "all"
        day: name of the day to filter by, or "all"

    Returns:
        df: filtered DataFrame
    """
    df = pd.read_csv(CITY_DATA[city])

    df['Start Time'] = pd.to_datetime(df['Start Time'])

    df['month'] = df['Start Time'].dt.month_name().str.lower()
    df['day_of_week'] = df['Start Time'].dt.day_name().str.lower()
    df['hour'] = df['Start Time'].dt.hour

    if month != 'all':
        df = df[df['month'] == month]

    if day != 'all':
        df = df[df['day_of_week'] == day]

    return df


def time_stats(df):
    """Display statistics on the most frequent times of travel."""
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    print("Most common month:", df['month'].mode()[0])
    print("Most common day of week:", df['day_of_week'].mode()[0])
    print("Most common start hour:", df['hour'].mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def station_stats(df):
    """Display statistics on the most popular stations and trip."""
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    print("Most commonly used start station:", df['Start Station'].mode()[0])
    print("Most commonly used end station:", df['End Station'].mode()[0])

    trips = df['Start Station'] + " to " + df['End Station']
    print("Most frequent trip:", trips.mode()[0])

    print(f"\nThis took {time.time() - start_time} seconds.")
    print('-' * 40)


def trip_duration_stats(df):
    """Display statistics on the total and average trip duration."""
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    print("Total travel time:", df['Trip Duration'].sum())
    print("Mean travel time:", df['Trip Duration'].mean())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def user_stats(df):
    """Display statistics on bikeshare users."""
    print('\nCalculating User Stats...\n')
    start_time = time.time()

    print("\nUser Types:")
    print(df['User Type'].value_counts())

    if 'Gender' in df.columns:
        print("\nGender:")
        print(df['Gender'].value_counts())
    else:
        print("\nGender data is not available for this city.")

    if 'Birth Year' in df.columns:
        print("\nEarliest year of birth:", int(df['Birth Year'].min()))
        print("Most recent year of birth:", int(df['Birth Year'].max()))
        print("Most common year of birth:", int(df['Birth Year'].mode()[0]))
    else:
        print("\nBirth year data is not available for this city.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def display_raw_data(df):
    """Display raw data in groups of five rows based on user input."""
    rows_per_page = 5

    while row_index < len(df):
        answer = input("\nWould you like to see 5 rows of raw data? Enter yes or no:\n")
        answer = answer.lower().strip()

        if answer == 'yes':
            print(df.iloc[row_index:row_index + rows_per_page])
	    row_index += rows_per_page
        elif answer == 'no':
            break
        else:
            print("Invalid input. Please enter yes or no.")

    if row_index >= len(df):
        print("\nNo more raw data to display.")


def main():
    """Run the bikeshare analysis program."""
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        if df.empty:
            print("No data found for these filters. Please try again.")
        else:
            time_stats(df)
            station_stats(df)
            trip_duration_stats(df)
            user_stats(df)
            display_raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        restart = restart.lower().strip()

        if restart != 'yes':
            print("Goodbye!")
            break


if __name__ == "__main__":
    main()