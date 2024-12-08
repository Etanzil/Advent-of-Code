# Function to check if a report is safe
def is_safe(report):
    # Convert the report into a list of integers
    levels = list(map(int, report.split()))
    
    # Check if the levels are strictly increasing or strictly decreasing
    is_increasing = all(levels[i] < levels[i + 1] for i in range(len(levels) - 1))
    is_decreasing = all(levels[i] > levels[i + 1] for i in range(len(levels) - 1))
    
    # Check if the difference between adjacent levels is between 1 and 3
    valid_differences = all(1 <= abs(levels[i] - levels[i + 1]) <= 3 for i in range(len(levels) - 1))
    
    # A report is safe if it is either all increasing or all decreasing
    # AND the differences are valid
    return (is_increasing or is_decreasing) and valid_differences

# Function to check if a report can be made safe by removing one level
def is_safe_with_dampener(report):
    levels = list(map(int, report.split()))
    
    # Try removing each level and checking if the remaining levels are safe
    for i in range(len(levels)):
        reduced_report = levels[:i] + levels[i + 1:]  # Remove the ith level
        if is_safe(" ".join(map(str, reduced_report))):  # Check if the reduced report is safe
            return True
    
    return False

# Main function to analyze the input data
def analyze_data(file_path):
    with open(file_path, 'r') as file:
        reports = file.readlines()
    
    # Count safe reports (without dampener)
    safe_reports_count = sum(1 for report in reports if is_safe(report.strip()))
    
    # Count safe reports (with dampener)
    safe_reports_with_dampener_count = sum(
        1 for report in reports if is_safe(report.strip()) or is_safe_with_dampener(report.strip())
    )
    
    return safe_reports_count, safe_reports_with_dampener_count

# Usage
if __name__ == "__main__":
    # Replace 'day2.txt' with your input file name
    file_path = 'day2.txt'
    safe_reports, safe_reports_with_dampener = analyze_data(file_path)
    print(f"Number of safe reports (without Problem Dampener): {safe_reports}")
    print(f"Number of safe reports (with Problem Dampener): {safe_reports_with_dampener}")
