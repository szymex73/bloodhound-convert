import argparse
import json
import os
import zipfile
from bloodhound_convert.converters import *


def check_valid_file_or_dir(input_path):
    if not os.path.exists(input_path):
        return False

    if input_path[-4:] == '.zip' and os.path.isfile(input_path):
        zip = zipfile.ZipFile(input_path)
        if [filename for filename in zip.namelist() if filename.endswith('.json')] == []:
            zip.close()
            return False

        zip.close()
        return True

    if not os.path.isdir(input_path):
        return False

    if [filename for filename in os.listdir(input_path) if filename.endswith('.json')] == []:
        return False

    return True


def read_from_directory(input_path):
    data = {}
    for filename in os.listdir(input_path):
        timestamp, datatype = filename.split('.')[0].split('_')

        if 'timestamp' not in data:
            data['timestamp'] = timestamp

        f = open(os.path.join(input_path, filename), 'rb')
        data[datatype] = json.load(f)
        f.close()

    return data


def read_from_zipfile(input_path):
    data = {}
    zip = zipfile.ZipFile(input_path)

    for filename in zip.namelist():
        timestamp, datatype = filename.split('.')[0].split('_')

        if 'timestamp' not in data:
            data['timestamp'] = timestamp

        # Even though it's r, zipfile returns bytes on .read()
        f = zip.open(filename, 'r')
        data[datatype] = json.load(f)
        f.close()

    zip.close()
    return data


def write_to_zipfile(output_path, data):
    zip = zipfile.ZipFile(output_path, 'w')
    for datatype in data['files']:
        filename = f'{data["timestamp"]}_{datatype}.json'
        f = zip.open(filename, 'w')
        f.write(json.dumps(data[datatype]).encode())
        f.close()
    zip.close()


def write_to_dir(output_path, data):
    for datatype in data['files']:
        filename = f'{data["timestamp"]}_{datatype}.json'
        f = open(os.path.join(output_path, filename), 'wb')
        json.dump(data[datatype], f)
        f.close()


def main():
    parser = argparse.ArgumentParser(
        add_help=True,
        description='Python based Bloodhound data converter from the legacy pre 4.1 format to 4.1+ format',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument('input', type=str, help='Data input, can be either a zip file or a directory containing JSON data files')
    parser.add_argument('output', type=str, help='Data output, can be either a zip file or a directory which the JSON files will be saved into')

    args = parser.parse_args()

    if not check_valid_file_or_dir(args.input):
        print(f"Given input ('{args.input}') is not a zip file or a directory containing json files")
        exit(1)

    if args.output[-4:] != '.zip' and not os.path.exists(args.output):
        print(f"Given output path ('{args.input}') is not a zip file or a directory")
        exit(1)

    if args.input[-4:] == '.zip':
        input_data = read_from_zipfile(args.input)
    else:
        input_data = read_from_directory(args.input)

    output_data = {}
    output_data['timestamp'] = input_data['timestamp']
    output_data['files'] = []

    for converter_name, converter_func in converters.items():
        if converter_name in input_data:
            print(f'Processing {converter_name}')
            output_data[converter_name] = converter_func(input_data[converter_name])
            output_data['files'].append(converter_name)

    if args.output[-4:] == '.zip':
        write_to_zipfile(args.output, output_data)
    else:
        write_to_dir(args.output, output_data)

    print('Done.')
