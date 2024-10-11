import cv2
import pytesseract
import re
import pandas as pd

# Öğrenci isimlerini dosyadan oku
with open('students.txt', 'r', encoding='utf-8') as file:
    names = [line.strip() for line in file.readlines()]

# Kamerayı aç
cap = cv2.VideoCapture(0)

# Kamera çözünürlüğünü düşür (640x480 önerilir)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# Tanımak istediğin regex formatı: S-###-###-####
pattern = r'[A-Z]-\d{3}-\d{3}-\d{4}'

# Daha önce okunan kodları saklamak için bir set
recognized_codes = set()

assignments = []  # Kod ve isim eşleştirmeleri
current_index = 0  # İsimlerin indeksini takip et

while True:
    # Her döngüde yeni bir kare al
    ret, frame = cap.read()

    # Eğer kare başarıyla alındıysa
    if ret:
        # OCR işlemi yap
        text = pytesseract.image_to_string(frame)

        # Regex ile formata uyan metinleri bul
        matches = re.findall(pattern, text)

        # Eğer formata uyan metin bulunduysa
        for match in matches:
            if match not in recognized_codes:  # Daha önce kaydedilmediyse
                print("Tanımlanan metin:", match)

                # Metni dosyaya kaydet
                with open("recognized_text.txt", "a", encoding='utf-8') as file:
                    file.write(match + "\n")

                # Tanınan kodu sete ekle
                recognized_codes.add(match)

                # İsim ile kodu eşleştir
                if current_index < len(names):  # İsimler tükenmemişse
                    assignments.append((names[current_index], match))
                    current_index += 1  # İndeksi artır

                # İstenilen sayıda kod okunduysa döngüden çık
                if current_index >= len(names):
                    print("Tüm kodlar okundu.")
                    break

        # Kamera görüntüsünü ekranda göster
        cv2.imshow('Camera Feed', frame)

        # 'q' tuşuna basılınca döngüden çık
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Tüm kodlar okunduysa döngüyü kır
    if current_index >= len(names):
        break

# Kamera ve pencereleri serbest bırak
cap.release()
cv2.destroyAllWindows()

# Eğer eşleştirme yapıldıysa DataFrame oluştur
if assignments:
    df = pd.DataFrame(assignments, columns=['İsim', 'Kod'])

    # Excel dosyasına kaydet
    df.to_excel('ogrenci_kodlari.xlsx', index=False)
    print("Excel dosyası oluşturuldu: ogrenci_kodlari.xlsx")
else:
    print("Hiçbir kod okunamadı, Excel dosyası oluşturulamadı.")
