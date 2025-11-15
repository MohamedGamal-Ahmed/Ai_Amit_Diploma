# Copilot Instructions for Ai_Amit_Diploma

This repository is a comprehensive **Machine Learning & Data Science portfolio** spanning educational projects to production-ready applications. It contains multiple ML projects at different maturity levels, from learning exercises to complete end-to-end ML pipelines.

## Project Structure & Architecture

### 📁 Main Directories

- **`Amit_ai_diploma/`** — Collection of mature ML projects with complete pipelines
  - `ML_P1/` — Boston Housing Price Prediction (Regression) with both ML and DL models
  - `student_success_project/` — End-to-end classification pipeline predicting student outcomes (Dropout/Enrolled/Graduate)
  - `correspondence_management-main/` — Full-stack database application with Arabic UI
  - Other projects: Forecasting, B2B systems, Hospital data systems

- **`Learning_Amit/`** — Jupyter notebooks for learning ML/DL concepts
  - Contains experimental notebooks, datasets, and exploratory analysis
  - Mix of classification, regression, NLP, and deep learning experiments
  - Used for prototyping and learning patterns

- **`Python/`** — General Python tasks and assignments structure

### 🏗️ Architecture Pattern: ML Pipeline Architecture

This codebase follows a **standard ML pipeline pattern** for production projects:

1. **Data Loading & Cleaning** → `data_preprocessing.py`
2. **Feature Engineering** → `feature_engineering.py` 
3. **Model Training & Evaluation** → `model_training.py`, `model_evaluation.py`
4. **Analysis & Insights** → `feature_analysis.py`
5. **Deployment** → Streamlit apps (`app/streamlit_app.py`)

**Example**: `student_success_project/` executes in sequential order:
```bash
python src/data_preprocessing.py
python src/feature_engineering.py
python src/model_training.py
python src/model_evaluation.py
python src/feature_analysis.py
python main.py  # Runs Streamlit dashboard
```

## Critical Developer Workflows

### Running ML Projects

**For production projects** (like `student_success_project/` or `ML_P1/`):
1. Install dependencies: `pip install -r requirements.txt`
2. Run preprocessing pipeline in sequence (see file names above)
3. Launch Streamlit: `python main.py` or `streamlit run app/streamlit_app.py`

**For learning notebooks** (`Learning_Amit/`):
- Execute Jupyter notebooks directly; they're self-contained
- Dependencies: `pandas`, `numpy`, `scikit-learn`, `tensorflow`, `plotly`

### Key Commands

- **Data inspection**: Use utility functions like `dtypes_and_unique()` and `is_null()` defined in preprocessing modules
- **Model evaluation**: All models evaluate on test set with `accuracy_score`, `f1_score`, `classification_report`
- **Visualization**: Use `plotly.express` for interactive dashboards (not static matplotlib in production apps)

## Project-Specific Conventions & Patterns

### 1. **Data Preprocessing Pattern**
All projects follow pandas-based cleaning:
```python
# Typical preprocessing flow
df = pd.read_csv(filepath)
df = df.drop_duplicates()
# Fill missing: mean for numeric, mode for categorical
# Encode categorical columns with LabelEncoder
# Scale with StandardScaler/MinMaxScaler before training
```

### 2. **Model Training Pattern**
Uses scikit-learn with grid search for hyperparameter tuning:
```python
# Random Forest is preferred for classification
# Logistic Regression as baseline
# Always use class_weight='balanced' for imbalanced data
# GridSearchCV for optimization with scoring='f1_weighted'
grid = GridSearchCV(rf, param_grid, scoring='f1_weighted', cv=3, n_jobs=-1)
```

### 3. **Streamlit Deployment Pattern**
Production dashboards use Streamlit with:
- `@st.cache_resource` for loading heavy models/data
- Tabs for multiple views (e.g., ML vs DL models in ML_P1)
- Plotly for interactive visualizations
- `TARGET_MAP` dictionaries for encoding class labels

### 4. **Notebook vs Production Code Split**
- **Notebooks** (`*.ipynb`): Exploratory analysis, prototyping, visualization
- **Python scripts** (`*.py`): Production pipelines with proper functions and error handling
- Cross-reference: `feature_analysis.py` creates feature importance, used in streamlit apps

## Integration Points & External Dependencies

### Primary Libraries
- **ML/Data**: pandas, numpy, scikit-learn
- **DL**: tensorflow/keras (for neural networks in some projects)
- **Visualization**: plotly, matplotlib, seaborn
- **Deployment**: streamlit, joblib (model serialization)

### Data Flow Across Projects

**Student Success Project** (complete example):
1. Raw CSV → `data_preprocessing.py` → `data/clean_students.csv`
2. Clean data → `feature_engineering.py` → Enhanced features
3. Features → `model_training.py` → `models/model_optimized.pkl`
4. Model + features → `streamlit_app.py` → Interactive predictions

**ML_P1 Project**:
- Data: `housing.csv` → Scaled → Trained on both sklearn (Decision Tree) and keras (NN)
- Outputs: `reg.pkl` (sklearn) + `model_outputs/nn_model.keras` (TensorFlow)
- Dashboard compares both in tabs

## Common Patterns to Reuse

### Handle Class Imbalance
```python
from imblearn.over_sampling import SMOTE  # Used in student_success_project
SMOTE(random_state=42).fit_resample(X_train, y_train)
```

### Feature Importance Analysis
```python
feature_importance = best_model.feature_importances_
pd.DataFrame({'Feature': feature_names, 'Importance': feature_importance}).sort_values('Importance', ascending=False)
```

### Train-Test Split with Stratification
```python
train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
```

### Interactive Streamlit Inputs
```python
rm = st.number_input("Feature Name", min_value=1.0, step=0.1)
if st.button("Predict"):
    prediction = model.predict(np.array([[rm, ...]]))
    st.success(f"Result: {prediction[0]:.2f}")
```

## Common File Naming & Locations

- **Models**: Saved in `models/` or `model_outputs/` as `.pkl` (sklearn) or `.keras` (TensorFlow)
- **Clean Data**: `data/clean_*.csv` or `data/processed/`
- **Reports**: `reports/` contains training histories and metrics
- **App Files**: `app/streamlit_app.py` or `main.py` (wrapper)
- **Config**: `requirements.txt` always in project root

## Notes for AI Agents

- **Path handling**: Some projects use absolute Windows paths like `C:/Users/Mgama/...` — be aware when refactoring
- **Language mix**: Repository contains both English and Arabic code/comments
- **Maturity levels**: Projects range from learning notebooks to production-ready; check project-level README for context
- **Preprocessing is critical**: Always run the pipeline in order; outputs feed into subsequent steps
