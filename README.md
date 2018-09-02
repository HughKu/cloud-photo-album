# Cloud-photo-album
A demo photo album featuring search by image using deep feature learning.

Note: Due to cost, this website is no longer served online and I need to host another on-going project.

# Demo Video


# Features
## Auto-labeling when uploading images
![upload](asset/upload.png)
## Search by Text
![search-by-text](asset/search_by_text.png)
## Search by Image
![search-by-image](asset/search_by_image.png)

# Install and Run
1. Get off-the-shelf dependencies 
```shell
pip install -r requirements.txt
```
2. Get customed caffe python wrapper for deep retrieval
```shell
git clone https://github.com/HughKu/caffe-retrieval.git
```
3. Run Django Server
```shell
cd my_website
python manage.py runserver 8002
```
4. Open web browser and enter the following URL 
```HTML
http://localhost:8002/work/photo-album-alpha/
```

# Server Structure
* [Model Overview](#model-overview)
    * [Introduction](#introduction)
    * [Architecture](#architecture)
* [Requirement](#getting-started)
    * [Install](#install-required-packages)
    * [Get Pre-trained Model](#get-pre-trained-model)
* [Generating Captions](#generating-captions)
* [Issue](#encoutering-issue)
