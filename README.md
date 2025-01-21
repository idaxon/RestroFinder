# RestoFinder

**RestoFinder** is a personalized restaurant recommendation dashboard built using Python, Dash, and Plotly. This app helps users discover the best restaurants tailored to their preferences, budget, and location.

---

## Features

- **Personalized Recommendations**: Tailored to user preferences, including cuisine, price, and ratings.
- **Extensive Database**: Search through a wide variety of restaurants and cuisines.
- **Interactive Dashboard**: User-friendly interface with advanced filtering options.
- **Real-Time Updates**: Stay informed about trending restaurants and offers.
- **Verified Reviews**: Access trusted ratings and reviews for restaurants.
- **Visualization**: Interactive maps and graphs for better insights:
  - Restaurant locations on a map.
  - Heatmaps for ratings and restaurant density.
  - Rating distribution histogram.
- **Mobile-Friendly Design**: Works seamlessly on all devices.
- **Exclusive Deals**: Registered users can access special offers.
- **24/7 Support**: Get assistance anytime.

---

## Installation and Setup

### Prerequisites
- Python 3.7+
- `pip` (Python package manager)

### Clone the Repository
```bash
git clone https://github.com/your-username/restofinder.git
cd restofinder
```

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Required Files
Ensure the following files are present in the root directory:
- `dineout_data_cleaned_final.csv` (Dataset containing restaurant data, available [here](https://www.kaggle.com/datasets/chitwanmanchanda/dineout-delhi-ncr-restaurant-dataset))

---

## Running the Application

1. Open a terminal in the project directory.
2. Run the following command:
   ```bash
   python app.py
   ```
3. Open your browser and navigate to `http://127.0.0.1:8050/` to use the application.

---

## Usage

### Landing Page
- Provides an overview of RestoFinder with features and instructions.

### Filters
- **Price per Person**: Specify the cost range for meals.
- **Cuisine Selection**: Choose from famous cuisines or search for additional ones.
- **Number of People**: Specify the group size for accurate cost calculation.

### Outputs
- **Top Locations**: Displays a table of the best matches based on user inputs.
- **Selected Locations Map**: Interactive map showing filtered restaurant locations.
- **General Heatmap**: Visualizes overall restaurant density and ratings.

### Visualizations
- **Rating Distribution**: Histogram of restaurant ratings.
- **Location Heatmap**: Density map for top-rated restaurants.

---

## Technologies Used
- **Dash**: For building the interactive web app.
- **Plotly**: For data visualization.
- **Pandas**: For data preprocessing.
- **Scikit-Learn**: For basic machine learning model setup.
- **Bootstrap**: For styling and responsive design.

---

## Contributing

We welcome contributions to improve RestoFinder! To contribute:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Make your changes and commit them.
4. Push to your branch and create a pull request.

---

## Contact
For questions or support, contact us at:
- LinkedIn - www.linkedin.com/in/daksh-mishra-5a036b2b1

---
