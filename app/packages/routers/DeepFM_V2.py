# import pandas as pd
# import torch
# import numpy as np
# import ast

# from sklearn.metrics import accuracy_score
# from sklearn.model_selection import train_test_split
# from sklearn.preprocessing import LabelEncoder, MinMaxScaler

# from deepctr_torch.inputs import SparseFeat, get_feature_names
# from deepctr_torch.models import DeepFM

# class DeepFM:


#   def __init__(self):

#     self.all_genre_list = ['Adventure', 'Disaster', 'Martial Arts', 'Military Action', 'Spy and Espionage',
#                   'Superhero', 'Video game movies', 'Action comedy', 'Action crime', 'Action drama',
#                   'Action-horror', 'Action thriller', 'Docudrama', 'Melodrama', 'Teen drama', 'Medical drama',
#                   'Legal drama', 'Religious drama', 'Sports drama', 'Political drama', 'Anthropological drama',
#                   'Philosophical drama', 'Contemporary and urban fantasy', 'Epic Fantasy', 'Fairy Tale', 'Dark Fantasy',
#                     'Ghost', 'Zombie', 'Werewolf', 'Vampire', 'Monster', 'Slasher', 'Splatter and Gore', 'Body Horror',
#                     'Folk Horror', 'Occult', 'Found Footage', 'Outbreak', 'Historical romance', 'Regency romance', 'Romantic drama',
#                     'Romantic comedy', 'Chick Flick', 'Fantasy romance', 'Space Opera or epic sci-fi', 'Utopia', 'Dystopia', 'Contemporary Sci-Fi',
#                       'Cyberpunk', 'Steampunk', 'Psychological thriller', 'Mystery', 'Film noir']
    
#     self.sparse_features = ["subsr", 'content_id', "ct_cl", "genre_of_ct_cl"] 

    
#   # Load 
#   def load_model(self):
#      model = torch.load('resource/DeepFM.h5')
#      return model
  
#   def load_label_encoder(self):
#      label_encoders = torch.load('resuorce/label_encoders_1202.pth')
#      return label_encoders



#     # [선택] np.NaN -> None 변경
#   def prcs_NaN2None(df:pd.DataFrame) -> pd.DataFrame:
#     return_df = df.replace({np.NaN:None})
#     return return_df

#     # 53 개의 컬럼을 원핫인코딩 template_A : ['words1','words2',,,] -> | words1 | words2 | ,,, 
#   def prcs_MakeModelDataSet(self,user: pd.DataFrame) -> pd.DataFrame:
#       # Create a DataFrame with zeros for the genres
#       genre_df = pd.DataFrame(0, index=user.index, columns=self.all_genre_list)

#       templates = user[['template_A_TopGroup', 'template_B_TopGroup', 'template_C_TopGroup']].apply(lambda row: list(set(item for sublist in row.dropna() for item in sublist)), axis=1)

#       # Update the genre_df using vectorized operations with tqdm
#       for genre in self.all_genre_list:
#           genre_df[genre] = templates.apply(lambda x: 1 if genre in x else 0)


#       # Drop unnecessary columns
#       user.drop(columns=['template_A_TopGroup', 'template_B_TopGroup', 'template_C_TopGroup'], inplace=True)

#       returned_df = pd.concat([user,genre_df],axis=1)

#       return returned_df
  


#   def prcs_Model_Input(self,prcsed_data) -> dict:
# # 전처리 1. 범주형 변수 인코딩 : 원핫 인코딩된, 칼럼들이 들어가야한다.
#     label_encoder = self.load_label_encoder()

#     for feat, lbe in label_encoder.items():
#         prcsed_data[feat] = lbe.transform(prcsed_data[feat])

#     sparse_features = self.sparse_features + self.all_genre_list

#     fixlen_feature_columns = [SparseFeat(feat, prcsed_data[feat].nunique())
#                               for feat in sparse_features]

#     # DeepFM linear_feature 설정
#     linear_feature_columns = fixlen_feature_columns
#         # DeepFM dnn_feature 설정
#     dnn_feature_columns = fixlen_feature_columns


#     feature_names = get_feature_names(linear_feature_columns + dnn_feature_columns)

#     prcsed_model_input = {name: prcsed_data[name] for name in feature_names}

#     return prcsed_model_input


# # -------------------------------------------------------------------------------------------------------


# # Predict, 전체 컨텐츠에 대해서, predicted_liked 가 1인 것을 예측하고,
# # predicted_liked가 1인 content_id를 리턴한다.
# def predict2rs_list(self,request_data,model_input_data) -> list[int]:
#   model = self.load_model()

#   pred_ans = model.predict(model_input_data,batch_size=256)
#   pred_labels = (pred_ans > 0.2).astype(int)

#   # Recommend List
#  # 전체 컨텐츠에 대한 딕셔너리를 만들고
#   total_list = dict(zip(request_data['content_id'],pred_labels))
#   # predicted_liked가 1인 content_id만 추출하기.
#   recommend_list =  [ key for key, value in total_list.items() if value == 1]

#   return recommend_list




# # -------------------------------------------------------------------------------------------------------


# def get_request_data_2_Rs(self,request_data) -> list[int]:
#   # TODO BE로 부터 받는 데이터 넣기


#   prcsed_data = self.prcs_MakeModelDataSet(request_data = request_data)

#   prcsed_model_input = self.prcs_Model_Input(prcsed_data = prcsed_data)

#   recommed_content_id_list = self.predict2rs_list(request_data=request_data,
#                                                   model_input_data=prcsed_model_input)

#   return recommed_content_id_list.astype(str)