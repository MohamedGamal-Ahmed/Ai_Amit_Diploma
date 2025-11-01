# Boston House Price Prediction

This project predicts house prices in Boston using machine learning techniques. It's part of the Machine Learning Engineer Nanodegree program, focusing on model evaluation and validation.

## Project Overview

The goal of this project is to predict the median value of owner-occupied homes (MEDV) in Boston based on various features such as:
- RM: Average number of rooms per dwelling
- LSTAT: Percentage of population considered lower status
- PTRATIO: Pupil-teacher ratio by town

The project demonstrates fundamental machine learning concepts including:
- Data exploration and preprocessing
- Model training and evaluation
- Hyperparameter tuning
- Cross-validation techniques
- Bias-variance tradeoff

## Files in this Project

- [`boston_housing.ipynb`](boston_housing.ipynb): Main Jupyter notebook containing data analysis, model development, and evaluation
- [`app.py`](app.py): Streamlit web application for deploying the trained model
- [`visuals.py`](visuals.py): Helper functions for creating visualizations
- `housing.csv`: Dataset containing Boston housing data (not included in this repository)
- `reg.pkl`: Trained model file (not included in this repository)

## Dataset

The dataset contains 489 instances with 4 features:
- **RM**: Average number of rooms (float)
- **LSTAT**: Percentage of lower status population (float)
- **PTRATIO**: Pupil-teacher ratio (float)
- **MEDV**: Median value of owner-occupied homes in $1000s (target variable)

Basic statistics:
- Mean home value: $454,342.90
- Standard deviation: $165,340.30
- Minimum value: $105,000
- Maximum value: $1,024,800

## Methodology

This project uses a Decision Tree Regressor to predict housing prices. Key steps include:

1. **Data Exploration**: Analyzing the distribution and relationships between features
2. **Model Training**: Using decision trees with varying complexity (max_depth)
3. **Model Evaluation**: Applying k-fold cross-validation to assess performance
4. **Hyperparameter Tuning**: Finding the optimal tree depth to balance bias and variance

## Results

The analysis shows that:
- A decision tree with max_depth around 3-4 provides the best generalization
- Models with max_depth=1 suffer from high bias (underfitting)
- Models with max_depth=10 suffer from high variance (overfitting)
- Cross-validation helps ensure reliable performance estimates

## Requirements

To run this project, you need the following Python packages:
- numpy
- pandas
- scikit-learn
- matplotlib
- streamlit
- joblib

Install requirements with:
```bash
pip install -r requirements.txt
```

## Usage

### Jupyter Notebook
To explore the analysis and modeling process:
```bash
jupyter notebook boston_housing.ipynb
```

### Web Application
To run the Streamlit web app:
```bash
streamlit run app.py
```

Enter the requested features (number of rooms, poverty level, and student-teacher ratio) to get a price prediction.

## License

This project is part of the Machine Learning Engineer Nanodegree program. The dataset is derived from the Boston Housing dataset originally published by Harrison, D. and Rubinfeld, D.L.

## Acknowledgements

- Udacity for providing the Machine Learning Engineer Nanodegree curriculum
- The scikit-learn team for their excellent machine learning library#
