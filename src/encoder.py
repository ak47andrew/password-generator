def encode(data: list[int], length: int) -> str:
    final_data = split_and_sum_with_interaction(data, length)
    password =  "".join([chr((i + ind * length - 1) % 94 + 33) for ind, i in enumerate(final_data)])

    return password


def split_and_sum_with_interaction(source: list[int], length: int) -> list[int]:
    """
    Splits a list into sublists and computes interactive sums to generate password components.
    
    Args:
        source (list[int]): Input list of integers to process
        length (int): Desired length of the output list
    
    Returns:
        list[int]: Processed list of integers for password generation
    
    Raises:
        ValueError: If length is not positive or source is None
    """
    # Input validation
    if not source:
        return []
    if length <= 0:
        raise ValueError("Length must be a positive integer")

    # Calculate initial chunk size for splitting
    chunk_size = max(1, len(source) // length)
    
    # Create initial sublists
    sublists = [
        source[i:i + chunk_size]
        for i in range(0, len(source), chunk_size)
    ]

    # Generate additional sublists if needed
    while len(sublists) < length:
        new_sublists = []
        for sublist in sublists:
            # Generate new sublist with interaction
            new_sublist = [
                (element + len(sublists) + i) ^ element
                for i, element in enumerate(sublist)
            ]
            new_sublists.append(new_sublist)
        sublists.extend(new_sublists)
        
    # Trim to desired length
    sublists = sublists[:length]

    # Calculate interactive sums
    result = []
    for i in range(length):
        # Sum both the i-th elements from all sublists and the i-th sublist itself
        current_sum = sum(sublist[i] if i < len(sublist) else 0 for sublist in sublists)
        current_sum += sum(sublists[i]) if i < len(sublists) else 0
        result.append(current_sum)

    # Apply final transformations
    for _ in range(3):
        for i in range(len(result) - 1):
            result[i] = result[i - 1] + result[i] * result[i + 1]
        result[-1] = result[-2] + result[-1]

    return result
