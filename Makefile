# Makefile for the Valkyrie Training Video Pipeline

# --- Variables ---
PYTHON := python3

# Input files
CONTEXT_FILE := context.md
EXERCISES_FILE := exercises.json

# Scripts
PROMPT_GENERATOR := create_prompts.py
VIDEO_GENERATOR := generate_video.py

# --- Dynamic File Lists ---
# Generate the list of all .md files that NEED to be created by calling our script with the --list-outputs flag
PROMPTS := $(shell $(PYTHON) $(PROMPT_GENERATOR) $(EXERCISES_FILE) --list-outputs)

# Automatically generate the list of all final .mp4 video files based on the prompt list
VIDEOS := $(patsubst scripts/%.md,videos/%.mp4,$(PROMPTS))


# --- Targets ---
.PHONY: all prompts videos clean

# The default target, executed when you just type "make"
all: $(VIDEOS)

# A target to generate just the markdown prompts.
prompts: $(PROMPTS)

# A target to generate just the videos, assuming prompts exist.
videos: $(VIDEOS)

# This rule tells 'make' how to generate ANY single prompt file.
$(PROMPTS): | prompts_sentinel

# This rule runs the main prompt generator script.
prompts_sentinel: $(PROMPT_GENERATOR) $(CONTEXT_FILE) $(EXERCISES_FILE)
	@echo "--- Generating all markdown prompt files... ---"
	$(PYTHON) $(PROMPT_GENERATOR) $(EXERCISES_FILE) $(CONTEXT_FILE)
	@touch prompts_sentinel

# This rule tells 'make' how to generate ANY single video file.
videos/%.mp4: scripts/%.md
	@echo "--- Generating video for $< ---"
	$(PYTHON) $(VIDEO_GENERATOR) $<

# A target to clean up all generated files.
clean:
	@echo "--- Cleaning up generated files... ---"
	-rm -rf scripts videos prompts_sentinel