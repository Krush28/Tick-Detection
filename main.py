from ultralytics import YOLO
from paddleocr import PaddleOCR
import cv2
import math
IMAGE_PATH = "/Users/jagadeesh/Downloads/IMG_20260804_154219.jpg"

# Load trained model
model = YOLO("/Users/jagadeesh/Downloads/best-2.pt")

# Run inference
results = model.predict(
    source="/Users/jagadeesh/Downloads/IMG_20260804_154219.jpg",
    conf=0.1,
    save=True,
    show=True
)

tick_centroids = []

for result in results:

    for box in result.boxes:

        x1, y1, x2, y2 = box.xyxy[0]

        x1 = int(x1)
        y1 = int(y1)
        x2 = int(x2)
        y2 = int(y2)

        # Calculate centroid
        cx = (x1 + x2) // 2
        cy = (y1 + y2) // 2

        tick_centroids.append((cx, cy))

print("\nDetected Tick Centroids:\n")

for i, point in enumerate(tick_centroids):
    print(f"Tick {i+1}: {point}")

#this is to sorth the tick coordinates based on the y-coordinate(vertical position) of the centroid, so that we can process them in order from top to bottom.

tick_centroids.sort(key=lambda x: x[1])

print("\nSorted Tick Coordinates\n")

for point in tick_centroids:
    print(point)



#this is to dram every centroid

image = cv2.imread("/Users/jagadeesh/Downloads/IMG_20260804_154219.jpg")

for result in results:

    for box in result.boxes:

        x1, y1, x2, y2 = map(int, box.xyxy[0])

        cx = (x1 + x2) // 2
        cy = (y1 + y2) // 2

        cv2.rectangle(image, (x1,y1), (x2,y2), (0,255,0), 2)

        cv2.circle(image, (cx,cy), 5, (0,0,255), -1)

        cv2.putText(
            image,
            f"({cx},{cy})",
            (cx+5, cy),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.4,
            (255,0,0),
            1
        )

cv2.imshow("Ticks", image)
cv2.waitKey(0)
cv2.destroyAllWindows()

#save the coordinates
with open("tick_coordinates.txt", "w") as f:

    for i, point in enumerate(tick_centroids):

        f.write(f"Tick {i+1}: {point}\n")

#group into rows
ROW_THRESHOLD = 20

rows = []

current_row = []

for point in tick_centroids:

    if not current_row:
        current_row.append(point)
        continue

    # Compare with first point of current row
    if abs(point[1] - current_row[0][1]) <= ROW_THRESHOLD:
        current_row.append(point)

    else:
        rows.append(current_row)
        current_row = [point]

# Add last row
if current_row:
    rows.append(current_row)

#print the rows
for i, row in enumerate(rows):

    print(f"\nRow {i+1}")

    for point in row:
        print(point)

tick_row_info = []

for row in rows:

    avg_y = sum(point[1] for point in row) / len(row)

    tick_row_info.append({
        "avg_y": avg_y,
        "ticks": row
    })

print("\nTick Rows")

for i, row in enumerate(tick_row_info):

    print(f"\nTick Row {i+1}")

    print("Average Y :", row["avg_y"])

    print("Ticks :", row["ticks"])
    
ocr = PaddleOCR(
    use_doc_orientation_classify=False,
    use_doc_unwarping=False,
    use_textline_orientation=False,
    lang="en"
)


results = ocr.predict(IMAGE_PATH)

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
print("\nFiltered OCR Words\n")

for item in filtered:
    print(item["text"])

OCR_ROW_THRESHOLD = 25

ocr_rows = []

current_row = []

filtered.sort(key=lambda item: item["center"][1])
for item in filtered:

    if not current_row:
        current_row.append(item)
        continue

    if abs(item["center"][1] - current_row[0]["center"][1]) <= OCR_ROW_THRESHOLD:
        current_row.append(item)

    else:
        ocr_rows.append(current_row)
        current_row = [item]

if current_row:
    ocr_rows.append(current_row)

for row in ocr_rows:
    row.sort(key=lambda item: item["center"][0])
for i, row in enumerate(ocr_rows):

    print(f"\nOCR Row {i+1}")

    for word in row:

        print(word["text"], word["center"])

ocr_row_info = []

for row in ocr_rows:

    avg_y = sum(word["center"][1] for word in row) / len(row)

    ocr_row_info.append({

        "avg_y": avg_y,

        "words": row

    })

print("\nOCR Rows")

for i,row in enumerate(ocr_row_info):

    print(f"OCR Row {i+1} -> Avg Y = {row['avg_y']}")

def nearest_ocr_row(tick_avg_y):

    nearest = None

    minimum = float("inf")

    for row in ocr_row_info:

        distance = abs(tick_avg_y - row["avg_y"])

        if distance < minimum:

            minimum = distance

            nearest = row

    return nearest
SKIP_WORDS = {

    "NAME",
    "ADDRESS",
    "PASSPORT",
    "DATE",
    "NATIONALITY",
    "HEIGHT",
    "WEIGHT",
    "SIZE",
    "DETAILS",
    "PERSONAL",
    "PARTICULARS",
    "ISSUE",
    "EXPIRY"

}

def match_tick_row(tick_row, ocr_row):

    matches = []

    for tick in tick_row:

        tick_x = tick[0]

        nearest = None

        minimum = float("inf")

        for word in ocr_row["words"]:
            text=word["text"].strip().upper()
            if text in SKIP_WORDS:
                continue
            if ":" in text:
                continue
            if len(text)>15:
                continue
            if " " in text:
                continue
            word_x=word["center"][0]
            distance=abs(tick_x-word_x)
            if distance<minimum:
                minimum=distance
                nearest=word


        if nearest:

            matches.append({

                "tick": tick,

                "text": nearest["text"],

                "text_center": nearest["center"]

            })

    return matches
print("\n==============================")
print("MATCHING RESULTS")
print("==============================")


all_matches = []

print("\nFINAL MATCHING")
print("============================")

for tick_row in tick_row_info:

    matched_row = nearest_ocr_row(

        tick_row["avg_y"]

    )

    row_matches = match_tick_row(

        tick_row["ticks"],

        matched_row

    )

    all_matches.extend(row_matches)

    for match in row_matches:

        print(

            f"{match['tick']} ---> {match['text']}"

        )


image = cv2.imread(IMAGE_PATH)

for match in all_matches:

    tick = match["tick"]

    center = match["text_center"]

    text = match["text"]

    cv2.circle(image, tick, 7, (0,0,255), -1)

    cv2.circle(image, center, 7, (255,0,0), -1)

    cv2.line(image, tick, center, (0,255,0), 2)

    cv2.putText(

        image,

        text,

        (tick[0]+10, tick[1]),

        cv2.FONT_HERSHEY_SIMPLEX,

        0.6,

        (0,255,255),

        2

    )

cv2.imshow("Final Matching", image)

cv2.waitKey(0)

cv2.destroyAllWindows()
