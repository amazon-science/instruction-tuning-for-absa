
# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0

"""
Converts the data from the triplet format used by https://github.com/xuuuluuu/Position-Aware-Tagging-for-ASTE/ to
the format used in this code (quad)
Appends "LAPTOP" as the category
"""

import os
import argparse

sentiment_map = {
    'POS': 'positive',
    'NEG': 'negative',
    'NEU': 'neutral',
}

def convert_line_to_quad(line: str) -> str:
    sentence, tuples = line.split('####')
    words = sentence.split(' ')
    labels = eval(tuples)
    new_labels = []
    for (aspect_term_indices, opinion_term_indices, sentiment) in labels:
        aspect_term  = ' '.join([words[x] for x in aspect_term_indices])
        opinion_term = ' '.join([words[x] for x in opinion_term_indices])
        new_labels.append([aspect_term, 'laptop', sentiment_map[sentiment], opinion_term])
    return '####'.join([sentence, str(new_labels)])


def get_args():
    parser = argparse.ArgumentParser("Create laptop 14 data in quad format")
    parser.add_argument("--train_file", required=True, type=str, help="train file")
    parser.add_argument("--dev_file", required=True, type=str, help="dev file")
    parser.add_argument("--test_file", required=True, type=str, help="test file")
    parser.add_argument("--output_dir", required=True, type=str, help="Output directory to save new files")
    args = parser.parse_args()
    return args


def main():
    args = get_args()
    with open(args.train_file) as fin:
        lines = []
        for line in fin:
            lines.append(convert_line_to_quad(line))
        with open(os.path.join(args.output_dir, 'train.txt'), 'w+') as fout:
            for line in lines:
                _=fout.write(f'{line}\n')

    with open(args.dev_file) as fin:
        lines = []
        for line in fin:
            lines.append(convert_line_to_quad(line))
        with open(os.path.join(args.output_dir, 'dev.txt'), 'w+') as fout:
            for line in lines:
                _=fout.write(f'{line}\n')

    with open(args.test_file) as fin:
        lines = []
        for line in fin:
            lines.append(convert_line_to_quad(line))
        with open(os.path.join(args.output_dir, 'test.txt'), 'w+') as fout:
            for line in lines:
                _=fout.write(f'{line}\n')

if __name__ == "__main__":
    main()