import os
import csv
from datetime import datetime
from aiohttp import web

# Function to create or verify the database file
def create_database_file(test_name):
    filename = "Database.csv"
    header = ["timestamp", "test name", "water", "blank", "standard", "sample"]
    
    # Get the current timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Check if file exists
    if not os.path.exists(filename):
        with open(filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(header)  # Write header row
            writer.writerow([timestamp, test_name, "", "", "", ""])  # Write the first row with test name
        print(f"{filename} created with header and test name.")
    else:
        # Append the new test name and timestamp to the file
        with open(filename, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([timestamp, test_name, "", "", "", ""])
        print(f"Test name '{test_name}' added to {filename}.")

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

            // Send the test name to the server to save it to the database
            fetch('/create-database', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ testName: testName })  // Send the test name to the server
            })
            .then(response => {
                if (response.ok) {
                    // Proceed to save the rest of the test data
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
                } else {
                    alert("Error saving test name to database");
                }
            })
            .catch(error => {
                alert("Error saving test name to database: " + error);
            });
        }

        function deleteTest(button) {
            button.parentElement.remove();
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

# Handler for saving test data
async def handle_save_data(request):
    data = await request.json()
    with open("test_data.csv", "a") as f:
        f.write(f"{data['testName']},{data['testType']},{data['wavelength']},{data['temperature']},{data['lowFlag']},{data['highFlag']},{data['numReadings']},{data['r1Value']},{data['r2Value']}\n")
    return web.Response(text="Data saved successfully!", content_type='text/plain')

# Handler for creating the database file
async def handle_create_database(request):
    data = await request.json()  # Get the test name from the frontend
    test_name = data.get("testName", "Unnamed Test")  # Default to "Unnamed Test" if no name is provided
    create_database_file(test_name)  # Save the test name and timestamp to the database
    return web.Response(text=f"Test '{test_name}' saved to database!", content_type='text/plain')

# Create the web application
app = web.Application()

# Add routes
app.router.add_get('/', handle_main_page)
app.router.add_get('/chemistry-list', handle_chemistry_list)
app.router.add_post('/save-data', handle_save_data)
app.router.add_post('/create-database', handle_create_database)  # New route for creating the database

# Run the application
web.run_app(app, port=80)