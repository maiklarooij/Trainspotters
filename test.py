import random

def breed_uniform( first_parent, second_parent):

    child_length = max([len(parent) for parent in [first_parent, second_parent]])
    bits = [random.randint(0, 1) for _ in range(child_length)]

    child = []
    for i in range(child_length-1):

        parent = first_parent if bits[i] == 1 else second_parent

        if i < len(parent):
            child.append(parent[i])

    return child

print(breed_uniform([1, 2, 3, 6, 9, 23, 39, 28, 39, 12], [28, 32, 10, 2, 1, 102]))