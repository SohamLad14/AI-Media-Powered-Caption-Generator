# Caption Generator Module

This Drupal module generates AI-powered captions for images using Python scripts embedded within the module.

## Features

- Generates captions for uploaded images in article forms
- Uses embedded Python scripts (no external API required)
- Supports configurable caption length
- AJAX-powered caption generation

## Setup Instructions

### 1. Prerequisites

Ensure you have Python 3.x installed in your DDEV environment:

```bash
# SSH into DDEV
ddev ssh

# Check Python version
python3 --version

# Install required Python packages
pip3 install torch torchvision transformers pillow requests
```

### 2. Module Installation

1. Place the module in `web/modules/caption_generator/`
2. Enable the module:
   ```bash
   ddev drush en caption_generator -y
   ```

### 3. Python Environment Setup

The module requires the `caption-generating-api` directory to be present at the same level as the `web` directory:

```
d10-site/
├── caption-generating-api/  # Your Python API files
├── web/
│   └── modules/
│       └── caption_generator/
└── ...
```

### 4. Testing the Setup

Run the test script to verify everything is working:

```bash
ddev ssh
cd /var/www/html/web/modules/caption_generator
drush php-script test_python_env.php
```

### 5. Usage

1. Create or edit an article with an image field
2. Upload an image
3. Click "Generate Caption" button
4. The caption will be generated using AI

## Troubleshooting

### Python Not Found
If Python is not available in DDEV:
```bash
ddev ssh
apt-get update
apt-get install python3 python3-pip
```

### Missing Python Packages
Install required packages:
```bash
ddev ssh
pip3 install torch torchvision transformers pillow requests
```

### Permission Issues
Make sure the Python script is executable:
```bash
ddev ssh
chmod +x /var/www/html/web/modules/caption_generator/caption_generator_python.py
```

### API Directory Not Found
Ensure the `caption-generating-api` directory exists and contains:
- `vision.py`
- `caption.py`
- `enhancer.py`

## File Structure

```
caption_generator/
├── caption_generator.info.yml
├── caption_generator.module
├── caption_generator.services.yml
├── caption_generator_python.py    # Embedded Python script
├── test_python_env.php           # Test script
├── README.md
└── src/
    └── Service/
        ├── PythonApiService.php   # Legacy HTTP API service
        └── CaptionGeneratorService.php  # New embedded service
```

## How It Works

1. When a user clicks "Generate Caption", the AJAX callback is triggered
2. The `CaptionGeneratorService` executes the embedded Python script
3. The Python script imports modules from the `caption-generating-api` directory
4. The script generates a caption and returns it as JSON
5. The caption is displayed in the form field

## Security Notes

- The Python script runs with the same permissions as the web server
- File paths are properly escaped to prevent command injection
- Input validation is performed on both PHP and Python sides 