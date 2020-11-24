def readHeader(input):
    header_len = 0
    metadata_sum = 0
    value = 0
    child_values = []
    metadata_values = []

    num_children = int(input[header_len])
    header_len += 1
    num_metadata = int(input[header_len])
    header_len += 1
    
    for child in range(num_children):
        (child_len, child_metadata, child_value) = readHeader(input[header_len:])
        header_len += child_len
        metadata_sum += child_metadata
        child_values.append(child_value)

    for data in range(num_metadata):
        metadata = int(input[header_len])
        metadata_sum += metadata
        metadata_values.append(metadata)
        header_len += 1

        # Our value is given by valid indexes of our childrens' value
        if metadata > 0 and metadata <= num_children:
            value += child_values[metadata - 1]

    # No children; our value is the sum of our metadata
    if num_children is 0:
        value = sum(metadata_values)

    return (header_len, metadata_sum, value)

with open('day08_input.txt') as f:
    input = f.read().rstrip('\n').split()

result = readHeader(input)
print "%d nodes, %d metadata, %d value" % (result[0], result[1], result[2])
