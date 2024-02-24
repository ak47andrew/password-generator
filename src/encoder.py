def encode(data: list[int], length: int):
    input = data[::(len(data) // (length + 1)) or 1][1:]
    while len(input) < length:
        input += input
    input = input[:length]
    password =  "".join([chr((i + ind * length - 1) % 94 + 33) for ind, i in enumerate(input)])

    return password
