skycell_dashboard/
├── app.py                 # Main Flask backend
├── static/
│   ├── css/
│   │   └── styles.css     # Custom styles or Tailwind
│   └── images/            # Received balloon images
├── templates/
│   └── dashboard.html     # Main dashboard page
├── data/
│   └── balloon_state.json # Optional: store latest telemetry
└── modules/
    ├── data_fetcher.py    # Connects to LoRa / handles parsing
    └── utils.py           # General helpers like unit conversion
