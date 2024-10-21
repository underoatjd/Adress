import pytesseract
import cv2

# Ruta al ejecutable de Tesseract
pytesseract.pytesseract.tesseract_cmd = r'D:/Tesseract/tesseract.exe'

# Cargar imagen del captcha
image = cv2.imread(r"F:/Descargas/Descargas/SELENIUM CURSO/ADRESS/Adress/images/991.png")

if image is None:
    print("No se pudo cargar la imagen.")
    exit()

# Convertir a escala de grises
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Aplicar filtro de afilado para mejorar los bordes
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
sharp = cv2.filter2D(gray, -1, kernel)

# Aplicar un umbral inverso
_, thresh = cv2.threshold(sharp, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

# Mostrar la imagen procesada
cv2.imshow("Imagen procesada", thresh)
cv2.waitKey(0)
cv2.destroyAllWindows()

# Usar OCR para extraer texto
extracted_text = pytesseract.image_to_string(thresh, config='--psm 6 -c tessedit_char_whitelist=0123456789')
print(f'Texto extraído: {extracted_text}')


