import time
import requests
import json
from tqdm import tqdm


class VkUser:
    url = 'https://api.vk.com/method/'
    def __init__(self, access_token, user_id, version):
       self.token = access_token
       self.id = user_id
       self.version = version
       self.params = {'access_token': self.token, 'v': self.version}

    def users_info(self):
       url = 'https://api.vk.com/method/users.get'
       params = {'user_ids': self.id}
       response = requests.get(url, params={**self.params, **params})
       return response.json()
 
    def get_photos(self): 
        photos_get_url = 'https://api.vk.com/method/photos.get' 
        params = {
            'owner_id' : user_id,
            'album_id' : profile,            
            'rev' : 0,
            'extended' : 1            
        }
        res = requests.get(photos_get_url, params={**self.params, **params}).json()['response']['items']
        return(res)

    def heights_photos(self):        
        fotos_dict = {} 
        foto_list = []       
        foto_inf = self.get_photos()        
        for a in foto_inf:            
            names = a['likes']['count']
            res2 = a['sizes']
            heights = []           
            for b in res2:                                              
                heights.append(b['height'])
                max_height = sorted(heights)[-1]
            for b in res2:
                if max_height == b['height']:
                    url_photo = b['url']                 
            foto = {
                'file_name' : names,
                'size' : max_height,
                'url_photo' : url_photo
            }
            foto_list.append(foto)                
        return(foto_list)
    
   
         
class YaUploader:
    def __init__(self, token: str):
        self.token = token

        
    def get_headers(self):
        return {
            'Content-Type': 'application/json',
            'Authorization': 'OAuth {}'.format(self.token)
        }

   
    def upload1(self, cikl = 5):        
        cikl_n = 0
        foto_list = []
        for a in tqdm(vk.heights_photos()):
            time.sleep(1)
            if cikl_n != cikl:
                upload_url = "https://cloud-api.yandex.net/v1/disk/resources/upload"
                headers = self.get_headers()
                params = {}
                params = {
                'url' : a['url_photo'],       
                'path' : a['file_name']
                }
                response = requests.post(upload_url, headers=headers, params = params)
                time.sleep(0.3)
                cikl_n += 1
                foto_info = {
                    "file_name": a['file_name'],
                    "size": a['size']                   
                }
                foto_list.append(foto_info) 

        with open("data.json","w") as write_file: 
                json.dump(foto_list,write_file)                                             
        print("Загрузка файлов выполнена")


  



if __name__ == '__main__': 
    access_token = ''
    version = '5.131'
    cikl = 5
    user_id = input('Введите id пользователя VK: ')
    profile = input('Введите номер альбома VK: ')
    token = input('Введите токен с Полигона Яндекс.Диска: ') 
    vk = VkUser(access_token, user_id, version)       
    uploader = YaUploader(token)     
    result = uploader.upload1(cikl)