def encode(data: list[int], length: int, offset: int = 0):
    input = data[::(len(data) // length + offset) or 1]
    while len(input) < length:
        input = input + input
    input = input[:length]
    password =  "".join([chr(val if (val := (i + 66 + ind * 20) % 127) > 33 and val <= 127 else val + 33 % 126) 
                    for ind, i in enumerate(input)])

    return password
