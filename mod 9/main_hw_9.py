# Функція-декоратор для обробки помилок введення користувача
def input_error(func):
  def wrapper(*args, **kwargs):
    try:
      return func(*args, **kwargs)
    except KeyError:
      return "Enter user name"
    except ValueError:
      return "Give me name and phone please"
    except IndexError:
      return "Invalid input format. Use 'add', 'change', 'phone', 'show all', or 'good bye'."
  return wrapper


contacts = {}

@input_error
def handle_hello():
  return "How can I help you?"

@input_error
def handle_add(input_str):
  _, name, phone = input_str.split()
  contacts[name.lower()] = phone
  return f"Added {name.title()} with phone {phone}"

@input_error
def handle_change(input_str):
  _, name, phone = input_str.split()
  if name.lower() in contacts:
    contacts[name.lower()] = phone
    return f"Changed phone for {name.title()} to {phone}"
  else:
    return f"{name.title()} not found in contacts"

@input_error
def handle_phone(name):
  if name.lower() in contacts:
    return f"{name.title()}'s phone number is {contacts[name.lower()]}"
  else:
    return f"{name.title()} not found in contacts"

@input_error
def handle_show_all():
  if not contacts:
    return "No contacts found."
  else:
    return "\n".join([f"{name.title()}: {phone}" for name, phone in contacts.items()])

def main():
  print("Hello! I'm your assistant bot.")
  while True:
    user_input = input("> ").strip().lower()
    if user_input in ["good bye", "close", "exit"]:
      print("Good bye!")
      break
    elif user_input == "hello":
      response = handle_hello()
    elif user_input.startswith("add"):
      response = handle_add(user_input)
    elif user_input.startswith("change"):
      response = handle_change(user_input)
    elif user_input.startswith("phone"):
      name = user_input.split(" ", 1)[1]
      response = handle_phone(name)
    elif user_input == "show all":
      response = handle_show_all()
    else:
      response = "Invalid command. Use 'hello', 'add', 'change', 'phone', 'show all', 'close', 'exit' or 'good bye'."
    print(response)

if __name__ == "__main__":
    main()
