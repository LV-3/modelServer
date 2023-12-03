import pandas as pd
import torch
import numpy as np
import ast

from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, MinMaxScaler

from deepctr_torch.inputs import SparseFeat, get_feature_names
from deepctr_torch.models import DeepFM

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
        self.all_genre_dic = {genre: 0 for genre in self.all_genre_list}
        self.sparse_features = ["subsr",'content_id',"ct_cl", "genre_of_ct_cl"] + self.all_genre_list
        self.target = ['liked']
        self.test_user_09 = pd.read_pickle('resource/test_deepfm_data_1129.pickle')
        self.df_test_user_09 = pd.DataFrame(self.test_user_09)
    

    def prcs_nan_parse_template(self, DF: pd.DataFrame) -> pd.DataFrame:
        DF.replace({np.NaN:None},inplace=True)

        template_list = ['template_A','template_B','template_C']

        for template in template_list:
            DF[template] = DF[template].apply(lambda x: ast.literal_eval(x) if x is not None else None)
        return DF
            

    def prcs_template_cols(self, total_data:pd.DataFrame, user:pd. DataFrame) -> pd.DataFrame:
        total_data['template_group_words'] = None
        total_data['is_prefer_content'] = False
        total_data.loc[total_data['content_id'].isin(user['content_id']), 'is_prefer_content'] = True
        
        for idx in range(len(total_data)):
            all_genre_dic = {genre: 0 for genre in self.all_genre_list}

            if not total_data.loc[idx, 'is_prefer_content']:
                total_data.at[idx, 'template_group_words'] = all_genre_dic
                continue
            
            template_A = total_data.loc[idx, 'template_A']
            template_B = total_data.loc[idx, 'template_B']
            template_C = total_data.loc[idx, 'template_C']

            if template_A is not None:
                for elm in template_A:
                    if elm in all_genre_dic:
                        all_genre_dic[elm] = 1

            if template_B is not None:
                for elm in template_B:
                    if elm in all_genre_dic:
                        all_genre_dic[elm] = 1

            if template_C is not None:
                for elm in template_C:
                    if elm in all_genre_dic:
                        all_genre_dic[elm] = 1

            total_data.at[idx, 'template_group_words'] = all_genre_dic
        # 딕셔너리의 키값을 통해, 데이터프레임에 새로운 칼럼을 만들고

        for col in all_genre_dic:
            total_data[col] = 0

        # 딕셔너리의 키값을 새로운 칼럼에 값을 할당한다.
        for idx,row in total_data.iterrows():
            template_group_words = row['template_group_words']
            for genre, value in template_group_words.items():
                total_data.at[idx,genre] = template_group_words.get(genre, 0)

        total_data.drop(columns=['template_A','template_B','template_C','template_group_words', 'is_prefer_content'],inplace=True)

        return total_data


    def load_model(self):
        model = torch.load('resource/DeepFM.h5')

        return model


    def get_request_data(self, request_data):

        # 요청된 사용자의 선호 컨텐츠
        user_personal_data_df = pd.DataFrame([vars(item) for item in request_data])
        personal_data_df = self.df_test_user_09

        user_subsr = user_personal_data_df['subsr'][0]
        personal_data_df['subsr'] = user_subsr

        # prcsed_nan_sparse_data = self.prcs_nan_parse_template(personal_data_df)

        # # regex2 유저 컨텐츠
        prcsed_templates_cols_data = self.prcs_template_cols(personal_data_df, user_personal_data_df)

        model = self.load_model()
        inf_data = self.prcs_sparse_fts_get_names(prcsed_templates_cols_data, user_subsr)

        # print(type(inf_data))
        # print(inf_data)

        pred_ratio = model.predict(inf_data, batch_size=256)

        # print(pred_ratio)

        # # # liked 컬럼은 user_preference가 30%(백분율) 이상
        # # # threshold를 조절하면 recommend_list 개수를 조절할 수 있다. (많이 뽑고 21개로)
        # threshold = 0.5

        # pred_labels = (pred_ratio > threshold).astype(int)

        # # 추천되어야 할 컨텐츠들의 리스트 (9월 전체 vod 리스트)
        # result_df = recommend_test_user_09[['subsr', 'content_id', 'liked']].copy()

        # print(result_df)
        # result_df['predicted_liked'] = pred_labels
        # result_df['predicted_rate'] = pred_ratio
        # result_df.reset_index(drop=True,inplace=True)

        # print(result_df)

        # recommend_content_id = result_df[result_df['predicted_liked']==1]['content_id'].tolist()
        
        # return recommend_content_id
    

    def prcs_sparse_fts_get_names(self, query: pd.DataFrame, append_subsr):

        # 자바 스프링부트에서 받은 데이터가 들어온다.
        new_data_drop_target_col = query.copy()

        new_data_drop_target_col['subsr'] = append_subsr

        for feat in self.sparse_features:
            lbe = LabelEncoder()
            new_data_drop_target_col[feat] = lbe.fit_transform(new_data_drop_target_col[feat])

        fixlen_feature_columns = [SparseFeat(feat, new_data_drop_target_col[feat].nunique())
                                for feat in self.sparse_features]

        linear_feature_columns = fixlen_feature_columns

        dnn_feature_columns = fixlen_feature_columns

        feature_names = get_feature_names(linear_feature_columns + dnn_feature_columns)

        # Prepare input data for the model
        new_model_input = {name: new_data_drop_target_col[name] for name in feature_names}

        return new_model_input
        



