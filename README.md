# pdp
For the Product Development Project course 2025-26. 

This consists of Python scripts that control a CNC machine running custom drivers, a Flask (Python) server that acts as the backend, and a web page as the UI (JS/TS, React - for now, Tailwind)

# How to use

After cloning, run
> git submodule init
>
> git submodule update

to fetch the two submodules, namely the frontend and backend.

Next navigate to user-interface, run

> deno install

Finally return to the root folder and run

> [sudo] docker compose up --build

to start the (development) server.

# Disclaimer

THIS IMPLEMENTATION HAS NOT BEEN TESTED NOR CHECKED FOR SECURITY VULNERABILITIES AND MAY CONTAIN BAD SECURITY PRACTICES! 

DO NOT USE IN PRODUCTION ENVIRONMENTS!