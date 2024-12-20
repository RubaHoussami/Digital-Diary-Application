# Digital Diary Application

The Digital Diary Application is a versatile tool designed to assist users in maintaining a digital journal, extracting meaningful insights, and gaining deeper self-awareness. It leverages advanced Natural Language Processing (NLP) models to provide personalized analysis and advice based on user input.

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [How to Use](#how-to-use)
- [Project Structure](#project-structure)
- [License](#license)

## Introduction

The Digital Diary Application allows users to create, view, and delete diary entries while providing insightful features such as:

- Emotion Extraction: Identifies the emotional tone of user entries.
- Event Extraction: Extracts and categorizes events from user inputs.
- Character Trait Analysis: Analyzes personality traits based on textual input.
- Personalized Advice Generation: Suggests actionable advice based on extracted insights.

This application ensures data privacy and user security through robust authentication mechanisms and local storage of sensitive data.

## Features

- Emotion Extraction: Detects emotions such as happiness, sadness, anger, and more.
- Event Extraction: Identifies key events and topics from user entries.
- Character Trait Analysis: Provides insights into personality traits based on textual data.
- Personalized Advice Generation: Offers helpful suggestions based on the context of the diary entry.
- User Authentication: Implements secure login and logout functionality with JWT-based authentication.
- Extensibility: Modular architecture for adding custom NLP extractors and new functionalities.

## Installation

1. Clone the Repository:
```bash
git clone https://github.com/RubaHoussami/Digital-Diary-Application.git
```

2. Navigate to the Project Directory:
```bash
cd Digital-Diary-Application
```

3. Install Dependencies:
```bash
pip install -r requirements.txt
```

4. Set Up Environment Variables (Copy the example .env file and configure it):
```bash
cp .env.example .env
```

5. Download Pre-Trained Models:
   Download the pre-trained models and their tokenizers from Hugging Face:
   - Emotion Extraction Model: https://huggingface.co/stefaniesamaha/emotion_extraction
   - Event Extraction Model: https://huggingface.co/hawraakhalil/event_extraction
   - Character Trait Extraction Model: https://huggingface.co/rhe34/Character_Trait_Extractor
   - Advice Generation Model: https://huggingface.co/stefaniesamaha/advicegeneration

   Place the downloaded models in the src/models/model_respective_directory directory.

## How to Use

1. Start the Application:
```bash
python app.py
```

2. Access the Application:
   Open your web browser and navigate to http://localhost:5000 to access the application.

3. API Endpoints:
   The application provides several API endpoints documented using Swagger. You can access the Swagger documentation by visiting /apidocs on your localhost. These endpoints include:
   - Emotion Extraction
   - Event Extraction
   - Character Trait Extraction
   - Advice Generation
   - User Authentication and Manipulation

4. Explore the Features:
   Use the Swagger interface to add diary entries, extract insights, and receive personalized advice.

## Project Structure
Digital-Diary-Application/
├── local_datasets/         # Directory for storing any local datasets
├── model_training/         # Files used for fine-tuning the models
├── src/
│   ├── models/             # Directory for storing pre-trained fine-tuned models and tokenizers
│   ├── crew/
│   │   ├── active/         # Classes for extractors and sanitizers
│   │   ├── base/           # Base classes for extractors and sanitizers
│   ├── api/v1/
│   │   ├── controllers/    # API endpoints documented with Swagger
│   │   ├── models/         # SQLAlchemy database models
│   │   ├── schemas/        # Marshmallow schemas for validation
│   │   ├── services/       # Core functions for endpoints
│   │   ├── utils/          # Utility scripts used across the application
│   ├── errors.py           # Custom error handling
│   ├── extensions.py       # JWT manager and database setup
│   ├── logger.py           # Logger configuration
│   ├── logout_management.py# Token management for user logout
├── requirements.txt        # Python dependencies
├── app.py                  # Flask application entry point
├── .env.example            # Example environment configuration file
└── README.md               # Project documentation


## License

This project is licensed under the MIT License. See the LICENSE file for more information.
