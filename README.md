**# HELIX Clinical Data Management System

## 📋 Project Overview
HelixSoft Technologies has developed a bespoke FTP-based clinical data management system for Port Avalon General Hospital (PAGH) to securely retrieve, validate, and archive experimental drug-testing results from pharmaceutical partners.

## 🎯 Assignment Scenario
Port Avalon General Hospital's Department of Clinical Trials receives sensitive clinical trial data via a legacy FTP server. This interim solution provides secure data validation and archival capabilities until the pharmaceutical partner transitions to modern API-based integration.

### 🚨 Known Data Quality Issues
The system addresses these recurring deficiencies in submitted CSV files:
- Non-conformant filename structures
- Negative or non-numeric dosage values
- Anomalous date ranges (EndDate before StartDate)
- Invalid Outcome classifications (must be: "Improved", "No Change", "Worsened")
- Omission of mandatory fields (Outcome, Analyst, SideEffects)
- Intra-file record duplication
- Corrupted or empty file submissions
- Malformed CSV syntax

## ✨ System Capabilities

### 1. FTP Connection Management
- Manual establishment/termination of FTP sessions via GUI
- Visual connection state indicators (connected/disconnected)
- Persistent session maintenance

### 2. File Discovery and Selection
- Retrieval and display of available CSV files from remote server
- Real-time filename search with user feedback
- Single-file selection mechanism

### 3. Validation Engine
Executes sequential validation checks:
- Filename pattern compliance (`CLINICALDATAYYYYMMDDHHMMSS.CSV`)
- Header structure validation against 9-field schema
- Per-record validation:
  - Dosage positivity and integer format
  - StartDate/EndDate format compliance (YYYY-MM-DD) and chronological integrity
  - Outcome value conformity to permitted values
  - Field completeness assessment
  - Duplicate record detection within files

### 4. Intelligent Archival
- **Valid files**: Transferred to Archive directory with current-date suffix
- **Invalid files**: Relocated to Errors directory with original filename preservation

### 5. Duplicate Prevention
- Maintains processed-files log to prevent re-processing
- Enforcement at both file-level and intra-record level

### 6. Error Logging and Audit
- Generates detailed error reports in dedicated log file
- Assigns unique UUID4 GUIDs to each error entry via external API
- Log entries contain: timestamp, GUID, filename, and specific error diagnostics

### 7. Workspace Management
- Refresh function to reload server file manifest and clear filters

## 🏗️ Project Structure
Based on the provided file structure:

```
HELIX/
├── .github/workflows/
│   └── ci-cd.yml                 # CI/CD Pipeline Configuration
├── clinical_trials/              # Clinical trial data handling
├── Filename Validation/
│   ├── test_filename_validation_green.py
│   ├── test_filename_validation_red.py
│   └── test_filename_validation_refactor.py
├── sample_test_files/            # Test data samples
├── test_samples/
│   ├── docker-compose.yml        # Container orchestration
│   ├── Dockerfile               # Containerization
│   └── Helix.py                 # Main application
├── requirements.txt              # Python dependencies
├── test_csv_validation_automated.py
├── test_csv_validation.py
├── test_ftp_connection.py
├── test_uuid_api_integration.py
└── test_uuid_integration.py
```

## 🛠️ Technical Implementation

### Design Patterns Implemented
- **Strategy Pattern**: Modular validation strategies for different data types
- **TDD Approach**: Comprehensive test suite with red/green/refactor cycles
- **GUI Principles**: Modern interface following recognized UI/UX principles

### Key Features
- **Modular Validation**: Separate strategies for filename, header, dosage, date, and outcome validation
- **External API Integration**: UUID generation via https://www.uuidtools.com/api/generate/v4
- **Containerization**: Docker support for deployment consistency
- **CI/CD Pipeline**: Automated testing and deployment workflows
- **Comprehensive Logging**: Detailed error tracking with GUIDs for auditability

### File Validation Requirements
- **Filename Pattern**: `CLINICALDATAYYYYMMDDHHMMSS.CSV`
- **Required Fields**: PatientID, TrialCode, DrugCode, Dosage_mg, StartDate, EndDate, Outcome, SideEffects, Analyst
- **Date Format**: YYYY-MM-DD
- **Valid Outcomes**: "Improved", "No Change", "Worsened"
- **Dosage**: Must be positive integer

## 📁 Directory Structure
The system creates and manages these local directories:
- **Downloads**: Temporary storage for retrieved files
- **Archive**: Storage for validated files (with date suffix)
- **Errors**: Storage for invalid files with error logs

## 🔧 Setup and Usage
1. Configure FTP connection parameters (host, username, password)
2. Connect to the FTP server using the GUI interface
3. Browse and select CSV files from the server
4. Validate individual files or process them directly
5. Monitor progress and errors through the processing log

## 🧪 Testing Approach
The project follows Test-Driven Development (TDD) with:
- Unit tests for validation components
- Integration tests for FTP connectivity
- API integration tests for UUID generation
- Automated test data generation scripts

## 🚀 Deployment
The system supports:
- **Containerized deployment** via Docker and Docker Compose
- **CI/CD pipeline** for automated testing and deployment
- **Version control** through Git repository management

## 📊 Error Handling
All validation failures generate comprehensive error reports with:
- ISO 8601 timestamp
- Unique UUID4 identifier
- Source filename
- Specific error description

This ensures complete auditability and facilitates communication with pharmaceutical partners regarding data quality issues.**
