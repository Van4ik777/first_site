




def x_y(strin):
    x_find = strin.find("x")
    y_find = strin.find("y")

    if x_find == -1 and y_find == -1:
        return "У рядку немає символів 'x' та 'y'"
    elif x_find < y_find:
        return "'x' зустрічається раніше"
    else:
        return "'y' зустрічається раніше"

strin = input(" ")
result = x_y(strin)
print(result)


def matching_indexes(string):
    last_char = string[-1]
    indexes = []
    for i in range(len(string)):
        if string[i] == last_char:
            indexes.append(i)
    return indexes

input_string = input(" ")
result = matching_indexes(input_string)
print("", result)