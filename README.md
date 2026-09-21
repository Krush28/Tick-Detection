# AI-Based Tick Mark Detection & Form Processing

## Overview

This project is an AI-based document processing system designed to automatically detect tick marks in structured forms and associate them with their corresponding options.

Traditional OCR-based approaches struggle with forms containing multiple selectable options such as:

* YES / NO
* VEG / NON-VEG
* MED / LARGE / XL / XXL
* Multiple-option fields
* Forms containing many fields and checkboxes

To address this, the project uses a combination of **YOLO-based object detection** and **PaddleOCR-based text extraction**.

## Architecture

```text
Input Document/Image
        │
        ▼
   YOLO Detection
        │
        ▼
   Tick Detection
        │
        ▼
  Tick Centroids
        │
        ▼
    Row Grouping
        │
        ├───────────────┐
        │               │
        ▼               ▼
   PaddleOCR       OCR Text
        │               │
        └───────┬───────┘
                ▼
       Spatial Matching
                │
                ▼
      Selected Option
                │
                ▼
      Structured Output
```

## Technologies Used

* **Python**
* **YOLO / Ultralytics** – Tick-mark detection
* **PaddleOCR** – Text detection and recognition
* **OpenCV** – Image processing and visualization
* **NumPy** – Coordinate and numerical processing

## Current Pipeline

### 1. Tick Detection

A custom-trained YOLO model detects tick marks in the document.

For every detected tick, the system calculates its centroid:

```text
(cx, cy)
```

These coordinates provide the spatial location of each selection.

### 2. Row Grouping

Detected tick centroids are sorted according to their Y-coordinate and grouped into rows.

This allows the system to understand the spatial structure of the form.

### 3. OCR Processing

PaddleOCR extracts text and corresponding coordinates from the document.

Example:

```text
YES     → (3600, 1787)
NO      → (3829, 1787)
```

### 4. Spatial Matching

The detected tick coordinates are compared with OCR coordinates to determine which option the tick is associated with.

The system uses spatial relationships such as:

* Y-coordinate proximity
* X-coordinate proximity
* Row relationships
* OCR text filtering

## Example

For a field such as:

```text
Boiler Suit Size:

MED     LARGE     XL     XXL
                  ✓
```

the system attempts to determine that:

```text
Selected Option → XL
```

Similarly:

```text
YES     NO
 ✓
```

can produce:

```text
Selected Option → YES
```

## Project Status

The YOLO tick-detection pipeline and PaddleOCR text-coordinate extraction are implemented.

The current development focus is improving the spatial matching logic so that the system can reliably associate detected ticks with their corresponding options across different form layouts.

## Future Improvements

* Improve tick detection recall
* Detect selectable option regions
* Improve OCR-based option extraction
* Handle multi-column forms
* Improve field-to-option association
* Support multiple document templates
* Generate structured JSON output
* Process multiple pages automatically
* Improve robustness to different resolutions and document layouts

## Goal

The ultimate goal is to build a reliable automated document-processing pipeline capable of converting scanned forms into structured digital data while minimizing manual data entry.
