
# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0


from collections import defaultdict


absa_quad_text2category = {
    'location general':'LOCATION#GENERAL',
    'food prices':'FOOD#PRICES',
    'food quality':'FOOD#QUALITY',
    'food general':'FOOD#GENERAL',
    'ambience general':'AMBIENCE#GENERAL',
    'service general':'SERVICE#GENERAL',
    'restaurant prices':'RESTAURANT#PRICES',
    'drinks prices':'DRINKS#PRICES',
    'restaurant miscellaneous':'RESTAURANT#MISCELLANEOUS',
    'drinks quality':'DRINKS#QUALITY',
    'drinks style_options':'DRINKS#STYLE_OPTIONS',
    'restaurant general':'RESTAURANT#GENERAL',
    'food style_options':'FOOD#STYLE_OPTIONS',
    "laptop": "laptop",
    "LAPTOP": "laptop",

}


def read_absa_quad_from_file(data_path):
    """
    Read data from file, each line is: sent####labels
    Return List[List[str]], List[List[Tuple]], Dict
    """
    all_sents, all_labels = [], []
    unique_labels = defaultdict(int)
    with open(data_path, 'r', encoding='UTF-8') as fp:
        words = []
        for line in fp:
            line = line.strip()
            if line != '':
                words, tuples = line.split('####')
                all_sents.append(words.split())
                tmp_labels = eval(tuples)
                new_labels = []
                for label in tmp_labels:
                    at,ac,sp,ot = label
                    if at == 'NULL':
                        at = 'none'
                    if ot == 'NULL':
                        ot = 'none'
                    if '#' not in ac:
                        ac = absa_quad_text2category[ac]
                    unique_labels[ac] += 1
                    new_labels.append((at.lower(),ac,sp,ot.lower()))
                all_labels.append(new_labels)
    return all_sents, all_labels, unique_labels
