def Data_Refinery(rec):
    import re
    def extract_numbers(string):
        # pattern = r'-?\d+(?:\.\d+)?E-?\d+'

        pattern = r'-?\d+(?:\.\d+)?(?:E-?\d+)?'  # Regular expression pattern to match decimal numbers and scientific notation
        numbers = re.findall(pattern, string)
        return numbers

    for index, items in enumerate(rec):
        if index == 0:
            dataset = extract_numbers(items)
        else:
            dataset += extract_numbers(items)

    dataset = [float(x) for x in dataset]
    dataset = np.array(dataset).astype("float")
    return dataset


def write_file(FileName, ValueList):
    with open(FileName, 'w') as f:
        for Value in ValueList:
            f.write(str(Value))
            f.write("\n")
