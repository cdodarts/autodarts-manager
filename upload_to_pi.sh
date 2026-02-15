#!/bin/bash
# Upload autodarts-manager to cdo-vertex Pi

PI_HOST="cdo-vertex@cdo-vertex.local"
REMOTE_DIR="/opt/autodarts-manager"

echo "=========================================="
echo "Uploading autodarts-manager to Pi"
echo "=========================================="

# Create directory structure on Pi
echo ""
echo "[1/3] Creating directory structure..."
ssh ${PI_HOST} "sudo mkdir -p ${REMOTE_DIR}/{config,scripts,services,docs,examples} && sudo chown -R cdo-vertex:cdo-vertex ${REMOTE_DIR}"

# Upload config files
echo ""
echo "[2/3] Uploading files..."
echo "  - Config files..."
scp config/* ${PI_HOST}:${REMOTE_DIR}/config/

echo "  - Scripts..."
scp scripts/* ${PI_HOST}:${REMOTE_DIR}/scripts/

echo "  - Documentation..."
scp docs/* ${PI_HOST}:${REMOTE_DIR}/docs/

echo "  - Examples..."
scp examples/* ${PI_HOST}:${REMOTE_DIR}/examples/

echo "  - Root files..."
scp Makefile __init__.py ${PI_HOST}:${REMOTE_DIR}/

# Set permissions
echo ""
echo "[3/3] Setting permissions..."
ssh ${PI_HOST} "chmod +x ${REMOTE_DIR}/scripts/*.py"

echo ""
echo "=========================================="
echo "✓ Upload complete!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "  ssh ${PI_HOST}"
echo "  cd ${REMOTE_DIR}"
echo "  sudo python3 scripts/setup.py"
echo ""
