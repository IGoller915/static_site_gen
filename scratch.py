import re

test = "test * string *"
split_test = re.split(r"(\*)", test)
print(split_test)