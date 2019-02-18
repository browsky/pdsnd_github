import time
import pandas as pd
import numpy as np
import calendar

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

months = ['january', 'february', 'march', 'april', 'may', 'june', 'july',
          'august', 'september', 'october', 'november', 'december']

days_of_week = ['monday', 'tuesday', 'wednesday', 'thursday',
                'friday', 'saturday', 'sunday']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    print()

    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = ''
    while True:
        try:
            city = str(input("Please enter the city you want to see the data from (chicago, new york city, \
            washington, all): ")).lower()
            if city == 'all':
                print()
                break
            elif CITY_DATA.get(city):
                print()
                break
            else:
                print('There is no data enabled for the city entered!')
        except:
            print('An error occurred, please try again!')
            continue
        print()

    # get user input for month (all, january, february, ... , june)
    month = ''
    while True:
        try:
            month = str(input("Please enter the month (literal) you want to see the data from (all, january, \
            february, ... december): ")).lower()
            if month == 'all':
                print()
                break
            elif month in months:
                print()
                break
            else:
                print("The month entered isn't a valid month!")
        except:
            print('An error occurred, please try again!')
            continue
        print()

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = ''
    while True:
        try:
            day = str(input("Please enter the day (literal) you want to see the data from (all, monday, \
            tuesday, ... sunday): ")).lower()
            if day == 'all':
                print()
                break
            elif day in days_of_week:
                print()
                break
            else:
                print("The day entered isn't a valid day!")
        except:
            print('An error occurred, please try again!')
            continue
        print()

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
        df - pandas DataFrame containing city data filtered by month and day
    """
    # load data file into a dataframe
    df = pd.DataFrame()
    if city == 'all':
        for location in CITY_DATA:
            df = df.append(pd.read_csv(CITY_DATA[location]), sort=False)
    else:
        df = pd.read_csv(CITY_DATA[city])

    df['Start Time'] = pd.to_datetime(df['Start Time'])

    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    if month != 'all':
        month_int = months.index(month)+1
        df = df[(df['month'] == month_int)]

    if day != 'all':
        df = df[(df['day_of_week'] == day.title())]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""
    if len(df) > 0:
        print('\nCalculating The Most Frequent Times of Travel...\n')
        start_time = time.time()
        # display the most common month
        popular_month = df['month'].mode()
        for pop_month in popular_month:
            print('Most Popular Month: ', calendar.month_name[pop_month])

        # display the most common day of week
        popular_day = df['day_of_week'].mode()
        for pop_day in popular_day:
            print('Most Popular Day of the Week: ', pop_day)

        # display the most common start hour
        df['Start Time'] = pd.to_datetime(df['Start Time'])
        df['hour'] = df['Start Time'].dt.hour
        popular_hour = df['hour'].mode()
        for pop_hour in popular_hour:
            print('Most Popular Start Hour: ', pop_hour)

        print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""
    if len(df) > 0:
        print('\nCalculating The Most Popular Stations and Trip...\n')
        start_time = time.time()

        # display most commonly used start station
        popular_start_stn = df['Start Station'].mode()
        for pop_start_stn in popular_start_stn:
            print('Most Common Start Station: ', pop_start_stn)

        # display most commonly used end station
        popular_end_stn = df['End Station'].mode()
        for pop_end_stn in popular_end_stn:
            print('Most Common End Station: ', pop_end_stn)

        # display most frequent combination of start station and end station trip
        df['Trip Stations'] = df['Start Station'] + ' to ' + df['End Station']
        popular_trip_stns = df['Trip Stations'].mode()
        for pop_trip_stns in popular_trip_stns:
            print('Most Common Start and End Stations: ', pop_trip_stns)

        print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""
    if len(df) > 0:
        print('\nCalculating Trip Duration...\n')
        start_time = time.time()

        # display total travel time
        total_travel_time = df['Trip Duration'].sum()
        print('Total traveled time in seconds:  ', round(total_travel_time,2))
        print('Total traveled time in minutes:  ', round(total_travel_time/60,2))
        print('Total traveled time in hours:    ', round(total_travel_time/3600,2))
        print('Total traveled time in days:     ', round(total_travel_time/86400,2))

        # display mean travel time
        mean_travel_time = df['Trip Duration'].mean()
        print('Average traveled time in seconds: ', round(mean_travel_time,2))
        print('Average traveled time in minutes: ', round(mean_travel_time/60,2))
        print('Average traveled time in hours:   ', round(mean_travel_time/3600,2))
        print('Average traveled time in days:    ', round(mean_travel_time/86400,2))

        print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""
    if len(df) > 0:
        print('\nCalculating User Stats...\n')
        start_time = time.time()

        # Display counts of user types
        if 'User Type' in df.columns:
            user_types_qty = df['User Type'].value_counts()
            print('Quantity of trips by User Type: ')
            print(user_types_qty)
            print()
        else:
            print('There is no data of User Type for the city selected!')
            print()

        # Display counts of gender
        if 'Gender' in df.columns:
            genders_qty = df['Gender'].value_counts()
            print('Quantity of trips by User\'s Genders: ')
            print(genders_qty)
            print()
        else:
            print('There is no data of Gender for the city selected!')
            print()

        # Display earliest, most recent, and most common year of birth
        if 'Birth Year' in df.columns:
            earliest_by = df['Birth Year'].min()
            print('Most Earliest Year of Birth of Users: ', int(earliest_by))
            most_recent_by = df['Birth Year'].max()
            print('Most Recent Year of Birth of Users: ', int(most_recent_by))
            most_common_by = df['Birth Year'].mode()
            for common_by in most_common_by:
                print('Most Common Year of Birth of Users: ', int(common_by))
        else:
            print('There is no data of Birth Year for the city selected!')
            print()

        print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    """Displays the inicial menu."""
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        if len(df) > 0:
            time_stats(df)
            station_stats(df)
            trip_duration_stats(df)
            user_stats(df)
        else:
            print('There is no data for the filters selection!')

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

    row_count = 0
    show_rows = 5
    while True:
        row_count += show_rows
        restart = input('\nWould you like to see raw data? Enter yes or no.\n')
        if restart.lower() == 'yes':
            print(df[(row_count-show_rows):row_count])
        else:
            break

if __name__ == "__main__":
	main()
