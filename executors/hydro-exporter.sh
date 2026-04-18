#!/bin/bash

OPIUM_DIR="$HOME/Opiumware"
COMET_DIR="$HOME/Library/Application Support/com.comet.dev"
WORKSPACES_DIR="$COMET_DIR/workspaces" # hydrogen tabs
SCRIPTS_DIR="$COMET_DIR/scripts" # hydrogen autoexec
EDITOR_JSON="$OPIUM_DIR/editor.json"
AUTOEXEC_DIR="$OPIUM_DIR/autoexec"

echo "Exporting Hydrogen Files to Opiumware"

if [ ! -d "$OPIUM_DIR" ]; then
    echo "Error: Opiumware not installed ($OPIUM_DIR)"
    exit 1
fi

if [ ! -d "$COMET_DIR" ]; then
    echo "Error: Hydrogen Comet UI Directory not found ($COMET_DIR)"
    exit 1
fi

if ! command -v jq >/dev/null 2>&1; then
    echo "jq not found. Downloading..."
    ARCH=$(uname -m)
    case $ARCH in
        arm64)  JQ_URL="https://github.com/jqlang/jq/releases/latest/download/jq-macos-arm64" ;;
        x86_64) JQ_URL="https://github.com/jqlang/jq/releases/latest/download/jq-macos-amd64" ;;
        *) echo "Error: Unsupported architecture: $ARCH"; exit 1 ;;
    esac
    curl -L -s -o /tmp/jq "$JQ_URL"
    chmod +x /tmp/jq
    JQ="/tmp/jq"
else
    JQ="jq"
fi

if [ ! -f "$EDITOR_JSON" ]; then
    echo "Error: editor.json not found"
    exit 1
fi

PROJECT_PATH=$($JQ -r '.projectPath // empty' "$EDITOR_JSON")

if [ -z "$PROJECT_PATH" ] || [ "$PROJECT_PATH" = "null" ]; then
    echo "Error: Project Path not found. Please reinstall/start Opiumware"
    exit 1
fi

echo "Project path: $PROJECT_PATH"
mkdir -p "$AUTOEXEC_DIR"

echo -e "\nCopying Tabs"

if [ ! -d "$WORKSPACES_DIR" ]; then
    echo "No workspaces directory found."
else
    for workspace in "$WORKSPACES_DIR"/*/ ; do
        [ -d "$workspace" ] || continue
        
        folder_name=$(basename "$workspace")
        tabs_dir="${workspace}tabs"
        target_dir="$PROJECT_PATH/$folder_name"
        
        if [ ! -d "$target_dir" ]; then
            mkdir -p "$target_dir"
            echo "Created folder: $folder_name"
        else
            echo "Folder $folder_name already exists."
        fi
        
        if [ -d "$tabs_dir" ]; then
            while IFS= read -r -d '' file; do
                if [ -f "$file" ]; then
                    filename=$(basename "$file")
                    
                    if [ "$filename" = "state.json" ]; then
                        continue
                    fi
                    
                    target_file="$target_dir/$filename"
                    
                    if [ ! -f "$target_file" ]; then
                        cp "$file" "$target_file"
                        echo "Copying $folder_name/$filename"
                    else
                        echo "Error: $folder_name/$filename Found. Skipping"
                    fi
                fi
            done < <(find "$tabs_dir" -maxdepth 1 -type f -print0)
        else
            echo "No tabs folder found in $folder_name"
        fi
    done
fi

echo -e "\nCopying Autoexecute Scripts"

if [ -d "$SCRIPTS_DIR" ]; then
    while IFS= read -r -d '' script; do
        if [ -f "$script" ]; then
            script_name=$(basename "$script")
            target="$AUTOEXEC_DIR/$script_name"
            
            if [ ! -f "$target" ]; then
                cp "$script" "$target"
                echo "Copying to Autoexec: $script_name"
            else
                echo "Error: Autoexec/$script_name Found. Skipping"
            fi
        fi
    done < <(find "$SCRIPTS_DIR" -maxdepth 1 -type f -print0)
fi

echo -e "\nExport Complete. Created by 109dg"
