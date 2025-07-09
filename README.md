
# 🌍 Earthquake ETL Pipeline (USGS API → BigQuery → Dashboard)

This project is an end-to-end ETL (Extract-Transform-Load) pipeline that retrieves real-time and historical global earthquake data from the **USGS Earthquake API**, processes it using Python, and uploads it into **Google BigQuery** for analysis and visualization (e.g., via **Looker Studio**).

---

## 🎯 Project Objectives

- Build a robust data pipeline using Python
- Work with real-world data from public APIs
- Store data in a cloud warehouse (Google BigQuery)
- Visualize earthquake trends on dashboards
- Demonstrate both **real-time** and **historical** data handling

---

## 📦 Features

- ✅ Extract earthquake data from USGS (24h, 1h, or by date)
- ✅ Transform and clean data using pandas
- ✅ Enrich with derived features (e.g., magnitude category)
- ✅ Upload to Google BigQuery with flexible upload mode
- ✅ Logging to file and console for monitoring
- ✅ Ready for dashboard integration (Looker Studio or Data Studio)

---

## 🗂️ Project Structure

```
etl_project/
├── etl/
│   ├── extract.py               # Fetch data from API
│   ├── transform.py             # Clean & enrich data
│   └── load.py                  # Upload to BigQuery
├── logs/
│   └── etl_log_*.log            # Log files
├── main.py                      # Orchestration script
├── requirements.txt             # Python dependencies
└── README.md                    # Project documentation
```

---

## 🧪 Installation

1. **Clone repository**
   ```bash
   git clone https://github.com/your-username/earthquake-etl.git
   cd earthquake-etl
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up Google Cloud**
   - Enable BigQuery API
   - Create a dataset (e.g., `earthquake_data`)
   - Download service account key and save as:
     ```
     config/service_account.json
     ```

---

## ⚙️ How to Run the Pipeline

### 🔄 Real-Time Mode (last 24h earthquakes)
```bash
python main.py --mode realtime
```

### 📅 Historical Mode (by date range)
```bash
python main.py --mode historical --start_date 2023-07-01 --end_date 2023-07-02
```

> ⚠ Historical mode uses the `fdsnws` endpoint and supports querying back to early 1900s.  
> Recommended: limit to one day or paginate to avoid API limits.

---

## 📊 BigQuery Schema Example

Dataset: `earthquake_data`  
Tables:
- `realtime_events`
- `historical_events`

Essential columns:
- `id`, `place`, `mag`, `time`, `latitude`, `longitude`, `depth`
- `mag_category`, `is_significant`, `day_of_week`, `hour_of_day`

---

## 📌 Sample Use Cases

- Build Looker Studio dashboard with trend line, heatmap, and severity maps
- Monitor significant (>5.5M) earthquakes globally
- Analyze time-based or regional patterns

---

## 🔐 Security

Credentials are handled securely via service account stored at:
```
config/service_account.json
```
**Never commit this file to version control.**

---

## ✅ To-Do / Enhancements

- [ ] Add automatic scheduler with cron or Prefect
- [ ] Extend to support weekly/monthly historical ingestion
- [ ] Enable GCS export before BigQuery
- [ ] Alerting on significant earthquake events

---

## 📚 References

- [USGS Earthquake GeoJSON Feed](https://earthquake.usgs.gov/earthquakes/feed/v1.0/geojson.php)
- [USGS Event Query API](https://earthquake.usgs.gov/fdsnws/event/1/)
- [Google BigQuery Docs](https://cloud.google.com/bigquery)
- [pandas-gbq](https://pandas-gbq.readthedocs.io/)

---

## 👨‍💻 Author

Developed by [Your Name] – Data Engineer & Analyst  
Feel free to fork or contribute!
