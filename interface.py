import sys


def show_welcome_message():
    # Display the welcome message with the 2 available choices about the scenarios
    print("\nWelcome!\n\nIn this interface you can choose to see the benevolent or the malicious scenario."
          "\nWhat do you want to see?\n   (0) the benevolent scenario; \n   (1) the malicious scenario.")

def run_scenario(choice):
    # Executing the chosen scenario based on user input
    try:
        if choice == "0":
            print("\nRunning the benevolent scenario...\n")
            import main_benevolent
        elif choice == "1":
            print("\nRunning the malicious scenario...\n")
            import main_malicious
        else:
            raise ValueError("Invalid choice. Please select '0', '1', or 'exit'.")
    except ImportError as e:
        print(f"Error: Unable to import the specified module. {e}")
    except ValueError as e:
        print(e)


def main():
    # Main function to drive the program
    #while True:
    show_welcome_message()

    user_input = input("Insert your choice here or type 'exit' to quit: ").strip().lower()

    if user_input == "exit":
        print("\nThank you for joining! Exiting the program.")
        sys.exit()  # Exit the program
    else:
        run_scenario(user_input)


if __name__ == "__main__":
    main()

