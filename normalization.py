import pandas as pd
from sklearn.preprocessing import LabelEncoder

def normalization(df, config):
    norm_df = df.copy()
    norm_df['Price'] = (
        norm_df['Price']
        .str.replace('€','')
        .str.replace('.','')
        .str.replace(',','.')
        .str.strip()
        .astype(float)
    )
    norm_df['Price'] = pd.to_numeric(norm_df['Price'], errors='coerce')

    norm_df['District'] = (
        norm_df['Address'].str.split(',')
        .str[0]
        .str.replace('Opština', '', regex=False)
        .str.strip()
        )

    norm_df['Squares'] = (
        norm_df['Squares']
        .str.replace('m2','')
        .str.replace(',','.')
        .str.replace('"','')
        .str.strip()
        .astype(float)
    )

    norm_df['Rooms'] = (
        norm_df['Rooms']
        .astype(str)
        .str.extract(r'(\d+[\.,]?\d*)', expand=False)
        .str.replace(',','.')
        .astype(float)

        )

    def parse_floor(floor_str):
        if pd.isna(floor_str):
            return None, None
        
        if '/' in floor_str:
            parts = floor_str.split('/')
            try:
            
                roman_to_int = {
                    'I': 1, 'II': 2, 'III': 3, 'IV': 4, 'V': 5,
                    'VI': 6, 'VII': 7, 'VIII': 8, 'IX': 9, 'X': 10,
                    'XI': 11, 'XII': 12, 'XIII': 13, 'XIV': 14, 'XV': 15,
                    'XVI': 16, 'XVII': 17, 'XVIII': 18, 'XIX': 19, 'XX': 20,
                    'XXI': 21
                }
                current_floor = roman_to_int.get(parts[0],None)
                total_floors = int(parts[1]) if parts[1].isdigit() else None
                return current_floor, total_floors
            except:
                return None, None
        elif floor_str in ['PR', 'VPR', 'PSUT']:
            return 1, None
        else:
            try:
                roman_to_int = {
                    'I': 1, 'II': 2, 'III': 3, 'IV': 4, 'V': 5,
                    'VI': 6, 'VII': 7, 'VIII': 8, 'IX': 9, 'X': 10,
                    'XI': 11, 'XII': 12, 'XIII': 13, 'XIV': 14, 'XV': 15,
                    'XVI': 16, 'XVII': 17, 'XVIII': 18, 'XIX': 19, 'XX': 20,
                    'XXI': 21
                }
                return roman_to_int.get(floor_str, None), None
            except:
                return None, None
    
    floor_data = norm_df['Floor'].apply(parse_floor)
    norm_df['Current_Floor'] = floor_data.apply(lambda x: x[0] if x else None)
    norm_df['Total_Floors'] = floor_data.apply(lambda x: x[1] if x else None)

    encoder = LabelEncoder()
    norm_df['District_encoded'] = encoder.fit_transform(norm_df['District'])

    norm_df = norm_df.drop(columns = 'Address')
    norm_df = norm_df.drop(columns = 'Floor')
    norm_df = norm_df.drop(columns = 'District')


    norm_df = norm_df.drop_duplicates()
    norm_df = norm_df.dropna()
    

    norm_df.to_csv(config.OUTPUT_NORM_PATH, index=False)

    return norm_df

if __name__ == '__main__':
    from config.private_config import ProdConfig
    config=ProdConfig()
        
    class NormTestConfig:
        #OUTPUT_NORM_PATH = 'test/test_normilized.csv'
        #OUTPUT_PARSER_PATH = "test/resultsTest.csv"
        OUTPUT_PARSER_PATH = config.OUTPUT_PARSER_PATH
        OUTPUT_NORM_PATH = config.OUTPUT_NORM_PATH

    norm_df = normalization(pd.read_csv(NormTestConfig.OUTPUT_PARSER_PATH), NormTestConfig)
    print(norm_df)
    norm_df.to_csv(NormTestConfig.OUTPUT_NORM_PATH, index=False)