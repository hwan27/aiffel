#import matplotlib.pyplot as plt
import face_recognition
import os
import numpy as np
from PIL import Image

img_path = './images/'
test_img = face_recognition.load_image_file(img_path + '강민경.jpg')

def get_gropped_face(img):
    # file_list = os.listdir(img_path)
    # for name in file_list:
        
    # print(file_list)
    image = img
    face_locations = face_recognition.face_locations(image)
    a, b, c, d = face_locations[0]
    cropped_face = image[a:c, d:b, :]
    # sample = Image.fromarray(cropped_face)
    # sample.show()
    
    return cropped_face

def get_face_embedding(face):
    return face_recognition.face_encodings(face)

#embedding = get_face_embedding(face)

def get_face_embedding_dict(dir_path):
    file_list = os.listdir(dir_path)
    embedding_dict = {}
    
    for file in file_list:
        img_path = os.path.join(dir_path, file)
        image = face_recognition.load_image_file(img_path)
        face_locations = face_recognition.face_locations(image)
        a, b, c, d = face_locations[0]
        cropped_face = image[a:c, d:b, :]
        embedding = get_face_embedding(cropped_face)
        if len(embedding) > 0:
            embedding_dict[os.path.splitext(file)[0]] = embedding[0]
    
    return embedding_dict

def get_face_embedding_byimg(img):

    face = get_gropped_face(img)
    embedding = get_face_embedding(face)

    #print(embedding)

    return embedding

def get_distance(img, name):
    
    embedding = get_face_embedding_byimg(img)

    return np.linalg.norm(embedding-embedding_dict[name], ord=2)

#embedding_dict = get_face_embedding_dict(dir_path)



def get_nearest_face_10(img, top=4):
    embedding_dict = get_face_embedding_dict('./images/')
    def get_sort_key_func(img):
        def get_distance_from_name1(name):
            embedding = get_face_embedding_byimg(img)
            return np.linalg.norm(embedding-embedding_dict[name], ord=2)

        return get_distance_from_name1
    sort_key_func = get_sort_key_func(img)
    sorted_faces = sorted(embedding_dict.items(), key=lambda x:sort_key_func(x[0]))

    _str = '{}, 거리: {}'.format(sorted_faces[0][0], sort_key_func(sorted_faces[0][0]))
    print(_str)
    
    # for i in range(top):
    #     if i == 0:continue
    #     if sorted_faces[i]:
    #         print('순위 {}: 이름({}), 거리({})'.format(i, sorted_faces[i][0], sort_key_func(sorted_faces[i][0])))
    #         _str = '{}, 거리: {}'.format(sorted_faces[i][0], sort_key_func(sorted_faces[i][0]))
    

    return _str

