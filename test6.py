# Input array
original_array = [['b', 'w', 'w'],
                  ['b', 'w', 'w'],
                  ['b', 'w', 'w']]

# Mirrored array
mirrored_array = [row[::-1] for row in original_array]
for row in mirrored_array:
    print(row)