import os
import subprocess
import shutil

def run_separation(input_path, output_dir):
    """
    Executes the Demucs AI separation.
    """
    # -n htdemucs: Uses the high-quality transformer model
    # -d cpu: Forces CPU mode (Render free/starter tiers don't have GPUs)
    command = [
        "demucs",
        "-n", "htdemucs",
        "--out", output_dir,
        input_path
    ]

    try:
        # Run the AI
        print(f"Starting AI separation for: {input_path}")
        subprocess.run(command, check=True)
        
        # Identify the folder where demucs put the files
        # Demucs structure: output_dir/htdemucs/filename/*.wav
        filename = os.path.splitext(os.path.basename(input_path))[0]
        result_path = os.path.join(output_dir, "htdemucs", filename)
        
        return {
            "success": True,
            "path": result_path,
            "stems": ["vocals", "drums", "bass", "other"]
        }
    except Exception as e:
        print(f"AI Error: {str(e)}")
        return {"success": False, "error": str(e)}