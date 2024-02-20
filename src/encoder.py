def encode(data: list[int], length: int, offset: int = 0):
    input = data[::(len(data) // (length + 1 + offset)) or 1][1:]
    while len(input) < length:
        input = input + input
    input = input[:length]
    password =  "".join([chr((i + ind * length - 1) % 94 + 33) for ind, i in enumerate(input)])

    return password
