from datetime import date, timedelta, datetime



def get_birthdays_per_week(users):
    birthday_dict = {}
    if not users:
        birthday_dict.clear()
    else:
        today = date.today()
        end_day = today + timedelta(days=7)
        for user in users:
            birthday = user['birthday']
            if birthday.month == 1:
                birthday = birthday.replace(year=today.year + 1)
            else:
                birthday = birthday.replace(year=today.year)
            if today <= birthday <= end_day:
                day_of_week = birthday.strftime("%A")
                if day_of_week in ["Saturday", "Sunday"]:
                    birthday_dict.setdefault('Monday', []).append(user['name'])
                else:
                    birthday_dict.setdefault(day_of_week, []).append(user['name'])
            else:
                continue
    return birthday_dict
   


if __name__ == "__main__":
    users = [
        {"name": "Jan Koum", "birthday": datetime(1976, 1, 1).date()},
    ]

    result = get_birthdays_per_week(users)
    print(result)
    # Виводимо результат
    for day_name, names in result.items():
        print(f"{day_name}: {', '.join(names)}")
