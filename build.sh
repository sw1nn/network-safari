#!/bin/bash



docker build -t simple-server .

if command -v livereload; then
    livereload -p 8000 -t presentation.html -t presentation.css
else
    echo "arrange for livereload to be installed"
    echo "The included PipEnv will install it."
fi
