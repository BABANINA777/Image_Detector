import numpy as np
import cv2
import os

#чистит папку temp_crops
def remove_objects():
    for root, dirs, files in os.walk('temp_crops'):
        for file in files:
            if file != '.gitkeep':
                os.remove(os.path.join(root, file))

#Принемает путь до картинки, выгружает в temp_crops пронумерованные картинки с объектами начальной картинки
def extract_objects(image_path):
    # Создание пути для картинки и проверка на сущьествование
    #path = os.path.join('images', 'test_image.png')

    img = cv2.imread(image_path, cv2.IMREAD_COLOR)

    if img is None:
        print("Ошибка: Изображение не найдено!")
        return

    # 1 часть: смена на серый и размытие
    grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    blur = cv2.GaussianBlur(grey, (9, 9), 0)

    # 2 часть: пороговая обработка
    ret, tresh = cv2.threshold(blur, 110, 255, cv2.THRESH_BINARY)

    # 3 часть: поиск границ
    edges = cv2.Canny(tresh, threshold1=100, threshold2=200)

    contours, hierarchy = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    print(contours)
    print(hierarchy)

    # 4 часть: визуализация(пункт для отладки)
    """
    image_with_contours = img.copy()
    cv2.drawContours(image_with_contours, contours, -1, (0, 255, 0), 3)
    
    # код для открытия картинки с контурами
    cv2.namedWindow("Found Contours", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Found Contours", 800, 600)
    cv2.imshow('Found Contours', image_with_contours)
    """
    #5 часть: заливка фона картинки белым цветом
    #заливка фона черным
    black_mask = np.zeros(img.shape[:2], dtype=np.uint8)#создание черного изображения

    cv2.drawContours(black_mask, contours, -1, (255, 255, 255), -1)# отрисовка на нем белых контуров

    black_phone_img = cv2.bitwise_and(img, img, mask=black_mask)# создане изображения с черным фоном

    # заливка фона белым
    mask_inv = cv2.bitwise_not(black_mask)# инвертированная маска

    white_background = np.ones(img.shape, dtype=np.uint8) * 255#белое изображение
    white_bg_without_objects = cv2.bitwise_and(white_background, white_background, mask=mask_inv)

    final_img = cv2.add(black_phone_img, white_bg_without_objects)#создание финального img

    # 6 часть: вырезка объектов из картинки
    saved_files = []
    count = 1

    for contour in contours:
        # ЗАЩИТА ОТ МУСОРА: Игнорируем слишком маленькие контуры (например пылинки)
        if cv2.contourArea(contour) < 500:
            continue

        x, y, w, h = cv2.boundingRect(contour)
        object = final_img[y:y+h, x:x+w]
        filename = os.path.join('temp_crops', f"object_{count}.jpg")

        cv2.imwrite(filename, object)
        saved_files.append(filename)
        count += 1


    """
    # код для открытия картинки
    cv2.namedWindow("Test", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Test", 800, 600)
    cv2.imshow('Test', final_img)

    # отрисовка контуров
    # cv2.imshow('Edges', edges)
    # cv2.imshow('Found Contours', image_with_contours)

    cv2.waitKey(0)
    cv2.destroyAllWindows()
    """

#Создание пути для картинки и проверка на сущьествование
path = os.path.join('images','test_image.png')

remove_objects()
extract_objects(path)