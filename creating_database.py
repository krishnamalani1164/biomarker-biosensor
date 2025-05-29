import os
import csv
from aiohttp import web

# Function to create or verify the database file
def create_database_file():
    filename = "Database.csv"
    header = ["timestamp", "test name", "water", "blank", "standard", "sample"]
    
    # Check if file exists
    if not os.path.exists(filename):
        with open(filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(header)  # Write header row
        print(f"{filename} created with header.")
    else:
        # Check if the file is empty
        with open(filename, mode='r') as file:
            if file.read().strip():
                print(f"{filename} already exists and contains data. No changes made.")
            else:
                with open(filename, mode='w', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow(header)
                print(f"{filename} was empty. Header added.")

# HTML: Main Page with "Create Test" Button
MAIN_PAGE = """\
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Multiplexed Biosensing</title>
    <style>
        body { 
            font-family: Arial, sans-serif; 
            text-align: center; 
            margin: 0; 
            padding: 0; 
            background-color: #f4f4f4; 
        }
        .container {
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            height: 100vh;
        }
        h1 {
            color: red;
            font-size: 32px;
            margin-bottom: 20px;
        }
        .btn {
            padding: 15px 40px;
            font-size: 20px;
            background-color: blue;
            color: white;
            border: none;
            cursor: pointer;
            border-radius: 5px;
            margin: 10px;
            width: 200px;
        }
        .btn:hover {
            background-color: #c71585;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>CVD Biomarkers</h1>
        <button class="btn" onclick="window.location.href='/chemistry-list'">Test</button>
        <button class="btn" onclick="window.location.href='/system'">System</button>
        <button class="btn" onclick="window.location.href='/result'">Result</button>
        <button class="btn" onclick="window.location.href='/help'">Help</button>
    </div>
</body>
</html>
"""

# HTML: Chemistry List Page
CHEMISTRY_LIST_PAGE = """\
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Bio-Marker List</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            text-align: center;
            margin: 0;
            padding: 0;
            background-color: #ffffff;
        }

        h1 {
            margin-top: 20px;
        }

        .test-list {
            display: flex;
            flex-direction: column;
            align-items: center;
            margin: 20px;
        }

        .test-entry {
            display: flex;
            align-items: center;
            justify-content: space-between;
            width: 50%;
            background: #f0f0f0;
            padding: 10px;
            margin: 5px 0;
            border-radius: 5px;
            cursor: pointer;
        }

        .test-entry:hover {
            background-color: #e0e0e0;
        }

        .test-entry span {
            flex-grow: 1;
            text-align: left;
            margin-left: 10px;
        }

        .test-entry b {
            font-weight: bold;
        }

        .test-entry button {
            background: none;
            border: none;
            cursor: pointer;
            font-size: 18px;
        }

        .modal {
            display: none;
            position: fixed;
            z-index: 1000;
            left: 50%;
            top: 50%;
            transform: translate(-50%, -50%);
            background: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0px 0px 10px gray;
            width: 400px;
            text-align: left;
        }

        .modal input, .modal select {
            width: 100%;
            padding: 8px;
            margin: 5px 0;
            border: 1px solid #ccc;
            border-radius: 5px;
        }

        .modal button {
            width: 100%;
            padding: 10px;
            background-color: #007BFF;
            color: white;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            margin-top: 10px;
        }

        .modal button:hover {
            background-color: #0056b3;
        }

        .close-btn {
            position: absolute;
            top: 5px;
            right: 10px;
            cursor: pointer;
            font-size: 20px;
            font-weight: bold;
        }

        .footer {
            position: fixed;
            bottom: 0;
            width: 100%;
            padding: 10px;
            background-color: #007BFF;
            color: white;
            text-align: center;
        }

        .footer button {
            margin: 5px;
            padding: 10px 15px;
            font-size: 16px;
            border: none;
            cursor: pointer;
            color: white;
            background: #0056b3;
            border-radius: 5px;
        }

        .hidden {
            display: none;
        }
    </style>
</head>
<body>
    <h1>Chemistry Test List</h1>
    
    <div class="test-list" id="testList"></div>
    
    <div id="testModal" class="modal">
        <span class="close-btn" onclick="closeModal()">&times;</span>
        <h2 id="modalTitle">New Test</h2>
        
        <label>Test Name</label>
        <input type="text" id="testName" placeholder="Enter Test Name">

        <label>Test Type</label>
        <select id="testType" onchange="toggleTestTypeFields()">
            <option value="EP" selected>EP</option>
            <option value="TP">TP</option>
        </select>

        <input type="number" id="numReadings" placeholder="Number of Readings">
        <input type="number" id="r1Value" class="hidden" placeholder="Enter R1">
        <input type="number" id="r2Value" class="hidden" placeholder="Enter R2">

        <label>Wavelength</label>
        <select id="wavelength">
            <option value="360">360 nm</option>
            <option value="420">420 nm</option>
            <option value="460">460 nm</option>
            <option value="540">540 nm</option>
        </select>

        <label>Temperature (Â°C)</label>
        <input type="number" id="temperature" placeholder="Enter Temperature">

        <label>Low Flag</label>
        <input type="number" id="lowFlag" placeholder="Enter Low Flag">
        
        <label>High Flag</label>
        <input type="number" id="highFlag" placeholder="Enter High Flag">

        <button onclick="submitTest()">Submit</button>
    </div>

    <div class="footer">
        <button onclick="openModal()">New Test</button>
    </div>

    <script>
        let currentEditElement = null;

        function openModal(editingElement = null) {
            // Send a request to the server to create the database file
            fetch('/create-database', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({}) // No data needed for this request
            })
            .then(response => {
                if (response.ok) {
                    // Proceed to open the modal
                    document.getElementById("testModal").style.display = "block";
                    document.getElementById("modalTitle").textContent = editingElement ? "Edit Test" : "New Test";
                    document.getElementById("testName").value = editingElement ? editingElement.dataset.name : "";
                    document.getElementById("testType").value = editingElement ? editingElement.dataset.type : "EP";
                    document.getElementById("numReadings").value = editingElement ? editingElement.dataset.readings : "";
                    document.getElementById("r1Value").value = editingElement ? editingElement.dataset.r1 : "";
                    document.getElementById("r2Value").value = editingElement ? editingElement.dataset.r2 : "";
                    document.getElementById("wavelength").value = editingElement ? editingElement.dataset.wavelength : "360";
                    document.getElementById("temperature").value = editingElement ? editingElement.dataset.temperature : "";
                    document.getElementById("lowFlag").value = editingElement ? editingElement.dataset.lowflag : "";
                    document.getElementById("highFlag").value = editingElement ? editingElement.dataset.highflag : "";

                    toggleTestTypeFields();
                    currentEditElement = editingElement;
                } else {
                    alert("Error creating database file");
                }
            })
            .catch(error => {
                alert("Error creating database file: " + error);
            });
        }

        function closeModal() {
            document.getElementById("testModal").style.display = "none";
            currentEditElement = null;
        }

        function toggleTestTypeFields() {
            let testType = document.getElementById("testType").value;
            document.getElementById("numReadings").classList.toggle("hidden", testType !== "EP");
            document.getElementById("r1Value").classList.toggle("hidden", testType !== "TP");
            document.getElementById("r2Value").classList.toggle("hidden", testType !== "TP");
        }

        function submitTest() {
            let testName = document.getElementById("testName").value;
            let testType = document.getElementById("testType").value;
            let wavelength = document.getElementById("wavelength").value;
            let temperature = document.getElementById("temperature").value;
            let lowFlag = document.getElementById("lowFlag").value;
            let highFlag = document.getElementById("highFlag").value;
            let numReadings = document.getElementById("numReadings").value;
            let r1Value = document.getElementById("r1Value").value;
            let r2Value = document.getElementById("r2Value").value;

            // Create a JSON object with the data
            let data = {
                testName: testName,
                testType: testType,
                wavelength: wavelength,
                temperature: temperature,
                lowFlag: lowFlag,
                highFlag: highFlag,
                numReadings: numReadings,
                r1Value: r1Value,
                r2Value: r2Value
            };

            // Send the data to the server using a POST request
            fetch("/save-data", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(data)
            })
            .then(response => {
                if (response.ok) {
                    // Add the test to the list on the screen
                    let testEntry = document.createElement("div");
                    testEntry.classList.add("test-entry");
                    testEntry.dataset.name = testName;
                    testEntry.dataset.type = testType;
                    testEntry.dataset.wavelength = wavelength;
                    testEntry.innerHTML = `
                        <span><b>${testName}</b> (${testType}) - ${wavelength} nm</span>
                        <button onclick="openModal(this.parentElement)">âœï¸</button>
                        <button onclick="deleteTest(this)">âŒ</button>
                    `;
                    testEntry.onclick = () => {
                        window.location.href = "/run_test";
                    };
                    document.getElementById("testList").appendChild(testEntry);

                    // Close the modal
                    closeModal();
                } else {
                    alert("Error saving data");
                }
            })
            .catch(error => {
                alert("Error saving data: " + error);
            });
        }

        function deleteTest(button) {
            button.parentElement.remove();
        }
    </script>
</body>
</html>
"""

# HTML: Run Test Page
RUN_TEST_PAGE = """\
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Run Test</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            text-align: center;
            margin: 0;
            padding: 0;
            background-color: #ffffff;
        }
        h1 {
            color: red;
            font-size: 32px;
            margin-bottom: 20px;
        }
        .btn {
            padding: 10px 15px;
            font-size: 14px;
            background-color: #007BFF;
            color: white;
            border: none;
            cursor: pointer;
            border-radius: 5px;
            margin: 5px;
            width: 100px;
        }
        .btn:hover {
            background-color: #0056b3;
        }
        .result-window {
            width: 90%;
            max-width: 400px;
            margin: 20px auto;
            padding: 15px;
            background-color: #f0f0f0;
            border: 1px solid #ccc;
            border-radius: 5px;
            box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
        }
        .result-window h3 {
            margin: 0 0 10px 0;
            font-size: 18px;
            color: #333;
        }
        .result-window p {
            margin: 5px 0;
            font-size: 16px;
            color: #555;
        }
        .graph-container {
            width: 90%;
            max-width: 800px;
            height: 400px;
            margin: 20px auto;
        }
        .button-container {
            display: flex;
            flex-wrap: wrap;
            justify-content: center;
            gap: 10px;
            margin: 20px auto;
        }
    </style>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
</head>
<body>
    <h1>Run Test Page</h1>

    <!-- Graph Container -->
    <div class="graph-container">
        <canvas id="liveGraph"></canvas>
    </div>

    <!-- Result Window -->
    <div class="result-window">
        <h3>Test Result</h3>
        <p><strong>Absorbance:</strong> <span id="absorbance">0.00</span></p>
        <p><strong>Concentration:</strong> <span id="concentration">0.00</span></p>
        <p><strong>Inference:</strong> <span id="inference">Low</span></p>
    </div>

    <!-- Buttons -->
    <div class="button-container">
        <button class="btn" onclick="sendCommand('water')">Water</button>
        <button class="btn" onclick="sendCommand('blank')">Blank</button>
        <button class="btn" onclick="sendCommand('standard')">Standard</button>
        <button class="btn" onclick="sendCommand('sample')">Sample</button>
        <button class="btn" onclick="sendCommand('wash')">Wash</button>
    </div>

    <script>
        // Initialize Chart.js
        const ctx = document.getElementById('liveGraph').getContext('2d');
        const liveGraph = new Chart(ctx, {
            type: 'line',
            data: {
                labels: [], // X-axis labels (time)
                datasets: [{
                    label: 'Absorbance',
                    data: [], // Y-axis data (absorbance values)
                    borderColor: '#007BFF',
                    borderWidth: 2,
                    fill: false
                }]
            },
            options: {
                scales: {
                    x: {
                        title: {
                            display: true,
                            text: 'Time (s)'
                        }
                    },
                    y: {
                        title: {
                            display: true,
                            text: 'Absorbance'
                        },
                        min: 0.8, // Set a fixed y-axis range for better visualization
                        max: 1.2
                    }
                },
                responsive: true,
                maintainAspectRatio: false
            }
        });

        // Function to calculate concentration from absorbance (Beer-Lambert Law)
        function calculateConcentration(absorbance) {
            const molarAbsorptivity = 1.0; // Example constant
            const pathLength = 1.0; // Example constant
            return (absorbance / (molarAbsorptivity * pathLength)).toFixed(2);
        }

        // Function to update the graph and result
        function updateGraphAndResult(time, absorbance) {
            // Calculate concentration
            const concentration = calculateConcentration(absorbance);

            // Update the graph
            liveGraph.data.labels.push(time);
            liveGraph.data.datasets[0].data.push(absorbance);
            liveGraph.update();

            // Update the result window
            document.getElementById('absorbance').textContent = absorbance.toFixed(2);
            document.getElementById('concentration').textContent = concentration;

            // Update inference (High or Low)
            const inference = concentration > 0.5 ? 'High' : 'Low'; // Example threshold
            document.getElementById('inference').textContent = inference;

            // Keep only the last 5 data points
            if (liveGraph.data.labels.length > 5) {
                liveGraph.data.labels.shift();
                liveGraph.data.datasets[0].data.shift();
            }
        }

        // Simulate live data with small, smooth variations
        let time = 0;
        const baselineAbsorbance = 1.0; // Baseline absorbance value
        const amplitude = 0.05; // Small amplitude for variations
        const frequency = 0.1; // Frequency of oscillations
        let intervalId;

        function startSimulation() {
            intervalId = setInterval(() => {
                time += 1;
                // Generate absorbance value with smooth variations
                const absorbance = baselineAbsorbance + amplitude * Math.sin(frequency * time);
                updateGraphAndResult(time, absorbance);

                // Stop after 5 seconds (5 readings)
                if (time >= 5) {
                    clearInterval(intervalId);
                    console.log("Simulation stopped after 5 seconds.");
                }
            }, 1000); // Update every 1 second
        }

        // Start the simulation
        startSimulation();

        // Function to send commands to the ESP32
        function sendCommand(command) {
            fetch('/' + command)
                .then(response => console.log(command + " executed"))
                .catch(error => console.error('Error:', error));
        }
    </script>
</body>
</html>
"""

# Handler for the main page
async def handle_main_page(request):
    return web.Response(text=MAIN_PAGE, content_type='text/html')

# Handler for the chemistry list page
async def handle_chemistry_list(request):
    return web.Response(text=CHEMISTRY_LIST_PAGE, content_type='text/html')

# Handler for the run test page
async def handle_run_test(request):
    return web.Response(text=RUN_TEST_PAGE, content_type='text/html')

# Handler for saving test data
async def handle_save_data(request):
    data = await request.json()
    with open("test_data.csv", "a") as f:
        f.write(f"{data['testName']},{data['testType']},{data['wavelength']},{data['temperature']},{data['lowFlag']},{data['highFlag']},{data['numReadings']},{data['r1Value']},{data['r2Value']}\n")
    return web.Response(text="Data saved successfully!", content_type='text/plain')

# Handler for creating the database file
async def handle_create_database(request):
    create_database_file()
    return web.Response(text="Database file created or verified successfully!", content_type='text/plain')

# Create the web application
app = web.Application()

# Add routes
app.router.add_get('/', handle_main_page)
app.router.add_get('/chemistry-list', handle_chemistry_list)
app.router.add_get('/run_test', handle_run_test)
app.router.add_post('/save-data', handle_save_data)
app.router.add_post('/create-database', handle_create_database)  # New route for creating the database

# Run the application
web.run_app(app, port=80)