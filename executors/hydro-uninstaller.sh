# hey gang

main() {
    clear
    echo "\033[1;33mWarning\033[0m: This is an \033[1;31munofficial\033[0m application created by @109dg."
    sleep 1
    echo "Install Hydrogen-M:         Press 1"
    echo "Uninstall Hydrogen-M:       Press 2"
    echo "Exit:                       Press Any Key"

    read -n 1 -s user_input

    if [ "$user_input" == "1" ]; then
        echo "Join the Discord Server to Install Hydrogen (#macos-updates)"
        
    elif [ "$user_input" == "2" ]; then
        echo "Uninstalling Hydrogen-M"

        if [ -d "/Applications/Hydrogen-M.app" ]; then
            echo "[-] Removing /Applications/Hydrogen-M.app..."
            rm -rf "/Applications/Hydrogen-M.app"
        else
            echo "[!] Hydrogen Application not found!"
        fi
        
        if [ -d "~/Hydrogen" ]; then
            echo "[-] Removing ~/Hydrogen..."
            rm -rf "~/Hydrogen"
        else
            echo "[!] Hydrogen folder not found!"
        fi
        
        if [ -d "/Applications/Roblox.app" ]; then
            echo "[-] Removing /Applications/Roblox.app..."
            rm -rf "/Applications/Roblox.app"
        else
            echo "[!] Roblox app not found!"
        fi

        

        cd /tmp
        echo "[+] Downloading Latest Roblox..."

        [ -f ./RobloxPlayer.zip ] && rm ./RobloxPlayer.zip

        arch=$(uname -m)
        
        if [[ "$arch" == "arm64" ]]; then
            echo "[!] Apple Silicon CPU Detected"
            version=$(curl -s http://setup.roblox.com/mac/arm64/DeployHistory.txt | grep "New Client version" | tail -n 1 | sed -n 's/.*\(version-[^ ]*\).*/\1/p')
            curl -s "http://setup.rbxcdn.com/mac/arm64/{$version}-RobloxPlayer.zip" -o "./RobloxPlayer.zip"
        elif [[ "$arch" == "x86_64" ]]; then
            echo "[!] Intel CPU Detected"
            version=$(curl -s http://setup.roblox.com/mac/DeployHistory.txt | grep "New Client version" | tail -n 1 | sed -n 's/.*\(version-[^ ]*\).*/\1/p')
            curl -s "http://setup.rbxcdn.com/mac/{$version}-RobloxPlayer.zip" -o "./RobloxPlayer.zip"
        else
            echo "Unknown architecture: $arch. Aborting"
            exit 0
        fi
        
        echo "[+] Installing Latest Roblox..."

        unzip -qo "./RobloxPlayer.zip"
        mv ./RobloxPlayer.app /Applications/Roblox.app
        rm ./RobloxPlayer.zip
        echo "[+] Uninstalled Hydrogen-M."
        echo "[+] Script by @109dg"
        echo "[-] Removing Hydro Uninstaller"
        cd
        rm -rf hydro-uninstaller.sh

        exit 0
    else
        echo "Have a nice day!"
        rm -rf hydro-uninstaller.sh
        exit 0
    fi

    clear

}

main
