from lingpy import *
from collections import defaultdict
import csv

profile = defaultdict(list)
language = "Asuri"

with open('../raw/data.csv') as f:
    for row in csv.DictReader(f):
        form = row["FORM"].strip()
        if not form:
            continue
        tokens = ipa2tokens(
            form.replace(" ", "_"),
            merge_vowels=True,
            semi_diacritics="shʃʂɕʑʒʐɦ"
        )
        if tokens:
            profile["^" + tokens[0]] += [(language, form, " ".join(tokens))]
            for token in tokens[1:-1]:
                profile[token] += [(language, form, " ".join(tokens))]
            if len(tokens) > 1:
                profile[tokens[-1] + "$"] += [(language, form, " ".join(tokens))]

lexemes = []
with open("../etc/orthography.tsv", "w") as f:
    f.write("Grapheme\tIPA\tFrequency\tExamples\n")
    for sound, vals in sorted(
        profile.items(),
        key=lambda x: (x[0].strip("^").strip("$"), len(x[1])),
        reverse=True
    ):
        freq = len(vals)
        if freq < 5:
            lexemes += vals
        examples = " // ".join([row[1] for row in vals[:2]])
        f.write("\t".join([sound, sound.strip("^").strip("$"), str(freq), examples]) + "\n")
