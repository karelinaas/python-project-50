def generate_diff(first_data: dict, second_data: dict) -> str:
    keys = sorted(set(first_data.keys()) | set(second_data.keys()))
    diff_lines = []
    
    for key in keys:
        if key in first_data and key not in second_data:
            diff_lines.append(f"  - {key}: {first_data[key]}")
        elif key not in first_data and key in second_data:
            diff_lines.append(f"  + {key}: {second_data[key]}")
        elif first_data[key] != second_data[key]:
            diff_lines.append(f"  - {key}: {first_data[key]}")
            diff_lines.append(f"  + {key}: {second_data[key]}")
        else:
            diff_lines.append(f"    {key}: {first_data[key]}")
    
    return "{\n" + "\n".join(diff_lines) + "\n}"
