import os
import glob

base_dir = r"D:\projects\emaillinggggggg\crawler"
output_file = os.path.join(base_dir, "ALL_FILES_COMBINED.txt")

# Collect all Python and JSON files
py_files = sorted(glob.glob(os.path.join(base_dir, "*.py")))
json_files = sorted(glob.glob(os.path.join(base_dir, "*.json")))
all_files = py_files + json_files

with open(output_file, "w", encoding="utf-8") as out:
    out.write(f"=== TOTAL COMBINED FILES: {len(all_files)} ===\n")
    out.write(f"Python Files: {len(py_files)} | JSON Files: {len(json_files)}\n\n")
    
    for f in all_files:
        if os.path.abspath(f) == os.path.abspath(output_file):
            continue
        fname = os.path.basename(f)
        out.write("=" * 80 + "\n")
        out.write(f"FILE: {fname}\n")
        out.write("=" * 80 + "\n\n")
        try:
            with open(f, "r", encoding="utf-8", errors="replace") as infile:
                out.write(infile.read())
        except Exception as e:
            out.write(f"ERROR READING FILE: {e}\n")
        out.write("\n\n")

print(f"Successfully combined {len(all_files)} files into: {output_file}")
print(f"File size: {os.path.getsize(output_file)} bytes")
