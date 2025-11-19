import os
import zipfile
import shutil
import tempfile
import re

def remove_modify_password(input_path, output_path):
    """
    Remove 'modify password' protection from a PPTX file
    by deleting the <p:modifyVerifier ... /> tag in presentation.xml.
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        # Extract PPTX (which is just a ZIP archive)
        with zipfile.ZipFile(input_path, 'r') as zip_ref:
            zip_ref.extractall(tmpdir)

        pres_xml = os.path.join(tmpdir, "ppt", "presentation.xml")

        if os.path.exists(pres_xml):
            with open(pres_xml, "r", encoding="utf-8") as f:
                xml_data = f.read()

            # Remove modifyVerifier tag if it exists
            if "modifyVerifier" in xml_data:
                xml_data = re.sub(r'<p:modifyVerifier[^>]*/>', '', xml_data)

                with open(pres_xml, "w", encoding="utf-8") as f:
                    f.write(xml_data)

        # Repack into a new PPTX file
        with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as new_zip:
            for root, dirs, files in os.walk(tmpdir):
                for file in files:
                    abs_path = os.path.join(root, file)
                    rel_path = os.path.relpath(abs_path, tmpdir)
                    new_zip.write(abs_path, rel_path)


def process_folder(input_folder, output_folder):
    """
    Process all PPTX files in input_folder and save cleaned versions in output_folder
    with '_Unlock' appended to the filename.
    """
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for file_name in os.listdir(input_folder):
        if file_name.lower().endswith(".pptx"):
            input_path = os.path.join(input_folder, file_name)

            # Append _Unlock before extension
            base, ext = os.path.splitext(file_name)
            new_file_name = f"{base}_Unlock{ext}"
            output_path = os.path.join(output_folder, new_file_name)

            print(f"Processing: {file_name}")
            remove_modify_password(input_path, output_path)
            print(f"Saved cleaned file: {output_path}")


# === Usage ===
input_folder = "C:\\WorkingDirectory\\MACrawler\\Python\\PPT Encryption Remover\\ppts"
output_folder = "C:\\WorkingDirectory\\MACrawler\\Python\\PPT Encryption Remover\\unlock_ppts"

process_folder(input_folder, output_folder)
