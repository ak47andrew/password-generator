def encode(data: list[int], length: int):
    final_data = data[::(len(data) // (length + 1)) or 1][1:]
    while len(final_data) < length:
        final_data += final_data
    final_data = final_data[:length]
    password =  "".join([chr((i + ind * length - 1) % 94 + 33) for ind, i in enumerate(final_data)])

    return password
