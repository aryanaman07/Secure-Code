# Secure-Code

## Entitlement Conflict Detection System Documentation

### Section 1: Methodology

#### Problem-Solving Methodology
The Entitlement Conflict Detection System prevents users from being given conflicting rights of access by direct or indirect roles. The process involves the following major steps:

- Load data from multiple sources as required.
- Map privileges to entitlements in a systematic way.
- Assign roles to privileges and specify how roles are related to one another.
- Map users to their corresponding roles, including inherited roles based on the hierarchy.
- Compare entitlements to segregation of duties (SoD) rules to detect potential conflicts.
- Generate a comprehensive report highlighting detected conflicts.

#### Flowchart
```
Load Data → Map Entitlements → Map Privileges → Map Users → Detect Conflicts → Generate Report
```

### Section 2: Function Descriptions

#### Data Loading
Data is pulled from several Excel files using Pandas. The system normalizes formats for consistency across data sources.

#### Core Algorithm
- **Entitlement Mapping**: Converts privilege codes to useful entitlement descriptions.
- **Privilege-to-Role Mapping**: Maps privileges to particular roles.
- **User-to-Role Mapping**: Identifies roles assigned to users, considering both direct and indirect roles.
- **Conflict Detection**: Compares user entitlements against SoD rules and flags violations.

#### Helper Functions
- Generates user and role information reports for easy reference.
- Verifies data integrity by checking privilege-role-entitlement relationships.
- Stores identified conflicts in an Excel report for easy review.

### Section 3: Testing Methodology

#### Testing Strategy
- **Unit Testing**: Functions were tested with controlled datasets to validate correct mappings.
- **Validation Against Known Test Cases**: The system was executed with test data containing predetermined SoD violations, and results were verified against expected outputs.

#### Debugging Techniques
- Sample mappings were printed to ensure correct privilege-role-entitlement relationships.
- Data integrity checks were performed using Pandas functions.
- Missing values and inconsistencies were handled through data normalization.

### Section 4: Setup and Execution Instructions

#### Prerequisites
Ensure Docker is installed for containerized execution. If executing locally, install Python 3.8+ and the necessary dependencies.

#### Running with Docker
```sh
# Build the Docker image
docker build -t entitlement_conflict_detector .

# Run the container
docker run --rm -v $(pwd)/data:/app/data entitlement_conflict_detector
```
The conflict report will be available in the `data` directory as `Conflict_Report.xlsx`.

#### Running Locally
```sh
# Install dependencies
pip install pandas openpyxl

# Run the script
python main.py
```
The conflict report will be generated as `Conflict_Report.xlsx`. 
