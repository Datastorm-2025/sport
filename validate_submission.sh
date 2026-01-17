#!/bin/bash

set -e

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INPUT_DIR="$SCRIPT_DIR/example/input"
OUTPUT_DIR="$SCRIPT_DIR/example/output"
OUTPUT_FILE="$OUTPUT_DIR/submission.csv"
TEAM="your_team"
DOMAIN="222.255.250.24:8001"
IMAGE_NAME="$DOMAIN/$TEAM/submission"
# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'

echo "Step 1: Checking Docker installation..."
if ! command -v docker &> /dev/null; then
    echo -e "${RED}ERROR: Docker is not installed or not in PATH${NC}"
    echo "Please install Docker first: https://docs.docker.com/get-docker/"
    exit 1
fi
echo -e "${GREEN}✓ Docker is installed${NC}"
echo ""

echo "Step 2: Checking input..."
[ ! -d "$INPUT_DIR" ] && echo -e "${RED}Error: Input directory not found${NC}" && exit 1
VIDEO_COUNT=$(find "$INPUT_DIR" -type f \( -name "*.mov" -o -name "*.mp4" -o -name "*.avi" \) | wc -l)
[ "$VIDEO_COUNT" -eq 0 ] && echo -e "${RED}Error: No videos in input${NC}" && exit 1
echo -e "${GREEN}✓ Found $VIDEO_COUNT videos${NC}"

mkdir -p "$OUTPUT_DIR"
rm -f "$OUTPUT_FILE"

echo "Step 3: Building Docker image..."
DOCKER_BUILDKIT=0 docker build -t "$IMAGE_NAME" "$SCRIPT_DIR"
echo -e "${GREEN}✓ Build successful${NC}"

echo "Step 4: Running inference..."
docker run --rm --network none --gpus '"device=0"'\
    -v "$INPUT_DIR:/data/input" \
    -v "$OUTPUT_DIR:/data/output" \
    -e INPUT_PATH=/data/input \
    -e OUTPUT_PATH=/data/output \
    "$IMAGE_NAME" > /dev/null
echo -e "${GREEN}✓ Inference complete${NC}"


echo "Step 5: Validating output..."
[ ! -f "$OUTPUT_FILE" ] && echo -e "${RED}Error: Output file not found${NC}" && exit 1

HEADER=$(head -n 1 "$OUTPUT_FILE" | tr -d '\r\n')
if [ "$HEADER" != "file_name,score" ]; then
    echo -e "${RED}Error: Invalid header. Expected 'file_name,score', got '$HEADER'${NC}"
    exit 1
fi

VALID_BANDS=("band_1_2" "band_2_4" "band_4_6" "band_6_8" "band_8_10")
INVALID_CLASSES=$(tail -n +2 "$OUTPUT_FILE" | cut -d',' -f2 | sort -u | while read -r class; do
    class=$(echo "$class" | tr -d '\r\n')
    valid=false
    for band in "${VALID_BANDS[@]}"; do
        if [ "$class" == "$band" ]; then
            valid=true
            break
        fi
    done
    if [ "$valid" == "false" ]; then
        echo "$class"
    fi
done)

if [ ! -z "$INVALID_CLASSES" ]; then
    echo -e "${RED}Error: Invalid classes found:${NC}"
    echo "$INVALID_CLASSES"
    echo -e "${RED}Valid classes are: ${VALID_BANDS[@]}${NC}"
    exit 1
fi

LINE_COUNT=$(wc -l < "$OUTPUT_FILE")
PREDICTION_COUNT=$((LINE_COUNT - 1))
echo -e "${GREEN}✓ Generated $PREDICTION_COUNT predictions${NC}"

echo -e "${GREEN}---------------------------------------------${NC}"
echo -e "${GREEN}You can submit your Docker image now! ${NC}"
echo -e "${GREEN}---------------------------------------------${NC}"
echo -e "${GREEN}To submit your Docker image, run:${NC}"
echo -e "${GREEN}   docker push 222.255.250.24:8001/$TEAM/submission${NC}"
echo -e "${GREEN}---------------------------------------------${NC}"