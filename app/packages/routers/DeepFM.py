import pandas as pd
import torch
import numpy as np
from deepctr_torch.inputs import SparseFeat, get_feature_names
import pickle
from collections import Counter

class DeepFM:
    def __init__(self):

        self.all_genre_list = ['Adventure', 'Disaster', 'Martial Arts', 'Military Action', 'Spy and Espionage',
                    'Superhero', 'Video game movies', 'Action comedy', 'Action crime', 'Action drama',
                    'Action-horror', 'Action thriller', 'Docudrama', 'Melodrama', 'Teen drama', 'Medical drama',
                    'Legal drama', 'Religious drama', 'Sports drama', 'Political drama', 'Anthropological drama',
                    'Philosophical drama', 'Contemporary and urban fantasy', 'Epic Fantasy', 'Fairy Tale', 'Dark Fantasy',
                        'Ghost', 'Zombie', 'Werewolf', 'Vampire', 'Monster', 'Slasher', 'Splatter and Gore', 'Body Horror',
                        'Folk Horror', 'Occult', 'Found Footage', 'Outbreak', 'Historical romance', 'Regency romance', 'Romantic drama',
                        'Romantic comedy', 'Chick Flick', 'Fantasy romance', 'Space Opera or epic sci-fi', 'Utopia', 'Dystopia', 'Contemporary Sci-Fi',
                        'Cyberpunk', 'Steampunk', 'Psychological thriller', 'Mystery', 'Film noir']
        
        self.sparse_features = ["subsr", 'content_id', "ct_cl", "genre_of_ct_cl"] 

        with open('app/resources/content_id_template.pkl', 'rb') as file:
            self.content_id_template = pickle.load(file)
            
    
    def load_model(self):
        model = torch.load('app/resources/DeepFM_epoch_1206.h5')

        return model
  

    def load_label_encoder(self):
        label_encoders = torch.load('app/resources/label_encoders_1206.pth')

        return label_encoders
  

    # 53 개의 컬럼을 원핫인코딩 template_A : ['words1','words2',,,] -> | words1 | words2 | ,,, 
    def MakeModelDataSet2(self, request_request_data: pd.DataFrame) -> pd.DataFrame:

        genre_request_data = pd.DataFrame(0, index = request_request_data.index, columns=self.all_genre_list)

        templates = request_request_data[['template_A_TopGroup', 'template_B_TopGroup', 'template_C_TopGroup']].apply(lambda row: list(set(item for sublist in row.dropna() 
                                                                                                                                 for item in sublist)), axis=1)

        for genre in self.all_genre_list:
            genre_request_data[genre] = templates.apply(lambda x: 1 if genre in x else 0)

        request_request_data.drop(columns=['template_A_TopGroup', 'template_B_TopGroup', 'template_C_TopGroup'], inplace=True)
        
        returned_request_data = pd.concat([request_request_data, genre_request_data], axis=1)
        
        return returned_request_data


    def prcs_Model_Input(self, prcsed_data: pd.DataFrame) -> dict:

        label_encoder = self.load_label_encoder()

        for feat, lbe in label_encoder.items():
            prcsed_data[feat] = lbe.transform(prcsed_data[feat])

        sparse_features = self.sparse_features + self.all_genre_list

        fixlen_feature_columns = [SparseFeat(feat, prcsed_data[feat].nunique())
                                    for feat in sparse_features]

        linear_feature_columns = fixlen_feature_columns

        dnn_feature_columns = fixlen_feature_columns

        feature_names = get_feature_names(linear_feature_columns + dnn_feature_columns)
        prcsed_model_input = {name: prcsed_data[name] for name in feature_names}

        return prcsed_model_input


    def predict2rs_list(self, request_data: pd.DataFrame, model_input_data: dict) -> list:

        model = self.load_model()

        pred_ans = model.predict(model_input_data,batch_size=256)
        
        pred_ans_avg = pred_ans.sum()/len(pred_ans)

        threshold = pred_ans_avg
        pred_labels = (pred_ans > threshold).astype(int)

        request_data['pred_ans'] = pred_ans
        request_data['pred_labels'] = pred_labels

        temp_dic_list = [
            {'content_id': request_data.loc[idx, 'content_id'], 'pred_ans': request_data.loc[idx, 'pred_ans'], 'pred_labels': request_data.loc[idx, 'pred_labels']}
            for idx in range(len(request_data))
        ]
        pred_dic_list_sorted = sorted(temp_dic_list, key=lambda elm: elm['pred_ans'], reverse=True)

        recommend_list = [str(item['content_id']) for item in pred_dic_list_sorted if item['pred_labels'] == 1]

        recommend_list = recommend_list[:21]

        return recommend_list

    def extract_template_word_list(self, recommended_content_ids: list):
        word_list = []
        
        for content_id in recommended_content_ids:
            content_id = int(content_id)
            template_words = self.content_id_template.get(content_id)
            if not pd.isna(template_words):
                word_list.extend(template_words.split(', '))
            else:
                continue

        word_count = Counter(word_list)

        duplicate_words = {word: count for word, count in word_count.items() if count > 1}

        sorted_duplicate_words = dict(sorted(duplicate_words.items(), key=lambda item: item[1], reverse=True))

        top_three_duplicates = list(sorted_duplicate_words.keys())[:3]
        top_three_str = ', '.join(top_three_duplicates)
        return top_three_str



    def get_request_data_2_Rs(self, request_data: dict) -> list:

        request_request_data_personal_data_request_data = pd.DataFrame([vars(item) for item in request_data])
        
        prcsed_data = self.MakeModelDataSet2(request_request_data = request_request_data_personal_data_request_data)

        prcsed_model_input = self.prcs_Model_Input(prcsed_data = prcsed_data)

        recommed_content_id_list = self.predict2rs_list(request_data = request_request_data_personal_data_request_data,
                                                        model_input_data = prcsed_model_input)
        
        top_content_id = self.extract_template_word_list(recommed_content_id_list)

        recommed_content_id_list.insert(0, top_content_id)

        return recommed_content_id_list