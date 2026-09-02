def calculator():
    while True:
        print("\n==============================")
        print("      SIMPLE CALCULATOR")
        print("==============================")
        print("1. Addition (+)")
        print("2. Subtraction (-)")
        print("3. Multiplication (*)")
        print("4. Division (/)")
        print("5. Exit")
        print("==============================")

        choice = input("Enter your choice (1-5): ").strip()

        if choice == "5":
            print("👋 Calculator closed. Thank you!")
            break

        if choice not in ["1", "2", "3", "4"]:
            print("❌ Invalid choice. Please enter 1, 2, 3, 4 or 5.")
            continue

        try:
            num1 = float(input("Enter first number: "))
            num2 = float(input("Enter second number: "))

            if choice == "1":
                result = num1 + num2
                operator = "+"

            elif choice == "2":
                result = num1 - num2
                operator = "-"

            elif choice == "3":
                result = num1 * num2
                operator = "*"

            elif choice == "4":
                if num2 == 0:
                    print("❌ Cannot divide by zero.")
                    continue

                result = num1 / num2
                operator = "/"

            print(f"\n✅ Result: {num1:g} {operator} {num2:g} = {result:g}")

        except ValueError:
            print("❌ Please enter valid numbers.")


if __name__ == "__main__":
    calculator()