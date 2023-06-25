from faker import Faker
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

users = []

def generate_users(num_of_users):
    Faker.seed(10)
    f = Faker(["en_US", "ja_JP", "uk_UA", "de_DE", "pl_PL", "tr_TR", "cs_CZ", "fr_FR"])
    for i in range(num_of_users):
        p = f.profile()
        users.append({"name": p["name"], "birthdate": p["birthdate"]})
    return users

def get_birthdays_per_week():
    today = datetime.today().date()
    next_week = today + timedelta(days=7)
    bd_per_week = {}

    for user in users:
        bd = user["birthdate"]
        bd += relativedelta(years=next_week.year - bd.year)

        if bd.weekday() >= 5:
            bd += timedelta(days=7 - bd.weekday())

        if today <= bd < next_week:
            weekday = bd.strftime("%A")
            if weekday not in bd_per_week:
                bd_per_week[weekday] = []
            bd_per_week[weekday].append(user["name"])

    return bd_per_week

if __name__ == "__main__":
    num_of_users = int(input("Number of users? >>> "))
    users_list = generate_users(num_of_users)  
    bd_per_week = get_birthdays_per_week()

    if bd_per_week:
        for weekday in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']:
             if weekday in bd_per_week:
                n = ", ".join(bd_per_week[weekday])
                print(f"{weekday}: {n}")
    else:
        print("No birthdays next week.")