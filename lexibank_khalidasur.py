import attr
from pathlib import Path

from pylexibank import Concept, Language, FormSpec
from pylexibank.dataset import Dataset as BaseDataset

from clldutils.misc import slug


@attr.s
class CustomConcept(Concept):
    Gloss = attr.ib(default=None)
    Number = attr.ib(default=None)


@attr.s
class CustomLanguage(Language):

    Name = attr.ib(default=None)
    SubGroup = attr.ib(default="Munda")
    Family = attr.ib(default="Austroasiatic")
    DialectGroup = attr.ib(default="Asuric")


class Dataset(BaseDataset):
    dir = Path(__file__).parent
    id = "khalidasur"
    concept_class = CustomConcept
    language_class = CustomLanguage
    form_spec = FormSpec(separators=";/,")

    def cmd_makecldf(self, args):
        args.writer.add_sources()
        
        args.writer.add_language(
            ID="Asuri",
            Glottocode="asur1254",
            Name="Asuri",
            Latitude=21.57,
            Longitude=83.46,
            Family="Austroasiatic"
        )

        raw = {
            row["CONCEPT"]: row["FORM"]
            for row in self.raw_dir.read_csv("raw/data.csv", dicts=True)
            if row["FORM"].strip()
        }

        for concept in self.conceptlists[0].concepts.values():
            idx = concept.number + "_" + slug(concept.concepticon_gloss)
            args.writer.add_concept(
                ID=idx,
                Name=concept.english,
                Number=concept.number,
                Concepticon_ID=concept.concepticon_id,
                Concepticon_Gloss=concept.concepticon_gloss,
            )
            form = raw.get(concept.english)
            if form:
                args.writer.add_forms_from_value(
                    Language_ID="Asuri",
                    Parameter_ID=idx,
                    Value=form,
                    Source="khalid2020",
                )