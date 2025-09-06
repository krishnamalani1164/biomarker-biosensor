# biomarker-biosensor
# Biomarker Biosensor Project

<img width="1919" height="959" alt="Screenshot 2025-09-06 172627" src="https://github.com/user-attachments/assets/b02c3ec7-7e5b-40a6-836c-5d87a6a90f45" />
<img width="1650" height="699" alt="Screenshot 2025-09-06 172711" src="https://github.com/user-attachments/assets/e4a82d56-6727-4380-9c63-5e016f2e756c" />
<img width="1641" height="825" alt="Screenshot 2025-09-06 172728" src="https://github.com/user-attachments/assets/3a02da24-4d3a-404e-9689-9e5e06dc3742" />

## Project Overview

This project is a comprehensive biosensing system for detecting cardiovascular disease (CVD) biomarkers, developed in collaboration with **ABHIJEET AWASTHI**. The system consists of a web-based interface running on an ESP32 microcontroller that allows users to:

* Create and manage biomarker test configurations
* Run diagnostic tests with real-time data visualization
* Store test results in a database
* View historical test data

## Key Features

### Web Interface
* **Main Dashboard**: Central hub with navigation to all system functions
* **Test Configuration**: Create and edit biomarker test parameters including:
   * Test name and type (EP/TP)
   * Wavelength selection (360nm, 420nm, 460nm, 540nm)
   * Temperature settings
   * Flag thresholds (low/high)
   * Number of readings (for EP tests)
   * R1/R2 values (for TP tests)

### Real-Time Testing
* **Interactive Graph**: Live visualization of absorbance data using Chart.js
* **Result Calculation**: Automatic concentration calculation using Beer-Lambert Law
* **Test Controls**: Buttons for water, blank, standard, sample, and wash operations

### Data Management
* **CSV Database**: Stores all test configurations and results
* **Timestamped Records**: Each test entry includes date/time information
* **Persistent Storage**: Data survives device reboots

## Technical Implementation

### Hardware
* ESP32 microcontroller
* Wi-Fi connectivity (STA mode)
* Sensor interface for biomarker detection

### Software
* MicroPython firmware
* Asynchronous web server
* HTML5/CSS3 frontend with responsive design
* JavaScript for interactive elements (Chart.js for graphing)

### File Structure
* `basic.py`: Core web server implementation
* `creating_database.py`: Database creation and management
* `import network.txt`: Network configuration and connectivity

## Installation & Setup

### 1. Flash ESP32 with MicroPython

```bash
esptool.py --chip esp32 --port /dev/ttyUSB0 erase_flash
esptool.py --chip esp32 --port /dev/ttyUSB0 --baud 460800 write_flash -z 0x1000 micropython.bin
```

### 2. Upload Project Files

```bash
ampy --port /dev/ttyUSB0 put basic.py
ampy --port /dev/ttyUSB0 put creating_database.py
```

### 3. Configure Wi-Fi
Edit the SSID and PASSWORD variables in the code to match your network.

### 4. Run the System

```python
import basic
```

## Usage Instructions

1. Connect to the ESP32's Wi-Fi network
2. Open a web browser and navigate to the displayed IP address
3. Use the interface to:
   * Create new biomarker tests
   * Run diagnostic procedures
   * View historical results

## Data Flow

1. **Test Configuration**: User inputs → HTML form → POST request → CSV storage
2. **Test Execution**: Sensor data → ESP32 → WebSocket → Chart.js visualization
3. **Result Storage**: Calculated results → CSV database with timestamp

## Collaboration Credits

This project was developed in collaboration with **Abijeet Washi**, who contributed to:
* System architecture design
* Data visualization implementation
* User interface optimization
* Testing and validation procedures

## Future Enhancements

* Add user authentication
* Implement data export functionality
* Add multi-user support
* Enhance sensor calibration routines
* Develop mobile app interface

## Troubleshooting

### Connection Issues
* Verify Wi-Fi credentials
* Check ESP32 power supply
* Ensure proper antenna placement

### Data Storage Problems
* Verify filesystem has sufficient space
* Check CSV file permissions
* Ensure proper file closures after writes
