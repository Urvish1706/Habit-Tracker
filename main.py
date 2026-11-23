
import json
import os
from datetime import date, timedelta

FILE_NAME = "habits.json"


def load_habits():
    if os.path.exists(FILE_NAME):
        try:
            with open(FILE_NAME, "r") as file:
                data = json.load(file)

                if isinstance(data, list):
                    return data

                return []

        except (json.JSONDecodeError, FileNotFoundError):
            return []

    return []


def save_habits(habits):
    with open(FILE_NAME, "w") as file:
        json.dump(habits, file, indent=4)


def add_habit(habits):
    name = input("Enter habit name: ").strip()

    if not name:
        print("Habit name cannot be empty!")
        return

    habit = {
        "id": max([h["id"] for h in habits], default=0) + 1,
        "name": name,
        "history": []
    }

    habits.append(habit)
    save_habits(habits)
    print("Habit added successfully!")


def view_habits(habits):
    if not habits:
        print("No habits found!")
        return

    print("\n========== YOUR HABITS ==========")

    for habit in habits:
        today = date.today().isoformat()
        status = "Completed" if today in habit["history"] else "Pending"

        print(f'{habit["id"]}. {habit["name"]} - {status}')


def update_habit(habits):
    view_habits(habits)

    try:
        habit_id = int(input("Enter habit ID to update: "))
    except ValueError:
        print("Invalid ID!")
        return

    for habit in habits:
        if habit["id"] == habit_id:
            new_name = input("Enter new habit name: ").strip()

            if new_name:
                habit["name"] = new_name
                save_habits(habits)
                print("Habit updated successfully!")
            return

    print("Habit not found!")


def complete_habit(habits):
    view_habits(habits)

    try:
        habit_id = int(input("Enter habit ID to complete: "))
    except ValueError:
        print("Invalid ID!")
        return

    for habit in habits:
        if habit["id"] == habit_id:
            today = date.today().isoformat()

            if today in habit["history"]:
                print("Already completed today!")
            else:
                habit["history"].append(today)
                save_habits(habits)
                print("Habit completed successfully!")
            return

    print("Habit not found!")


def delete_habit(habits):
    view_habits(habits)

    try:
        habit_id = int(input("Enter habit ID to delete: "))
    except ValueError:
        print("Invalid ID!")
        return

    for habit in habits:
        if habit["id"] == habit_id:
            habits.remove(habit)
            save_habits(habits)
            print("Habit deleted successfully!")
            return

    print("Habit not found!")


def calculate_streak(history):
    completed = set(history)
    streak = 0
    current = date.today()

    while current.isoformat() in completed:
        streak += 1
        current -= timedelta(days=1)

    return streak


def weekly_statistics(habits):
    if not habits:
        print("No habits available!")
        return

    today = date.today()
    week_start = today - timedelta(days=today.weekday())
    week_dates = {
        (week_start + timedelta(days=i)).isoformat()
        for i in range(7)
    }

    total = len(habits) * 7
    completed = 0

    print("\n========== WEEKLY STATISTICS ==========")

    for habit in habits:
        weekly_done = len(set(habit["history"]) & week_dates)
        completed += weekly_done

        streak = calculate_streak(habit["history"])

        print(f'\nHabit: {habit["name"]}')
        print(f"Weekly Completed: {weekly_done}/7")
        print(f"Current Streak: {streak} days")

    percentage = (completed / total) * 100

    print("\nTotal Weekly Progress:")
    print(f"Completion: {percentage:.2f}%")
    print(f"Completed: {completed}/{total}")


def main():
    habits = load_habits()

    while True:
        print("\n================================")
        print("       HABIT TRACKER")
        print("================================")
        print("1. Add Habit")
        print("2. View Habits")
        print("3. Update Habit")
        print("4. Mark Habit Complete")
        print("5. Delete Habit")
        print("6. Weekly Statistics")
        print("7. Exit")

        choice = input("\nEnter your choice: ")

        if choice == "1":
            add_habit(habits)
        elif choice == "2":
            view_habits(habits)
        elif choice == "3":
            update_habit(habits)
        elif choice == "4":
            complete_habit(habits)
        elif choice == "5":
            delete_habit(habits)
        elif choice == "6":
            weekly_statistics(habits)
        elif choice == "7":
            print("Thank you for using Habit Tracker!")
            break
        else:
            print("Invalid choice! Try again.")


if __name__ == "__main__":
    main()
