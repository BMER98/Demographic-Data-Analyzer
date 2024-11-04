import pandas as pd

def calculate_demographic_data(print_data=True):
    # Read data from file
    df = pd.read_csv('adult.data.csv', header=None, names=[
        'age', 'workclass', 'fnlwgt', 'education', 'education-num',
        'marital-status', 'occupation', 'relationship', 'race', 'sex',
        'capital-gain', 'capital-loss', 'hours-per-week', 'native-country', 'salary'
    ])

    # Ensure columns are of correct type
    df['age'] = pd.to_numeric(df['age'], errors='coerce')
    df['hours-per-week'] = pd.to_numeric(df['hours-per-week'], errors='coerce')
    df['salary'] = df['salary'].astype(str)

    # How many of each race are represented in this dataset?
    race_count = df['race'].value_counts().reindex(['White', 'Black', 'Asian-Pac-Islander', 'Amer-Indian-Eskimo', 'Other']).fillna(0).astype(int)

    # Average age of men
    men_ages = df[df['sex'] == 'Male']['age'].dropna()
    average_age_men = round(men_ages.mean(), 1) if not men_ages.empty else 0

    # Percentage of people who have a Bachelor's degree
    percentage_bachelors = round((df['education'] == 'Bachelors').mean() * 100, 1)

    # Percentage of people with advanced education making >50K
    higher_education = df['education'].isin(['Bachelors', 'Masters', 'Doctorate'])
    higher_education_rich = round((df[higher_education & (df['salary'] == '>50K')].shape[0] / df[higher_education].shape[0]) * 100, 1)

    # Percentage of people without advanced education making >50K
    lower_education = ~higher_education
    lower_education_rich = round((df[lower_education & (df['salary'] == '>50K')].shape[0] / df[lower_education].shape[0]) * 100, 1)

    # Minimum number of hours a person works per week
    min_work_hours = int(df['hours-per-week'].min())

    # Number of people working minimum hours and percentage of rich among them
    num_min_workers = df[df['hours-per-week'] == min_work_hours]
    rich_min_workers = num_min_workers[num_min_workers['salary'] == '>50K']
    rich_percentage = round((len(rich_min_workers) / len(num_min_workers)) * 100, 1) if len(num_min_workers) > 0 else 0

    # Country with the highest percentage of people that earn >50K
    country_earnings = df[df['salary'] == '>50K']['native-country'].value_counts()
    country_totals = df['native-country'].value_counts()
    highest_earning_country_percentage = round((country_earnings / country_totals * 100).max(), 1)
    highest_earning_country = (country_earnings / country_totals * 100).idxmax()

    # Most popular occupation for those who earn >50K in India
    top_IN_occupation = df[(df['native-country'] == 'India') & (df['salary'] == '>50K')]['occupation'].mode()[0]

    # DO NOT MODIFY BELOW THIS LINE

    if print_data:
        print("Number of each race:\n", race_count)
        print("Average age of men:", average_age_men)
        print(f"Percentage with Bachelors degrees: {percentage_bachelors}%")
        print(f"Percentage with higher education that earn >50K: {higher_education_rich}%")
        print(f"Percentage without higher education that earn >50K: {lower_education_rich}%")
        print(f"Min work time: {min_work_hours} hours/week")
        print(f"Percentage of rich among those who work fewest hours: {rich_percentage}%")
        print("Country with highest percentage of rich:", highest_earning_country)
        print(f"Highest percentage of rich people in country: {highest_earning_country_percentage}%")
        print("Top occupations in India:", top_IN_occupation)

    return {
        'race_count': race_count,
        'average_age_men': average_age_men,
        'percentage_bachelors': percentage_bachelors,
        'higher_education_rich': higher_education_rich,
        'lower_education_rich': lower_education_rich,
        'min_work_hours': min_work_hours,
        'rich_percentage': rich_percentage,
        'highest_earning_country': highest_earning_country,
        'highest_earning_country_percentage': highest_earning_country_percentage,
        'top_IN_occupation': top_IN_occupation
    }
