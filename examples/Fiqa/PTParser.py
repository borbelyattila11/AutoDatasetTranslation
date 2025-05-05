import sys, argparse
sys.path.insert(0, r'./')

from tqdm.notebook import tqdm
from datasets import load_dataset, load_from_disk
from configs import PTConfig
from translator import DataParser

PARSER_NAME = "DefaultParser"

class DefaultParser(DataParser):
    def __init__(self, file_path: str, output_path: str):
        super().__init__(file_path, output_path,
                         parser_name=PARSER_NAME,
                         target_config=PTConfig,    # The data config to be validated to check if self implement "convert" function is correct or not,
                                                        # you must map the data form to the correct fields of the @dataclass in the configs/corpus_config.py
                         target_fields=['hu_prompt', 'hu_text'],   # The data fields to be translated (The fields belong to CorpusConfig)

                         do_translate=True,
                         no_translated_code=False,
                         target_lang="hu",
                         source_lang="en",)

    # Read function must assign data that has been read to self.data_read
    def read(self, path_to_dataset: str) -> None:
        # The read function must call the read function in DataParser class
        # I just want to be sure that the file path is correct
        super(DefaultParser, self).read()

        #self.data_read = load_dataset("BeIR/fiqa", 'corpus', split='corpus')
        self.data_read = load_from_disk(path_to_dataset)
        return None

    # Convert function must assign data that has been converted to self.converted_data
    def convert(self) -> None:
        # The convert function must call the convert function in DataParser class
        # I just want to be sure the read function has actually assigned the self.data_read
        super(DefaultParser, self).convert()

        data_converted = []
        for data in tqdm(self.data_read, desc=f"Converting data"):
            data_dict = {}

            # The DataParser class has an id_generator method which can create random id for you
            data_dict['qas_id'] = self.id_generator()

            data_dict['id'] = 0
            data_dict['hu_prompt'] = data['prompt']
            data_dict['hu_text'] = data['text']
            
            data_dict['corpus_lengths'] = None
            data_converted.append(data_dict)

        # Be sure to assign the final data list to self.converted_data
        self.converted_data = data_converted

        return None


if __name__ == '__main__':

    # Create an argument parser object
    parser = argparse.ArgumentParser()
    parser.add_argument('path_to_dataset', help = 'Path to the dataset object.') # Add 'path_to_dataset' argument
    parser.add_argument('dataset_to_save', help = 'Path of the folder to save the translated dataset.') # Folder to save the translated dataset
    parser.add_argument('dataset_name', help = 'Name of the dataset.')
    args = parser.parse_args()

    PARSER_NAME = args.dataset_name
    
    default_parser = DefaultParser(r"examples/Fiqa/dummy.txt", args.dataset_to_save)
    default_parser.read(args.path_to_dataset)
    default_parser.convert()

    print(f'Saving: {args.dataset_name}_translated_hu.json')
    default_parser.save
