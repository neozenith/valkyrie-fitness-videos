import vertexai
from vertexai.generative_models import GenerativeModel, Part
import os
import json
import argparse
import sys
import time

# --- Configuration ---
PROJECT_ID = "your-gcp-project-id"  # <--- REPLACE with your Project ID
LOCATION = "us-central1"

def list_target_prompts(exercises_file):
    """Prints all target .md file paths based on the JSON input."""
    try:
        with open(exercises_file, 'r') as f:
            exercises = json.load(f)
    except FileNotFoundError:
        return # Exit gracefully if file not found

    all_prompts = []
    for exercise_name in exercises:
        exercise_key = exercise_name.lower().replace(" ", "_")
        for lead_character in ["nesta", "cassian"]:
            for video_num in range(1, 6):
                filepath = f"scripts/{exercise_key}/prompt_{video_num:02d}_lead_{lead_character}.md"
                all_prompts.append(filepath)
    
    # Print all file paths on one line, separated by spaces
    print(" ".join(all_prompts))

def construct_meta_prompt(global_context, exercise_name, exercise_data, video_num, lead_character):
    """Constructs a detailed prompt for Gemini to generate a single markdown file."""
    
    banterer_character = "Nesta" if lead_character == "Cassian" else "Cassian"
    
    # Details for each specific video in the sequence
    video_details = {
        1: f"This is Video #1: The Challenge & The Standard. The Leader ({lead_character}) introduces the standard '{exercise_name}'. The Banterer ({banterer_character}) critiques them. Use the cues for the standard exercise: '{exercise_data['cues']['standard']}'",
        2: f"This is Video #2: The Concession & The Regression. The Banterer from video 1 ({banterer_character}) is now the Leader. They demonstrate the regression exercise: '{exercise_data['regression']}'. They must break the fourth wall. Use the cues for the regression: '{exercise_data['cues']['regression']}'",
        3: f"This is Video #3: The Escalation & The Boast. The original Leader ({lead_character}) reclaims the spotlight to demonstrate the progression exercise: '{exercise_data['progression']}'. Their dialogue is a boast. Use the cues for the progression: '{exercise_data['cues']['progression']}'",
        4: f"This is Video #4: The Silent Duel. There is NO dialogue. Describe the scene of {lead_character} and {banterer_character} performing the standard '{exercise_name}' side-by-side with intense competition and a moment of playful, slapstick sabotage.",
        5: f"This is Video #5: The Final Push. Both characters are tired but unified. One of them ({lead_character} or {banterer_character}) must break the fourth wall with a powerful, encouraging line to the user. The exercise is the standard '{exercise_name}'."
    }
    specific_instruction = video_details.get(video_num, "")

    # The prompt sent to the AI
    meta_prompt = f"""
    You are a creative scriptwriter for a fantasy-themed fitness app. Your task is to generate the complete content for a single markdown prompt file. This file will be used to generate an 8-second video.

    **GLOBAL CONTEXT AND DIRECTORIAL NOTES:**
    {global_context}

    **TASK FOR THIS FILE:**
    - Exercise Name: {exercise_name}
    - Lead Character for the overall 40s sequence: {lead_character}
    - Details for this specific 8-second video: {specific_instruction}

    Please generate the markdown content now. It should be a detailed, cinematic description of the scene, characters, action, and dialogue (if any). Do not write anything else, just the markdown content itself.
    """
    return meta_prompt

def generate_all_prompts(context_file, exercises_file):
    """Main function to generate all prompt files."""
    
    print("Loading context and exercise files...")
    try:
        with open(context_file, 'r') as f:
            global_context = f.read()
        with open(exercises_file, 'r') as f:
            exercises = json.load(f)
    except FileNotFoundError as e:
        print(f"Error: Could not find a required file. {e}", file=sys.stderr)
        sys.exit(1)

    print("Initializing Vertex AI...")
    vertexai.init(project=PROJECT_ID, location=LOCATION)
    model = GenerativeModel("gemini-1.5-pro-001") 

    for exercise_name, exercise_data in exercises.items():
        exercise_key = exercise_name.lower().replace(" ", "_")
        for lead_character in ["Nesta", "Cassian"]:
            char_key = lead_character.lower()
            for video_num in range(1, 6):
                output_dir = os.path.join("scripts", exercise_key)
                os.makedirs(output_dir, exist_ok=True)
                output_filename = f"prompt_{video_num:02d}_lead_{char_key}.md"
                output_filepath = os.path.join(output_dir, output_filename)
                
                print(f"--- Generating prompt for: {output_filepath} ---")
                meta_prompt = construct_meta_prompt(global_context, exercise_name, exercise_data, video_num, lead_character)
                
                try:
                    response = model.generate_content([Part.from_text(meta_prompt)])
                    generated_markdown = response.text
                    with open(output_filepath, 'w') as f:
                        f.write(generated_markdown)
                    print(f"Successfully created {output_filepath}")
                except Exception as e:
                    print(f"An error occurred calling the AI model for {output_filepath}: {e}", file=sys.stderr)
                time.sleep(2)

    print("\nAll prompt files have been generated!")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate or list markdown prompt files for video generation.")
    parser.add_argument("exercises_file", help="Path to the exercises.json file.")
    parser.add_argument("context_file", nargs='?', default=None, help="Path to the context.md file (only required for generation).")
    parser.add_argument("--list-outputs", action="store_true", help="List all potential prompt file paths without generating them.")
    
    args = parser.parse_args()
    
    if args.list_outputs:
        list_target_prompts(args.exercises_file)
    else:
        if not args.context_file:
            print("Error: context_file is required when not using --list-outputs.", file=sys.stderr)
            sys.exit(1)
        generate_all_prompts(args.context_file, args.exercises_file)