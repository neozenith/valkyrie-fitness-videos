import vertexai
from vertexai.preview.vision_models import VideoGenerationModel
import base64
import os
import argparse
import sys

# --- Configuration ---
PROJECT_ID = "valkyrie-fitness"  # <--- REPLACE with your Project ID
LOCATION = "us-central1"           # Veo is available in specific regions

def generate_video_from_prompt_file(prompt_file_path: str):
    """
    Generates a video based on a prompt from a specified markdown file.
    """
    # --- 1. Validate and Read the Prompt File ---
    print(f"Loading prompt from: {prompt_file_path}")
    try:
        with open(prompt_file_path, "r") as f:
            prompt_from_file = f.read()
    except FileNotFoundError:
        print(f"Error: Prompt file not found at '{prompt_file_path}'", file=sys.stderr)
        sys.exit(1)

    # --- 2. Determine the Output Path (NEW LOGIC) ---
    # Example Input:  scripts/push_up/prompt_03_lead_cassian.md
    # Desired Output: videos/push_up/video_03_lead_cassian.mp4

    # Get the directory and filename from the input path
    input_dir, input_filename = os.path.split(prompt_file_path)
    
    # Create the new output directory path by replacing 'scripts' with 'videos'
    output_dir = input_dir.replace("scripts", "videos", 1)

    # Create the new output filename by replacing 'prompt' with 'video'
    output_filename = input_filename.replace("prompt", "video", 1)
    # And change the extension from .md to .mp4
    output_filename = os.path.splitext(output_filename)[0] + ".mp4"

    # Join them to create the full output path
    output_file_path = os.path.join(output_dir, output_filename)
    
    # Ensure the final output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"Video will be saved to: {output_file_path}")


    # --- 3. Initialize Vertex AI ---
    try:
        vertexai.init(project=PROJECT_ID, location=LOCATION)
    except Exception as e:
        print(f"Error initializing Vertex AI: {e}", file=sys.stderr)
        print("Please ensure your Project ID is correct and you are authenticated.", file=sys.stderr)
        sys.exit(1)

    # --- 4. Generate the Video ---
    print("Instantiating Veo model...")
    model = VideoGenerationModel.from_pretrained("imagine-video-v3.0-hd-generate@1")

    print("Generating video... This may take a few minutes.")
    try:
        response = model.generate(
            prompt=prompt_from_file,
            duration_sec=8.0,
        )
        print("Video generated successfully!")

        # --- 5. Save the Video File ---
        video_data_base64 = response.videos_base64[0]
        video_data = base64.b64decode(video_data_base64)

        with open(output_file_path, "wb") as f:
            f.write(video_data)
        
        print(f"Success! Video saved to: {output_file_path}")

    except Exception as e:
        print(f"An error occurred during video generation: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate a video from a markdown prompt file using Vertex AI.")
    parser.add_argument("prompt_file", help="The full path to the markdown prompt file.")
    
    args = parser.parse_args()
    
    generate_video_from_prompt_file(args.prompt_file)