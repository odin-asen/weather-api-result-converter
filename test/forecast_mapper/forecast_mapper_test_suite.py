def read_resources_file(relative_path) -> str:
    file_path = '../resources/json/{relative_path}'.format(relative_path=relative_path)
    with open(file_path, 'r') as json_file:
        return json_file.read()


def read_input_test_json(file_name) -> str:
    return read_resources_file('in/{file_name}.json'.format(file_name=file_name))


def read_output_test_json(file_name) -> str:
    return read_resources_file('out/{file_name}.json'.format(file_name=file_name))
