import os.path
import wave
import pandas as pd
import os.path
from collections import defaultdict


DATA_PATH = os.path.normpath(os.path.join(os.getcwd(), '../Data'))
AUDIO_METADATA_PATH = os.path.join(DATA_PATH, 'audio_metadata.csv')


def create_info_csv_about_data(data_path=DATA_PATH, csv_path=AUDIO_METADATA_PATH):
    fns_dict = __get_filenames_dict(data_path)
    columns = ('dir', 'fn ', 'channels', 'sample_width', 'frame_rate',
               'n_frames', 'compression_type', 'compression_name')
    df = pd.DataFrame(columns=columns)
    for folder, files in fns_dict.items():
        print('Processing {} folder'.format(folder))
        for file in files:
            print('\tProcessing {} file'.format(file))
            full_fn = os.path.join(data_path, folder, file)
            with wave.open(full_fn) as wave_file:
                params = dict(zip(columns, (folder, file, *wave_file.getparams())))
                df = df.append(params, ignore_index=True)
    df.to_csv(csv_path, index=True)


# resulting hierarchy: {folder: list of filenames}
def __get_filenames_dict(data_path):
    result_dict = defaultdict(list)
    for folder in os.listdir(data_path):
        for file in os.listdir(os.path.join(data_path, folder)):
            result_dict[folder].append(file)
    return result_dict


if __name__ == '__main__':
    create_info_csv_about_data()