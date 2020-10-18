from PIL import Image
import cv2


# 创建字典()
def build_dictionary():  # 字典的key是0-325 value是path 第0为白色 第1为黑色
    image_dict = {}
    for index in range(0, 325):
        path = r'./cut_all/' + str(index) + '.png'
        image_dict[index] = path
        index += 1
        # print(path,image_dict[path])
    return image_dict

# 判断该图片是否为正方形
def dispose(im):
    if (im.width == im.height):
        imageList = cutNine(im)
    else:
        new_im = fillSquare(im)
        imageList = cutNine(new_im)
    return save_images(imageList)

# 进行图片九等分
def cutNine(im):
    w = int(im.width / 3)
    boxList = []
    for i in range(0, 3):
        for j in range(0, 3):
            box = (j * w, i * w, (j + 1) * w, (i + 1) * w)
            boxList.append(box)
    imageList = [im.crop(box) for box in boxList]
    return imageList

# 进行图片填充
def fillSquare(im):
    w = im.width if im.width > im.height else im.height
    newImage = Image.new(im.mode, (w, w), color='white')
    if (im.width > im.height):
        newImage.paste(im, (0, int((w - im.height) / 2)))
    else:
        newImage.paste(im, (int((w - im.width) / 2, 0)))
    return newImage

# 完成切割
def save_images(imList):
    index = 0
    image_list = []
    for image in imList:
        image.save(r'./cut' + str(index) + '.png', 'png')
        image_list.append(r'./cut' + str(index) + '.png')
        index += 1
    return image_list

# 进行图片匹配
def compare_images(image_dict, image_list):
    image = {}
    image_nine = {}
    for im in image_list:
        img1 = cv2.imread(im)
        H1 = cv2.calcHist([img1], [1], None, [256], [0, 256])
        H1 = cv2.normalize(H1, H1, 0, 1, cv2.NORM_MINMAX, -1)
        for key in image_dict.keys():
            img2 = cv2.imread(image_dict[key])
            H2 = cv2.calcHist([img2], [1], None, [256], [0, 256])
            H2 = cv2.normalize(H2, H2, 0, 1, cv2.NORM_MINMAX, -1)
            sim = cv2.compareHist(H1, H2, 0)
            if (sim == 1.0):
                image[key] = im
                break
    # print(image)
    for i in image.keys():
        if (i > 1):
            break

    low = ((i-1) // 9) * 9 + 1  # 九张图的序号范围
    high = ((i-1) // 9) * 9 + 10

    for j in range(low, high):
        img = Image.open(image_dict[j])
        extrema = img.convert("L").getextrema()
        if (extrema == (0, 0)):

            break
    for i in image.keys():
        if i == 1:
            j = (j - 1) % 9 + 1
            image_nine[j] = image[1]
        elif i == 0:
            image_nine[0] = image[0]
        else:
            t = (i - 1) % 9 + 1
            image_nine[t] = image[i]
    # print(image_nine)
    return image_nine, (low - 1) // 9

# 将字典转为数字列表1-8+空白块
def tran_list(image_nine):
    for flag in range(1, 10):  # flag表示空白块的最终位置
        if flag not in image_nine.keys():
            break
    List = list(image_nine.keys())
    for i in range(0, 9):
        if (List[i] > flag):
            List[i] -= 1
    image_list = []
    print(List)
    if (len(List) % 3 == 0):
        for idx in range(0, 9, 3):
            image_list.append([List[idx], List[idx + 1], List[idx + 2]])
    target_list=[]
    for i in range(0,9):
        if i==(flag-1):
            target_list.append(0)
        elif i<(flag-1):
            target_list.append(i+1)
        else:
            target_list.append(i)
    target=[]
    if (len(target_list) % 3 == 0):
        for idx in range(0, 9, 3):
            target.append([target_list[idx], target_list[idx + 1], target_list[idx + 2]])
    return image_list, target,flag
