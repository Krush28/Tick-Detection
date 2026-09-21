def find_nearest_text(tick, ocr_data):

    SEARCH_X = 300
    SEARCH_Y = 100

    tx, ty = tick

    nearest = None

    minimum = float("inf")

    for item in ocr_data:

        ox, oy = item["center"]

        if abs(tx-ox) > SEARCH_X:
            continue

        if abs(ty-oy) > SEARCH_Y:
            continue

        distance = abs(tx-ox)

        if distance < minimum:

            minimum = distance
            nearest = item

    return nearest
print("\n=============================")
print("FINAL MATCHING")
print("=============================\n")

for tick in tick_centroids:

    match = find_nearest_text(tick, filtered)

    if match:

        print(f"{tick}  --->  {match['text']}")

image = cv2.imread(IMAGE_PATH)

for tick in tick_centroids:

    match = find_nearest_text(tick, filtered)

    if match is None:
        continue

    text_center = match["center"]

    cv2.circle(image, tick, 6, (0,0,255), -1)

    cv2.circle(image, text_center, 6, (255,0,0), -1)

    cv2.line(image, tick, text_center, (0,255,0), 2)

    cv2.putText(
        image,
        match["text"],
        (tick[0]+5,tick[1]-5),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.5,
        (0,255,255),
        2
    )

cv2.imshow("Final Matching", image)
cv2.waitKey(0)
cv2.destroyAllWindows()