# import uuid

# code = str(uuid.uuid4()).replace('-', '')[:12]
# code1= f"the code*** {code}"
# print(code1)


try:
    result = 10 / 00
except ZeroDivisionError:
    print("Cannot divide by zero!")
except Exception as e:
    print(f"An error occurred: {e}")


