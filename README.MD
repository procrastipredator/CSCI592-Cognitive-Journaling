# Therapist Co-Pilot: Hybrid AI for Cognitive Distortion Detection

**CSCI 592: Intelligent Systems | Fall 2025**

![Python](https://img.shields.io/badge/Python-3.9%2B-blue) ![License](https://img.shields.io/badge/License-MIT-green) ![Status](https://img.shields.io/badge/Status-Research%20Prototype-orange)

## Abstract

Cognitive Behavioral Therapy (CBT) relies on identifying cognitive distortions, yet the feedback loop between patient journaling and therapist review remains inefficient. This study evaluates two artificial intelligence paradigms for automating this process: a symbolic Rule-Based Expert System ("Glass Box") and a subsymbolic Linear Support Vector Machine ("Statistical Learning"). The systems were evaluated on a novel, trilingual dataset (English, Russian, Kazakh) reflecting the code-switching linguistic reality of university students in Central Asia. Results from a comparative A/B test (N=302) demonstrate that the statistical model (Accuracy=87%) significantly outperformed the rule-based system (Accuracy=64%) and surprisingly surpassed a DistilBERT deep learning baseline (Accuracy=81%).

## Key Features

* **Hybrid Inference Engine:** A deterministic router that switches between Rule-Based and ML backends based on User ID for A/B testing.
* **Trilingual Support:** Engineered to handle English, Russian, and Kazakh (Cyrillic) inputs, including code-switching.
* **Live Interface:** A fully functional Telegram Bot (`src/bot.py`) capable of asynchronous user interaction.
* **Privacy-First Design:** Logs are anonymized, and the system functions as a "screener" rather than a diagnostic tool.


## 🛠️ Setup & Usage

### 1. Installation

```
git clone https://github.com/yourusername/CSCI592-Cognitive-Journaling.git
cd CSCI592-Cognitive-Journaling
pip install -r requirements.txt
```

### 2. Training the Model (System B)

Before running the bot, you must generate the model artifacts

```
python scripts/train_local.py
```

### 3. Running the Bot

* Open src/bot.py.
* Replace TOKEN = "YOUR_TOKEN_GOES_HERE" with your Telegram API Token.
* Run the bot:

```
python src/bot.py
```

## Results Summary

| **Model System**     | **Accuracy** | **Precision** | **Recall** | **F1-Score** |
| -------------------------- | ------------------ | ------------------- | ---------------- | ------------------ |
| **System A (Rules)** | **0.64**     | **0.75**      | **0.64**   | **0.60**     |
| **System B (SVM)**   | **0.87**     | **0.87**      | **0.87**   | **0.87**     |
| **DistilBERT**       | **0.81**     | **0.83**      | **0.81**   | **0.81**     |

Key Finding: While Deep Learning is popular, for low-resource tasks (N < 2000 samples), the Linear SVM provided superior stability and generalization compared to Transformers, which exhibited signs of overfitting.

## License

This project is for academic purposes. The ecological data contained herein is anonymized.
