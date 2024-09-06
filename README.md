# Sign Language to Speech Conversion

This repository provides a solution for converting sign language gestures into spoken words. It leverages computer vision, machine learning, and media processing technologies to detect and recognize hand gestures corresponding to different letters of the alphabet, forming words that are then converted into speech.

## Tutorial
C:\Projects\SIH-Sign_to_Speech\Tutorial.png

## Table of Contents
- [Introduction](#introduction)
- [Features](#features)
- [Folder Structure](#folder-structure)
- [Installation](#installation)
- [Usage](#usage)
  - [Data Collection](#data-collection)
  - [Model Training](#model-training)
  - [Real-time Gesture Recognition](#real-time-gesture-recognition)
  - [Sign-to-Speech Conversion](#sign-to-speech-conversion)
- [Contributing](#contributing)
- [License](#license)

## Introduction
This project focuses on recognizing Indian Sign Language (ISL) alphabets using a computer webcam and converting them into text or spoken words. The application uses the MediaPipe library to process video input, extract hand landmarks, and predict gestures using a pre-trained model.

## Features
- **Real-time Gesture Detection:** Detects hand gestures from webcam input in real-time.
- **Alphabet Recognition:** Recognizes ISL letters A-Z.
- **Text-to-Speech Conversion:** Converts recognized letters into spoken words.
- **Custom Dataset Creation:** Allows users to collect their own gesture data and train the model.

## Folder Structure

```
models/
  ├── data3.pickle               # Preprocessed data in pickle format
  ├── model_final.p              # Pre-trained model file
.gitignore                       # Git ignore file
collect.py                       # Script to collect data for training
create_dataset.py                # Script to preprocess collected data
LICENSE                          # License file
live.py                          # Real-time gesture recognition script
README.md                        # ReadMe file (this document)
req.txt                          # List of required packages
Sign_to_Speech.py                # Main script for converting signs to speech
Tutorial.png                     # Image file for tutorial/reference
```

## Installation

1. **Clone the Repository:**

    ```bash
    git clone https://github.com/your-username/sign-to-speech.git
    cd sign-to-speech
    ```

2. **Install the Required Packages:**

    Make sure you have Python 3.x installed. Then, install the required packages:

    ```bash
    pip install -r req.txt
    ```

3. **Set Up MediaPipe and Other Dependencies:**

    Ensure `mediapipe`, `opencv-python`, and `pyttsx3` are properly installed in your environment.

## Usage

### 1. Data Collection

To collect data for training, run the `collect.py` script:

```bash
python collect.py
```

This script will use your webcam to capture images for each gesture class. Follow the on-screen instructions to collect data.

### 2. Model Training

Use the `create_dataset.py` script to preprocess the collected data and train your model.

```bash
python create_dataset.py
```

This script uses the MediaPipe library to extract hand landmarks from the collected images and stores the processed data in a pickle file (`data3.pickle`).

### 3. Real-time Gesture Recognition

To perform real-time gesture recognition, run the `live.py` script:

```bash
python live.py
```

This script captures frames from your webcam, processes them using the trained model, and displays the detected gesture on the screen.

### 4. Sign-to-Speech Conversion

To convert detected gestures into spoken words, run the `Sign_to_Speech.py` script:

```bash
python Sign_to_Speech.py
```

This script detects sign language letters, forms words, and uses the `pyttsx3` library to convert them into speech.

## Contributing

Contributions are welcome! If you would like to contribute to this project, please fork the repository and submit a pull request. For significant changes, please open an issue first to discuss your ideas.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## REFERENCES
https://www.youtube.com/watch?v=MJCSjXepaAM
