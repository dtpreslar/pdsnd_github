import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input("Enter a city to analyze (choose chicago, new york city, washington): ").lower()
    if city not in ('chicago', 'new york city', 'washington'):
        print('Not a valid city...')
        city = input("Enter a city to analyze (choose chicago, new york city, washington): ").lower()
    # get user input for month (all, january, february, ... , june)
    month = input("Enter a month to filter by or select all: ").lower()
    if month not in ('january', 'february', 'march', 'april', 'may', 'june', 'all'):
        print('Not a valid month...')
        month = input("Enter a month to filter by or select all: ").lower()
    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = input("Enter a day to filter by or select all: ").lower()
    if day not in ('monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all'):
        print('Not a valid day...')
        day = input("Enter a day to filter by or select all: ").lower()
    print('-'*40)

    return city, month, day

def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """

    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])
    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.dayofweek

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
        day = days.index(day)
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day]
    print(df)
    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    months = ['january', 'february', 'march', 'april', 'may', 'june']
    print('Most common month: ', months[df['month'].value_counts().idxmax() - 1])

    # display the most common day of week
    days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    print('Most common day: ', days[df['day_of_week'].value_counts().idxmax() - 1])

    # display the most common start hour
    hours = df['Start Time']
    hour = hours.dt.hour
    print('Most common start hour: ', hour.value_counts().idxmax())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print('Most common start station: ', df['Start Station'].value_counts().idxmax())

    # display most commonly used end station
    print('Most common end station: ', df['End Station'].value_counts().idxmax())

    # display most frequent combination of start station and end station trip
    maax_data = df.groupby(['Start Station', 'End Station']).count().reset_index().sort_values('month', ascending=False)
    startmax = maax_data['Start Station'].iloc[0]
    endmax = maax_data['End Station'].iloc[0]
    print('Most common start and stop station trip: Start at: {start} , End at:  {end}'.format(start=startmax, end=endmax) )

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    totaltravtime = df['Trip Duration'].sum()
    print('Total travel time: ', totaltravtime)
    # display mean travel time
    meantravtime = df['Trip Duration'].mean()
    print('Mean travel time: ', meantravtime)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df,city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_type = df['User Type'].value_counts()
    print('User type count:')
    print(user_type)
    print(' ')
    # Display counts of gender
    if city == 'chicago' or city == 'new york city':
        gender = df['Gender'].value_counts()
        print('Gender count:')
        print(gender)
        print(' ')

    # Display earliest, most recent, and most common year of birth
        earliest = df['Birth Year'].sort_values().iloc[0]
        print('Earliest year of birth: ', earliest)
        recent = df['Birth Year'].sort_values().dropna().iloc[-1]
        print('Most recent year of birth: ', recent)
        year_count = df['Birth Year'].value_counts().sort_values().reset_index().iloc[-1]
        print('Most common year of birth: ', year_count['index'])

        print("\nThis took %s seconds." % (time.time() - start_time))
        print('-'*40)

def raw_data(df):
    row = 0
    answer = input("Would you like to see 5 lines of data (yes/no): ").lower()
    while True:
        if row +6 > len(df.axes[0]):
            print(df[row:row + 5])
            print('All data has been displayed!')
            break
        elif answer == 'yes' and row +6 <= len(df.axes[0]):
            print(df[row:row+5])
            row = row +5
            answer = input("Would you like to see 5 more lines of data: ").lower()
        elif answer != 'yes' and answer != 'no':
            print('Invalid input...')
            answer = input("Would you like to see 5 more lines of data: ").lower()
        else:
            break

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df,city)
        raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break
main()