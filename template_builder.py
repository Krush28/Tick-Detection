from paddleocr import PaddleOCR

ocr = PaddleOCR(
    use_doc_orientation_classify=False,
    use_doc_unwarping=False,
    use_textline_orientation=False,
    lang="en"
)

image_path = "/Users/jagadeesh/Downloads/IMG_20260804_154219.jpg"

results = ocr.predict(image_path)

ocr_data = []

for page in results:

    texts = page["rec_texts"]
    boxes = page["rec_boxes"]

    for text, box in zip(texts, boxes):

        x, y, w, h = box

        cx = x + w // 2
        cy = y + h // 2

        ocr_data.append({
            "text": text,
            "center": (int(cx), int(cy))
        })

print(ocr_data[:5])

IGNORE = [

    "DATE",
    "PASSPORT",
    "ADDRESS",
    "WORLD",
    "GMOS",
    "EMAIL",
    "NAME",
    "SIGNATURE"

]

filtered = []

for item in ocr_data:

    keep = True

    for word in IGNORE:

        if word.lower() in item["text"].lower():

            keep = False
            break

    if keep:
        filtered.append(item)

