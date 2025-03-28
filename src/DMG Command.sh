#!/bin/bash

create-dmg \
  --volname "AutoTyperZer0 1.0 Installer - macOS" \
  --volicon "AutoTyperZer0-mac/AT0Icon.icns" \
  --background "AutoTyperZer0-mac/DMG-BG.png" \
  --window-pos 260 120 \
  --window-size 750 535\
  --icon-size 120 \
  --icon "AutoTyperZer0.app" 200 190 \
  --hide-extension "AutoTyperZer0.app" \
  --app-drop-link 560 190 \
  "AutoTyperZer0.dmg" \
  "AutoTyperZer0/"
