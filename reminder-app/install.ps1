# Function to check if Python is installed and return version
function Check-Python {
    try {
        $version = py --version 2>&1
        if ($version -match 'Python') {
            return $version
        } else {
            return $null
        }
    } catch {
        return $null
    }
}

# Set the Python version and URLs
$pythonVersion = "3.9.2"
$installerUrl = "https://www.python.org/ftp/python/$pythonVersion/python-$pythonVersion-amd64.exe"
$installerPath = "$env:USERPROFILE\Downloads\python-$pythonVersion-amd64.exe"
$zipUrl = "https://enspiredjack.com/crap/reminderapp_gui.zip"
$zipPath = "$env:USERPROFILE\Downloads\reminderapp_gui.zip"
$extractPath = "$env:USERPROFILE\Downloads"

# Check if Python is installed
if (-not (Check-Python)) {
    # Download Python installer
    Invoke-WebRequest -Uri $installerUrl -OutFile $installerPath
    # Install Python silently
    Start-Process -FilePath $installerPath -ArgumentList '/quiet InstallAllUsers=1 PrependPath=1' -Wait -NoNewWindow
    # Remove the installer
    Remove-Item -Path $installerPath
}

# Ensure pip is up-to-date
py -m pip install --upgrade pip

# Install required pip packages
$packages = "tkcalendar schedule plyer" # Add your required packages here, separated by commas
py -m pip install $packages

# Check if the ZIP file exists and download if not
if (-not (Test-Path $zipPath)) {
    Invoke-WebRequest -Uri $zipUrl -OutFile $zipPath
}

# Extract the ZIP file
Expand-Archive -Path $zipPath -DestinationPath $extractPath -Force

# Determine script path from extracted files
$scriptPath = (Get-ChildItem -Path $extractPath -Filter "*.py").FullName

# Run the Python script
& py $scriptPath

# Minimize PowerShell Window
Add-Type -AssemblyName System.Windows.Forms
[System.Windows.Forms.SendKeys]::SendWait('%{n}')