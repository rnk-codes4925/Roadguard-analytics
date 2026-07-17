# 🛡️ RoadGuard Safety Analytics Dashboard

[![Live App](https://img.shields.io/badge/Streamlit-Live%20Demo-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://roadguard-analytics-8sgatjwuznjiyhezvuur58.streamlit.app/)

RoadGuard Analytics is a professional-grade, interactive road safety intelligence dashboard designed to analyze and visualize UK safety incident records. Built using **Streamlit**, **Plotly**, and **Pandas**, this application provides deep, actionable insights into vehicle types, monthly trends, geographic hotspots, road types, and environmental factors (weather and lighting).

---

## 🚀 Features

- **Executive KPI Metrics**: Live-calculated metrics showing current year (CY) vs. prior year (PY) percentage changes for casualties, accidents, and severity levels.
- **Interactive Multi-Page Navigation**:
  - **Executive Overview**: High-level visual metrics, monthly trends, geographical hotspots, and incident distributions.
  - **Deep Dive Analytics**: Speed limit distributions, weather-severity cross-tabulation, and interactive tabular record exploration.
  - **Spatial Mapping**: Map-based visualization of coordinates with clustering.
  - **Insights & Export**: Auto-generated text summaries and options to extract filtered data directly to CSV.
- **Responsive Theme Configuration**: Sleek, high-contrast modern dark-neon interface optimized for readability.
- **Dynamic Data Engine**: Automatically checks for datasets or generates robust statistical models of road incidents on startup.

---

## 📁 Repository File Structure

To deploy this application successfully on **Streamlit Community Cloud**, your GitHub repository must contain the following core files:

```bash
├── app.py               # Main Streamlit application entry point
├── charts.py            # Custom Plotly visualization engine
├── style.py             # Global CSS and Custom Design System
├── utils.py             # Data loading, filtering pipeline, and mock generator
├── requirements.txt     # Python libraries/dependencies list
└── README.md            # Project documentation (this file)
```

> ⚠️ **Note**: You do *not* need to commit Node.js/Vite files like `package.json`, `vite.config.ts`, `bun.lock`, or `src/` to your Streamlit GitHub repository, as they are part of the local workspace infrastructure and not required by Streamlit.

---

## 🛠️ Local Installation & Setup

If you want to run this dashboard locally on your machine, follow these simple steps:

1. **Clone the Repository**:
   ```bash
   git clone <your-github-repo-url>
   cd <your-repo-name>
   ```

2. **Create a Virtual Environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Launch the Dashboard**:
   ```bash
   streamlit run app.py
   ```

---

## ☁️ Deploying to Streamlit Community Cloud (Step-by-Step)

Follow this professional guide to deploy your dashboard to the web for free:

### Step 1: Create a GitHub Repository
1. Go to [GitHub](https://github.com) and log in.
2. Click **New** (or "+" in the top-right corner) to create a new repository.
3. Give your repository a name (e.g., `roadguard-analytics`).
4. Set it to **Public** (required for the free tier of Streamlit Cloud).
5. Do *not* add a README, `.gitignore`, or license if you want to push your existing files directly. Click **Create repository**.

### Step 2: Push Your Code to GitHub
Open your terminal inside your project folder and run:
```bash
# Initialize git repository
git init

# Add only the required Python files & requirements
git add app.py charts.py style.py utils.py requirements.txt README.md

# Commit your changes
git commit -m "Initial commit: RoadGuard Dashboard files"

# Link your local repo to GitHub and push
git branch -M main
git remote add origin <YOUR_GITHUB_REPOSITORY_URL>
git push -u origin main
```

### Step 3: Set up Streamlit Community Cloud
1. Visit [Streamlit Share / Cloud](https://share.streamlit.io/) and click **Sign up** or **Sign in** using your **GitHub account**.
2. Once logged in, click the **Create app** (or **New app**) button in the dashboard.

### Step 4: Configure & Deploy the App
In the deployment form, fill in the details:
- **Repository**: Choose your newly created repository (`<username>/roadguard-analytics`).
- **Branch**: Select `main`.
- **Main file path**: Type `app.py`.
- Click **Deploy!**

Within 1-2 minutes, Streamlit Cloud will read your `requirements.txt`, install all the libraries, and launch your live production-ready dashboard. Enjoy! 🛡️
