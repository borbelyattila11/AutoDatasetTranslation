import sys, argparse

from tqdm.auto import tqdm
from datasets import load_dataset, load_from_disk

from configs import DefaultConfig
from translator import DataParser

class DefaultParser(DataParser):
    def __init__(self, file_path: str, output_path: str, file_name: str = 'default_parser'):
        super().__init__(file_path,
                         output_path,
                         parser_name = file_name,
                         target_config = DefaultConfig,
                         target_fields = [ 'hu_caps' ], # The data fields to be translated
                         do_translate = True,
                         no_translated_code = False,
                         target_lang = 'hu', # Target language
                         source_lang = 'en') # Source language

    def read(self, path_to_dataset: str) -> None:
        super(DefaultParser, self).read()

        self.data_read = load_dataset(path_to_dataset)

    def convert(self) -> None:
        super(DefaultParser, self).convert()

        data_converted = []
        for data in tqdm(self.data_read, desc = f'Converting data'):
            data_dict = {}

            # Generate unique id for each entry
            data_dict['qas_id'] = self.id_generator()

            # We just need to have an integer id, it doesn't matter the value.
            data_dict['id'] = 0
            data_dict['urls'] = data['url']
            data_dict['en_caps'] = data['caption']
            data_dict['hu_caps'] = data['caption']
            
            data_dict['corpus_lengths'] = None
            data_converted.append(data_dict)

        self.converted_data = data_converted

if __name__ == '__main__':

    # Create an argument parser object
    parser = argparse.ArgumentParser()
    parser.add_argument('path_to_dataset', help = 'Path to the dataset object.') # Add 'path_to_dataset' argument
    parser.add_argument('dataset_to_save', help = 'Path of the folder to save the translated dataset.') # Folder to save the translated dataset
    parser.add_argument('dataset_name', help = 'Name of the dataset.')
    args = parser.parse_args()
    
    # Create the dataset parser instance
    dataset_parser = DefaultParser(r'scripts/dummy.txt', args.dataset_to_save, parser_name = args.dataset_name)
    
    # Read the dataset
    dataset_parser.read(args.path_to_dataset)

    # Translate the data
    dataset_parser.convert()

    # Save the dataset
    dataset_parser.save
