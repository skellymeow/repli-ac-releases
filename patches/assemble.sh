#!/usr/bin/env bash
set -euo pipefail

rm -rf dist
mkdir -p dist/app/runtime
cp zig-out/bin/stitch.exe dist/app/StitchUI.exe
cp -R agent server config plugin dist/app/

"$NATIVE_SDK_ZIG" cc launcher/main.c \
  -target x86_64-windows-gnu \
  -O2 -DUNICODE -D_UNICODE -municode -mwindows \
  -lbcrypt -luser32 -lkernel32 -ladvapi32 \
  -o dist/app/Stitch.exe

test -f dist/app/Stitch.exe

curl --fail --location --retry 3 --output node-win.zip https://nodejs.org/download/release/v24.18.0/node-v24.18.0-win-x64.zip
echo '0ae68406b42d7725661da979b1403ec9926da205c6770827f33aac9d8f26e821  node-win.zip' | sha256sum --check
unzip -q node-win.zip
cp node-v24.18.0-win-x64/node.exe dist/app/runtime/node.exe

cat > dist/app/package.json <<'JSON'
{
  "name": "stitch-runtime",
  "version": "0.1.1",
  "private": true,
  "type": "module",
  "engines": { "node": ">=24" },
  "dependencies": {
    "@openrouter/ai-sdk-provider": "3.0.0",
    "ai": "7.0.37",
    "eve": "0.27.6",
    "mcp-proxy": "6.5.4",
    "zod": "4.4.3"
  }
}
JSON

(
  cd dist/app
  npm_config_os=win32 npm_config_cpu=x64 npm install --omit=dev --ignore-scripts --no-audit --no-fund
)

test -f dist/app/node_modules/eve/bin/eve.js
test -f dist/app/node_modules/mcp-proxy/package.json
