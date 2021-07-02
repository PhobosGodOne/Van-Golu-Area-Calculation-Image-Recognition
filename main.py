import cv2 as cv
import numpy as np



BGR = np.array([19, 7, 13])

# görseli alıyoruz
def read_image(path):
    return cv.imread(path)

# görsele treshold uyguluyoruz
def find_mask(image):
    #renk değerlerini daha alçak ve daha yüksek değerlere tolerans gösterecek şekilde gönderiyoruz.
    return cv.inRange(image, BGR-70, BGR + 70)


def find_contours(mask):
    ( cnts, hierarchy) = cv.findContours(mask.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

    return cnts

# contouru görüntülemek için bir fonksiyon kullanıyoruz
def show_contours(contours, image):
    cv.drawContours(image, contours, -1, (180, 50, 50), 2)

    cv.imshow("contours", image)


def get_main_contour(contours):
    copy = contours.copy()
    copy.sort(key=len, reverse=True)
    return copy[0]

if __name__ == "__main__":
    image = read_image("vangolu.png")

    mask = find_mask(image)

    #contour u bulup çiziyor ve gösteriyoruz.
    contours = find_contours(mask)
    main_contour = get_main_contour(contours)
    show_contours([main_contour], image)


    #pixel cinsinden toplam göl alanını buluyoruz
    area = cv.contourArea(main_contour)

    #resmin pixel cinsinden değerlerini opencv fonksiyonu ile buluyoruz
    wid = image.shape[1]
    hgt = image.shape[0]

    #areatotal = tüm resmin pixel cinsinden değeri
    areatotal = wid*hgt
    #percoflake = gölün tüm alana yüzdelik oranı
    percoflake = area/areatotal * 100

    #gerçek tüm boyutu elimizdeki verilere göre belirliyoruz
    totalarea = 230*250
    #elimizdeki yüzdelik değeri gerçek alana oranlayarak gerçek alanı tahmin etmeye çalışıyoruz
    areaoflake = totalarea*percoflake/100

    #van gölünün vikipedia' dan aldığım yüzölçümü
    vangolugercekalan = 3755

    #hata payını hesaplıyoruz.
    print("Hata payi = ", 100 - vangolugercekalan / areaoflake * 100)


    key = cv.waitKey(0)