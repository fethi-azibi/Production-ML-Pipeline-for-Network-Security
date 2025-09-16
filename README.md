# **Network Security System with ETL Pipelines and MLOps**

## **Table of Contents**
1. [Project Overview](#project-overview)
2. [Pipeline Architecture](#pipeline-architecture)
   - [Data Ingestion](#1-data-ingestion)
   - [Data Validation](#2-data-validation)
   - [Data Transformation](#3-data-transformation)
   - [Model Training](#4-model-training)
   - [Model Deployment](#5-model-deployment)
3. [Installation Guide](#installation-guide)
4. [Usage and Inference](#usage-and-inference)
5. [Technologies Used](#technologies-used)
6. [Folder Structure](#folder-structure)
7. [Future Enhancements](#future-enhancements)
8. [Contact](#contact)

---

## **Project Overview**

The **Network Security System** is an end-to-end machine learning project designed to detect phishing attacks and other network anomalies. This project leverages **ETL pipelines**, **MLOps principles**, and **cloud-based deployment** to ensure scalability, reliability, and maintainability.

### **Goal of the Project**
- Build a robust, automated pipeline for data ingestion, validation, transformation, model training, and deployment.
- Detect phishing attacks using machine learning models.
- Deploy the trained model as a REST API for real-time inference.

---

## **Pipeline Architecture**

The project is structured as a modular pipeline, with each component performing a specific task. Below is the architecture diagram and explanation for each step:

### **Pipeline Diagram**
<img src="https://github.com/user-attachments/assets/3959ae75-adb4-46fa-b320-b9b6b62d06b6" alt="Pipeline Diagram" >

### **1. Data Ingestion**
This module is responsible for fetching raw data from MongoDB, storing it in a feature store (CSV), and splitting it into training and testing datasets for downstream machine-learning tasks.

<img src="https://github.com/user-attachments/assets/d79c30d7-bb95-4a86-8efc-a2472269fe76" alt="data ingestion schema">

#### **Key Features**
- **MongoDB → Pandas**: Reads data directly from a MongoDB collection and loads it into a Pandas DataFrame.

- **Cleaning**: Drops the default MongoDB _id field and replaces any "na" strings with NaN.

- **Feature Store**: Saves the cleaned dataset as a CSV file for reproducible experiments.

- **Train/Test Split**: Splits the data into training and testing sets based on the configured ratio and stores them as separate CSV files.

- **Config-Driven**: All file paths, database names, and split ratios are provided through the DataIngestionConfig class.
#### **Implementation**
- Connects to MongoDB using the `pymongo` library.
- Drops unnecessary columns (e.g., `_id` from MongoDB).
- Saves the ingested data as an artifact for downstream tasks.

---

### **2. Data Validation**
The **Data Validation** step ensures the integrity and quality of the data.

<img alt="Image" src="https://github.com/user-attachments/assets/34728cdf-b5c1-4483-9a8f-0240e3bb13fb" />

#### **Key Features**
- **Schema Validation**: Validates the data against a predefined schema (`data_schema/schema.yaml`).
- **Missing Value Checks**: Ensures no critical columns have missing values.
- **Data Integrity**: Verifies that the data conforms to expected formats and ranges.

#### **Implementation**
- Uses YAML-based schema definitions for flexibility.
- Logs validation results for debugging and traceability.

---

### **3. Data Transformation**
The **Data Transformation** step prepares the data for machine learning by performing feature engineering and preprocessing.

<img alt="Image" src="https://github.com/user-attachments/assets/681a0e7b-8537-4efa-96bd-c55d7ca56ff7" />

#### **Key Features**
- **Feature Engineering**: Creates new features or modifies existing ones to improve model performance.
- **Scaling and Encoding**: Applies scaling (e.g., MinMaxScaler) and encoding (e.g., OneHotEncoder) to ensure the data is in a format suitable for ML models.

#### **Implementation**
- Saves the transformation pipeline as a `.pkl` file for consistent preprocessing during inference.
- Handles categorical and numerical features separately.

---

### **4. Model Training**
The **Model Training** step trains and evaluates machine learning models.

#### **Key Features**
- **Model Selection**: Trains multiple models (e.g., Decision Tree, Random Forest) and selects the best one based on evaluation metrics.
- **Hyperparameter Tuning**: Optimizes model parameters using grid search.
- **Experiment Tracking**: Logs metrics and parameters using **MLflow**.

#### **Implementation**
- Evaluates models using metrics like F1-score, precision, and recall.
- Saves the best model as `final_model/model.pkl`.

---

### **5. Model Deployment**
The **Model Deployment** step makes the trained model available for real-time inference.

#### **Key Features**
- **REST API**: Deploys the model as a REST API using **FastAPI**.
- **Containerization**: Dockerizes the application for portability.
- **Cloud Deployment**: Pushes the Docker image to **AWS ECR** and deploys it on **AWS ECS**.

#### **Implementation**
- Supports real-time predictions via HTTP requests.
- Ensures scalability and reliability using cloud infrastructure.

---

## **Installation Guide**

Follow these steps to set up the project locally:

### **Prerequisites**
- Python 3.8 or higher
- Docker
- AWS CLI configured with appropriate credentials
- MongoDB (local or cloud-based)

### **1. Clone the Repository**
```bash
git clone https://github.com/your-username/network-security-system.git
cd network-security-system
```

### **2. Set Up a Virtual Environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### **3. Install Dependencies**
```bash
pip install -r requirements.txt
```

### **4. Set Up Environment Variables**
Create a .env file in the root directory with the following content:
```bash
MONGO_DB_URL=<your_mongo_db_url>
AWS_ACCESS_KEY_ID=<your_aws_access_key>
AWS_SECRET_ACCESS_KEY=<your_aws_secret_key>
AWS_REGION=<your_aws_region>
```

### **5. Run the Application**
```bash
python app.py
```

## **Usage and Inference**
### **1. Train the Model**
Run the main.py script to execute the entire pipeline:
```bash
python main.py
```
### **2. Test the API**
Once the application is running, you can test the REST API using tools like **Postman**

## **Technologies Used**

- **Programming Language**: Python
- **Machine Learning**: scikit-learn
- **Data Processing**: Pandas, NumPy
- **Model Deployment**: FastAPI, Docker, AWS ECS
- **Experiment Tracking**: MLflow, DagsHub
- **Version Control**: GitHub
- **CI/CD**: GitHub Actions
- **Database**: MongoDB

## **Folder Structure**
```bash
.
├── .github/workflows/       # CI/CD workflows
├── Artifacts/               # Pipeline artifacts (e.g., data, models)
├── data_schema/             # Data schema for validation
├── final_model/             # Saved model and preprocessor
├── logs/                    # Log files
├── networksecurity/         # Core project code
│   ├── components/          # Pipeline components
│   ├── entity/              # Data classes
│   ├── exception/           # Custom exceptions
│   ├── logging/             # Logging setup
│   ├── pipeline/            # Pipeline orchestration
│   ├── utils/               # Utility functions
├── notebooks/               # Jupyter notebooks for EDA
├── templates/               # HTML templates for visualization
├── app.py                   # FastAPI application
├── main.py                  # Entry point for the pipeline
├── Dockerfile               # Docker configuration
├── requirements.txt
└── README.md
```

## **Future Enhancements**
- **Add Real-Time Data Streaming**: Integrate Kafka for real-time data ingestion.
- **Improve Model Performance**: Experiment with advanced models like XGBoost or LightGBM.
- **Implement Monitoring**: Use tools like Prometheus and Grafana to monitor the deployed model.
- **Expand Dataset**: Include more features and data sources to improve accuracy.

## **Contact**
For any questions or collaboration opportunities, feel free to reach out:

Name: Fethi Azibi

[LinkedIn](https://www.linkedin.com/in/fethi-azibi/)
