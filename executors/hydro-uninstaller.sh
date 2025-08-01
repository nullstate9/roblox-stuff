# hey gang
installLink='bash -c "$(curl -fsSL https://www.hydrogen.lat/install)"'

main() {
    clear
    echo "\033[1;33mWarning\033[0m: This is an \033[1;31munofficial\033[0m application created by @109dg."
    echo "Please note that the Uninstall and Reinstall both automatically reinstall ROBLOX to the latest version."
    sleep 1
    echo "Install Hydrogen:         Press 1"
    echo "Uninstall Hydrogen:       Press 2"
    echo "Reinstall Hydrogen:       Press 3"
    echo "Clean Uninstall:          Press 4"
    echo "Exit:                     Press Any Key"

    read -n 1 -s user_input
    
    if [ "$user_input" == "1" ]; then
        echo "[!] Installing Hydrogen"
        eval $installLink
        
    elif [ "$user_input" == "2" ]; then
        echo "[!] Uninstalling Hydrogen"

        if [ -d "/Applications/Hydrogen.app" ]; then
            echo "[-] Removing /Applications/Hydrogen.app..."
            rm -rf "/Applications/Hydrogen.app"
        else
            echo "[!] Hydrogen Application not found!"
        fi
        
        
        if [ -d "/Applications/Roblox.app" ]; then
            echo "[-] Removing /Applications/Roblox.app..."
            rm -rf "/Applications/Roblox.app"
        else
            echo "[!] Roblox app not found!"
        fi

        cd /tmp
        

        [ -f ./RobloxPlayer.zip ] && rm ./RobloxPlayer.zip

        arch=$(uname -m)
        
        if [[ "$arch" == "arm64" ]]; then
            echo "[!] Apple Silicon CPU Detected"
            echo "[+] Downloading Latest Roblox..."
            version=$(curl -s http://setup.roblox.com/mac/arm64/DeployHistory.txt | grep "New Client version" | tail -n 1 | sed -n 's/.*\(version-[^ ]*\).*/\1/p')
            curl -f --progress-bar "http://setup.rbxcdn.com/mac/arm64/{$version}-RobloxPlayer.zip" -o "./RobloxPlayer.zip"
        elif [[ "$arch" == "x86_64" ]]; then
            echo "[!] Intel CPU Detected"
            echo "[+] Downloading Latest Roblox..."
            version=$(curl -s http://setup.roblox.com/mac/DeployHistory.txt | grep "New Client version" | tail -n 1 | sed -n 's/.*\(version-[^ ]*\).*/\1/p')
            curl -f --progress-bar "http://setup.rbxcdn.com/mac/{$version}-RobloxPlayer.zip" -o "./RobloxPlayer.zip"
        else
            echo "Unknown architecture: $arch. Aborting"
            exit 1
        fi

        
        
        echo "[+] Installing Latest Roblox..."

        unzip -qo "./RobloxPlayer.zip"
        mv ./RobloxPlayer.app /Applications/Roblox.app
        rm ./RobloxPlayer.zip
        echo "[+] Uninstalled Hydrogen."
        echo "[+] Script by @109dg"
        echo "[-] Removing Hydro Uninstaller"
        cd
        rm -rf hydro-uninstaller.sh

        exit 0
        
    elif [ "$user_input" == "3" ]; then
        echo "Uninstalling Hydrogen"

        if [ -d "/Applications/Hydrogen.app" ]; then
            echo "[-] Removing /Applications/Hydrogen.app..."
            rm -rf "/Applications/Hydrogen.app"
        else
            echo "[!] Hydrogen Application not found!"
        fi
        
        if [ -d "/Applications/Roblox.app" ]; then
            echo "[-] Removing /Applications/Roblox.app..."
            rm -rf "/Applications/Roblox.app"
        else
            echo "[!] Roblox app not found!"
        fi

        

        cd /tmp

        [ -f ./RobloxPlayer.zip ] && rm ./RobloxPlayer.zip

        arch=$(uname -m)
        
        if [[ "$arch" == "arm64" ]]; then
            echo "[!] Apple Silicon CPU Detected"
            echo "[+] Downloading Latest Roblox..."
            version=$(curl -s http://setup.roblox.com/mac/arm64/DeployHistory.txt | grep "New Client version" | tail -n 1 | sed -n 's/.*\(version-[^ ]*\).*/\1/p')
            curl -f --progress-bar "http://setup.rbxcdn.com/mac/arm64/{$version}-RobloxPlayer.zip" -o "./RobloxPlayer.zip"
        elif [[ "$arch" == "x86_64" ]]; then
            echo "[!] Intel CPU Detected"
            echo "[+] Downloading Latest Roblox..."
            version=$(curl -s http://setup.roblox.com/mac/DeployHistory.txt | grep "New Client version" | tail -n 1 | sed -n 's/.*\(version-[^ ]*\).*/\1/p')
            curl -f --progress-bar "http://setup.rbxcdn.com/mac/{$version}-RobloxPlayer.zip" -o "./RobloxPlayer.zip"
        else
            echo "Unknown architecture: $arch. Aborting"
            exit 0
        fi
        
        echo "[+] Installing Latest Roblox..."

        unzip -qo "./RobloxPlayer.zip"
        mv ./RobloxPlayer.app /Applications/Roblox.app
        rm ./RobloxPlayer.zip

        sleep 1
        echo "[+] Reinstalling Hydrogen"

        eval $installLink

    elif [ "$user_input" == "4" ]; then
        echo "Performing clean uninstall"

        if [ -d "/Applications/Hydrogen.app" ]; then
            echo "[-] Removing /Applications/Hydrogen.app..."
            rm -rf "/Applications/Hydrogen.app"
        else
            echo "[!] Hydrogen Application not found!"
        fi
        
        if [ -d "/Applications/Roblox.app" ]; then
            echo "[-] Removing /Applications/Roblox.app..."
            rm -rf "/Applications/Roblox.app"
        else
            echo "[!] Roblox app not found!"
        fi

        echo "[-] Removing all files."
        if [ -d "~/Hydrogen" ]; then
            rm -rf "~/Hydrogen"
        fi

        if [ -d "~/Library/Application\ Support/Hydrogen" ]; then
            rm -rf "~/Library/Application\ Support/Hydrogen"
        fi

        if [ -d "~/Library/Application\ Support/Roblox" ]; then
            rm -rf "~/Library/Application\ Support/Roblox"
        fi

        cd /tmp

        [ -f ./RobloxPlayer.zip ] && rm ./RobloxPlayer.zip

        arch=$(uname -m)
        
        if [[ "$arch" == "arm64" ]]; then
            echo "[!] Apple Silicon CPU Detected"
            echo "[+] Downloading Latest Roblox..."
            version=$(curl -s http://setup.roblox.com/mac/arm64/DeployHistory.txt | grep "New Client version" | tail -n 1 | sed -n 's/.*\(version-[^ ]*\).*/\1/p')
            curl -f --progress-bar "http://setup.rbxcdn.com/mac/arm64/{$version}-RobloxPlayer.zip" -o "./RobloxPlayer.zip"
        elif [[ "$arch" == "x86_64" ]]; then
            echo "[!] Intel CPU Detected"
            echo "[+] Downloading Latest Roblox..."
            version=$(curl -s http://setup.roblox.com/mac/DeployHistory.txt | grep "New Client version" | tail -n 1 | sed -n 's/.*\(version-[^ ]*\).*/\1/p')
            curl -f --progress-bar "http://setup.rbxcdn.com/mac/{$version}-RobloxPlayer.zip" -o "./RobloxPlayer.zip"
        else
            echo "Unknown architecture: $arch. Aborting"
            exit 0
        fi
        
        echo "[+] Installing Latest Roblox..."

        unzip -qo "./RobloxPlayer.zip"
        mv ./RobloxPlayer.app /Applications/Roblox.app
        rm ./RobloxPlayer.zip

        sleep 1
        echo "[+] Reinstalling Hydrogen"
        
    else
        echo "Have a nice day!"
        rm -rf hydro-uninstaller.sh
        exit 0
    fi

    clear

}

main
