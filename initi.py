from add_feature import save_feature

with open('./test.jpeg', 'rb') as f:
    img = f.read()
save_feature(img, str(2))

from search_image import search

with open('./test.jpeg', 'rb') as f:
    res = search(f.read(), 10)
    # print(int(float(res[0])))