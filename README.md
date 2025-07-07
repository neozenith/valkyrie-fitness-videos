# Valkyrie Fitness Videos

This is part of a vibe coded project to create a silly fitness app themed after a romantacy book series.

Website: https://valkyrie-training.vercel.app/

## Overview

This project leverages Google Cloud's Vertex AI to generate fantasy-themed fitness tutorial videos featuring characters Nesta and Cassian. The pipeline creates:
1. Markdown prompt files using Gemini Pro 1.5
2. Video content using Veo (Imagine Video v3.0)

Each exercise has a series of 5 videos, creating a narrative arc that guides users through standard exercises, regressions, and progressions with engaging character interaction.

## Prerequisites

- Python 3.12 or higher
- Google Cloud account with Vertex AI enabled
- Google Cloud CLI installed and authenticated
- Google Cloud Project with Vertex AI API access

## Setup

### 1. Clone the Repository

```bash
git clone <repository-url>
cd valkyrie-fitness-videos
```

### 2. Set Up Python Environment

```bash
# Install uv (https://github.com/astral-sh/uv)
curl -sSf https://astral.sh/uv/install.sh | sh

# Sync dependencies and create virtual environment
uv sync
```

### 3. Set Up Google Cloud Authentication

```bash
# Install Google Cloud CLI if you haven't already
# Visit: https://cloud.google.com/sdk/docs/install

# Login to Google Cloud
gcloud auth login

# Set your project ID
gcloud config set project YOUR_PROJECT_ID

# Authenticate application default credentials
gcloud auth application-default login
```

### 4. Update Configuration

1. Open both Python scripts and update the `PROJECT_ID` variable with your Google Cloud project ID:
   ```python
   PROJECT_ID = "your-gcp-project-id"  # Replace with your actual Project ID
   ```

2. Create an `exercises.json` file with your exercise definitions:
   ```json
   {
     "Push Up": {
       "regression": "Knee Push Up",
       "progression": "Clapping Push Up",
       "cues": {
         "standard": "Keep your core tight, elbows at 45 degrees",
         "regression": "Maintain a straight line from knees to head",
         "progression": "Push explosively, land with soft elbows"
       }
     }
   }
   ```

## Usage

### Generate Prompt Files

```bash
# Generate all prompt files for exercises in exercises.json
make prompts

# Or run directly:
python create_prompts.py exercises.json context.md
```

This will create markdown files in the `scripts/` directory with detailed prompts for each video segment.

### Generate Videos

```bash
# Generate videos from all prompt files
make videos

# Or generate a specific video:
python generate_video.py scripts/push_up/prompt_01_lead_nesta.md
```

Generated videos will be saved in the `videos/` directory with corresponding names.

### Generate Everything

```bash
# Generate all prompts and then all videos
make all
```

## File Structure

```
valkyrie-fitness-videos/
├── context.md                  # Character and directorial guidelines
├── exercises.json              # Exercise definitions (create this)
├── create_prompts.py           # Script to generate prompt markdown files
├── generate_video.py           # Script to generate videos from prompts
├── Makefile                    # Automation tasks
├── scripts/                    # Generated prompt files (output)
│   └── exercise_name/
│       └── prompt_XX_lead_character.md
└── videos/                     # Generated video files (output)
    └── exercise_name/
        └── video_XX_lead_character.mp4
```

## Google Vertex AI Details

This project uses two key Vertex AI features:

1. **Gemini 1.5 Pro** for generating detailed text prompts
2. **Veo (Imagine Video v3.0)** for generating video content

### Vertex AI Setup Guide

1. **Create a Google Cloud Project**
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Create a new project or select an existing one

2. **Enable the Vertex AI API**
   - Go to "APIs & Services" > "Library"
   - Search for "Vertex AI API" and enable it

3. **Set up Authentication**
   - Create a service account with appropriate permissions
   - Download the JSON key file
   - Set the environment variable:
     ```bash
     export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your-service-account-key.json"
     ```
   - Or use application default credentials as described in the setup section

4. **Verify API Access**
   - The scripts will automatically check access when run
   - If you encounter permission issues, verify your service account has the "Vertex AI User" role

### Vertex AI Quota and Pricing Considerations

- Be aware of [Vertex AI quotas](https://cloud.google.com/vertex-ai/quotas) for your project
- Video generation can be costly - check [pricing](https://cloud.google.com/vertex-ai/pricing) before generating large batches
- Consider requesting quota increases if needed for production use

## Troubleshooting

### Common Issues

1. **Authentication Errors**
   - Ensure you've run `gcloud auth application-default login`
   - Verify your PROJECT_ID is set correctly

2. **API Access Errors**
   - Enable the Vertex AI API in your Google Cloud console
   - Verify your account has the necessary permissions

3. **Output Quality Issues**
   - Review and refine the context.md file
   - Experiment with exercise cues in exercises.json