
# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0

from collections import defaultdict
from email.policy import default
import os
import random
import argparse
from data_utils import read_absa_quad_from_file
from typing import List, Tuple, Set

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)



# GLOBAL_SEED = 12347
SEED_INCREMENT = 1237


def _select_k_points_per_class(all_sents: List[List[str]], all_labels: List[List[Tuple]], unique_labels: Set[str], k: int):

    def label_not_covered(label_count, k):
        for label in label_count:
            if label_count[label] < k:
                return label
        return None

    def update_label_count(labels, label_count):
        for label in labels:
            at,ac,sp,ot = label
            if '#' in ac:
                ac = ac.split('#')[0]
            label_count[ac] += 1

    subsampled_sents = []
    subsampled_labels = []
    label_count = {label: 0 for label in unique_labels}

    for i, labels in enumerate(all_labels):
        for label in labels:
            at,ac,sp,ot = label
            if '#' in ac:
                ac = ac.split('#')[0]
            if label_count[ac] >= k:
                continue
            else:
                subsampled_sents.append(all_sents[i])
                subsampled_labels.append(labels)
                update_label_count(labels, label_count)
                break
        if label_not_covered(label_count, k) is None:
            break

    not_covered = label_not_covered(label_count, k)

    if not_covered:
        logger.info(f"Not enough labels to fulfil {k} samples for {not_covered}")
        # raise ValueError(f"Not enough labels to fulfil {k} samples for {not_covered}")

    return subsampled_sents, subsampled_labels, label_count


def write_subsampled_data(output_file: str, all_sents: List[List[str]], all_labels: List[List[Tuple]]):
    with open(output_file, 'w+') as fhw:
        for sent,labels in zip(all_sents, all_labels):
            sent = ' '.join(sent)
            line = f'{sent}####{repr(labels)}'
            fhw.write(line)
            fhw.write('\n')


def get_parser():
    parser = argparse.ArgumentParser("prepare kshot data")

    parser.add_argument("--input_file", required=True, type=str, help="Input file")
    parser.add_argument("--output_dir", required=True, type=str, help="Output directory")
    parser.add_argument("--num_shot", required=True, type=int, help="number of shot for each entity type")
    parser.add_argument("--num_repeat", type=int, default=1, help="number of times to repeat the same sampling strategy")
    parser.add_argument("--seed", type=int, default=12347, help="random seed")
    return parser

def main():
    parser = get_parser()
    config = parser.parse_args()
    all_sents_original, all_labels_original, unique_labels_original = read_absa_quad_from_file(config.input_file)
    unique_labels = defaultdict(int)
    GLOBAL_SEED = config.seed
    for k,v in unique_labels_original.items():
        k = k.split('#')[0]
        unique_labels[k] += v
    print('unique_labels:', unique_labels)
    for i in range(config.num_repeat):
        current_seed = GLOBAL_SEED+(i*SEED_INCREMENT)
        random.seed(current_seed)
        combined = list(zip(all_sents_original, all_labels_original))
        random.shuffle(combined)
        all_sents, all_labels= zip(*combined)
        subsampled_sents, subsampled_labels, label_count = _select_k_points_per_class(all_sents, all_labels, unique_labels, config.num_shot)
        output_file = os.path.join(config.output_dir, os.path.basename(config.input_file).rsplit('.',1)[0]+f'_k_{config.num_shot}_seed_{current_seed}.txt')
        write_subsampled_data(output_file, subsampled_sents, subsampled_labels)
        print(f'Iteration={i+1}, k={config.num_shot}, seed={current_seed}, label_count={label_count}')

if __name__ == '__main__':
    main()