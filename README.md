# Instruction Tuning for Few-Shot Aspect-Based Sentiment Analysis

The package contains sources to construct the subsampled datasets for the few-shot experiments
used in the paper.

-------------------------------------------------------

Link to data:

REST15:

https://github.com/IsakZhang/ABSA-QUAD/tree/master/data/rest15

REST16:

https://github.com/IsakZhang/ABSA-QUAD/tree/master/data/rest16

LAP14:

https://github.com/xuuuluuu/Position-Aware-Tagging-for-ASTE/tree/master/data/ASTE-Data-V2/14lap

-------------------------------------------------------

Command to create the k-shot subsets for REST15/REST16

To create train subsamples for K=5:

python prepare_kshot_data_cat.py --input_file <path to rest15/rest16 original data>/train.txt --output_dir <path to output directory> --num_shot 5 --num_repeat 1

For dev subsamples, replace train.txt with dev.txt

-------------------------------------------------------

Command to create the k-shot subsets for LAP14

Convert above laptop14 data to quad format as follows:

python laptop_data_conversion.py --train_file <path to>/train_triplets.txt --dev_file <path to>/dev_triplets.txt --test_file <path to>/test_triplets.txt --output_dir <path to output dir>

Now create train subsamples using data in quad format(for K=5):

python prepare_kshot_data_sent.py --input_file <path to lap14 original data>/train.txt --output_dir <path to output directory> --num_shot 5 --num_repeat 1

For dev subsamples, replace train.txt with dev.txt

# Citation
If you find the sources useful, please consider citing our work:

```
@inproceedings{varia-etal-2023-instruction,
      title={Instruction Tuning for Few-Shot Aspect-Based Sentiment Analysis}, 
      author={Varia, Siddharth and Wang, Shuai and Halder, Kishaloy and Vacareanu, Robert and Ballesteros, Miguel and Benajiba, Yassine and John, Neha Anna and Anubhai, Rishita and Muresan, Smaranda and Roth, Dan},
      year={2023},
      month = "jul",
      booktitle = "Proceedings of the 13th Workshop on Computational Approaches to Subjectivity, Sentiment and Social Media Analysis",
      publisher = "Association for Computational Linguistics"
}
```

