from ultralytics import YOLO

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
import cv2

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

