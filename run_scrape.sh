#!/bin/bash

# Load NVM
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"  # This loads nvm
[ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"  # This loads nvm bash_completion

# Use specific Node version
nvm use 18.20.2

# Install dependencies
npm install

# Compile TypeScript
tsc

# Run the compiled JavaScript file
node ./dist/scrape_lambda.js

