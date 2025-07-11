# Udemate

<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/muhammadazzazy/udemate">
    <img src="./assets/images/udemate-logo.png" alt="Udemate Logo" width="250" height="250" >
  </a>
</div>

  <h3 align="center">Udemate</h3>

  <p align="center">
    A tool for automating enrollment into free Udemy courses.
    <br />
    <a href="https://github.com/muhammadazzazy/udemate"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/muhammadazzazy/udemate">View Demo</a>
    &middot;
    <a href="https://github.com/muhammadazzazy/udemate/issues/new?labels=bug&template=bug-report---.md">Report Bug</a>
    &middot;
    <a href="https://github.com/muhammadazzazy/udemate/issues/new?labels=enhancement&template=feature-request---.md">Request Feature</a>
  </p>
</div>

<!-- PROJECT LOGO -->

> **Disclaimer:** This software is not affiliated with, endorsed by, or sponsored by Udemy, Inc. "Udemy" is a registered trademark of Udemy, Inc. All other trademarks are the property of their respective owners.

<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->

[![Buy Me A Coffee](https://img.shields.io/badge/Buy%20Me%20a%20Coffee-yellow?style=for-the-badge&logo=buy-me-a-coffee)](https://www.buymeacoffee.com/muhammadazzazy) [![LinkedIn][linkedin-shield]][linkedin-url]

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <ul>
          <li><a href="#option-1-run-from-source-recommended-for-full-automation">Option 1: Run from Source (Recommended for Full Automation)</a></li>
          <ul>
            <li><a href="#download-and-install-chromedriver-version-1380720449">Download and Install ChromeDriver (Version 138.0.7204.49)</a></li>
            <li><a href="#brave--chromedriver-version-match">Brave + ChromeDriver Version Match</a></li>
          </ul>
          <li><a href="#option-2-run-in-docker-headless-mode-only">Option 2: Run in Docker (Headless Mode Only)</a></li>
          <li><a href="#reddit-bot-setup">Reddit Bot Setup</a></li>
        </ul>
        <li><a href="#installation">Installation</a></li>
        <ul>
          <li><a href="#option-1-run-from-source">Option 1: Run from Source</a></li>
          <li><a href="#option-2-run-in-docker">Option 2: Run in Docker</li></a>
        </ul>
      </ul>
    </li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>

<!-- ABOUT THE PROJECT -->

## About The Project

An automation tool that reads Reddit posts from [r/udemyfreebies](https://www.reddit.com/r/udemyfreeebies/), extracts course links from middleman websites, converts them into direct Udemy links with coupons, and automates the enrollment process into free courses.

### Built With

- [![Python][Python]][Python-url]
- [![PRAW][PRAW]][PRAW-url]
- <a href="https://github.com/SeleniumHQ/selenium">
    <img src="https://raw.githubusercontent.com/SeleniumHQ/selenium/trunk/common/images/selenium_logo_mark_green.svg" width="50" alt="Selenium">
  </a>
  <!-- GETTING STARTED -->

## Getting Started

### Prerequisites

#### Option 1: Run from Source (Recommended for Full Automation)

- [Python 3.12+](https://www.python.org/downloads)

- [ChromeDriver (Version 138.0.7204.49)](https://storage.googleapis.com/chrome-for-testing-public/137.0.7151.119/linux64/chromedriver-linux64.zip).

  📌 Follow this [guide](#download-and-install-chromedriver-version-1380720449) to download and install the appropriate version.

- [Brave Browser](https://brave.com/linux/)

##### Download and Install ChromeDriver (Version 138.0.7204.49)

```sh
wget https://storage.googleapis.com/chrome-for-testing-public/138.0.7204.49/linux64/chromedriver-linux64.zip && unzip chromedriver-linux64.zip && cd chromedriver-linux64
sudo mv chromedriver /usr/local/bin
```

##### Brave + ChromeDriver Version Match

⚠️ The Brave Browser and ChromeDriver major versions **must match** for automation to work correctly.

Check your installed versions

```sh
brave-browser --version
chromedriver --version
```

#### Option 2: Run in Docker (Headless Mode Only)

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Buildx](https://github.com/docker/buildx)

> Use this option only if you intend to run in headless mode. Non-headless and hybrid modes require prerequisites mentioned in [Option 1](#option-1-run-from-source-recommended-for-full-automation).

#### Reddit Bot Setup

Create a Reddit bot and get environment variables

1. Visit [Third-party app authorizations](https://www.reddit.com/prefs/apps/)
2. Click on **create another app** button at the bottom
3. Set **name** to `Udemate`
4. Select **script**
5. Set **description** to an appropriate description (e.g. repo description)
6. Set **redirect uri** to `http://localhost:8080`

📝 Note: It is preferable to use a Reddit account that doesn't have 2FA configured. If you have 2FA enabled for your Reddit account, the script will provide you with a link that you need to click on to generate a Reddit refresh token and authorize access.

### Tested Environment

Udemate was tested on Ubuntu 24.04 LTS.

### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/muhammadazzazy/udemate.git
   ```
2. Navigate into the project directory
   ```sh
   cd udemate
   ```
3. Create a .env file

   ```env
    # Reddit config
    # Required if 2FA is enabled.
    REDDIT_CLIENT_ID=""
    # Required if 2FA is enabled.
    REDDIT_CLIENT_SECRET=""
    # Optional. Default is 'script:Udemate:v1.0 (by u/kemitche)'.
    REDDIT_USER_AGENT=""
    # Required if 2FA is not enabled.
    REDDIT_PASSWORD=""
    # Required if 2FA is not enabled.
    REDDIT_USERNAME=""
    # Optional. Default is 500.
    LIMIT=1000

    # Browser config
    # Optional.
    BROWSER_USER_AGENT="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36"
    # Optional. Default is 9222.
    PORT=9222
    # Replace <username> with your Linux username.
    USER_DATA_DIR="/home/<username>/.config/BraveSoftware/Brave-Browser"
    # Optional. Default is 'Default'.
    PROFILE_DIR="Default"
   ```

#### Option 1: Run from Source

4. Create a virtual environment

   ```sh
     python3 -m venv .venv
   ```

5. Install dependencies

   ```sh
     pip install -r requirements.txt
   ```

6. Run `launch_brave.sh` script to start Brave Browser with debugging and default user profile

   ```sh
    ./src/web/launch_brave.sh
   ```

7. Run the script
   ```sh
    python3 src/main.py [--mode {headless|gui|hybrid}]
    # Default: --mode hybrid
   ```

#### Option 2: Run in Docker

4. Build the Docker image

   ```sh
    docker build --build-arg USER_ID=$(id -u) --build-arg GROUP_ID=$(id -g) -f docker/Dockerfile -t udemate .
   ```

5. Run the docker image

   ```sh
    docker run --rm --env-file .env -v "$(pwd):/udemate" udemate
   ```

<p align="right">(<a href="#udemate">back to top</a>)</p>

<!-- ROADMAP -->

## Roadmap

- [x] Implement environment variable parsing
- [x] Add requirements.txt
- [x] Implement refresh token authentication
- [x] Add functionality to generate JSON files of submissions grouped by hostname
- [x] Scrape intermediate links from the following middlemen:

  - [x] Easy Learning
  - [x] Freewebcart
  - [x] iDC
  - [x] Line51

- [x] Automate enrollment into Udemy courses
- [x] Implement caching mechanism for middleman and Udemy links
- [x] Transform codebase from standalone functions to class-based structure
- [x] Split driver into headless (for scraping) and non-headless (for enrollment)
- [x] Add logging across modules
- [x] Spoof User-Agent in browser when scraping intermediary websites
- [x] Support Reddit accounts without 2FA enabled
- [x] Add argument parsing for different modes (headless, non-headless, hybrid)
- [x] Provide a docker image for headless mode to facilitate deployment
- [x] Improve performance of Udemy bot by skipping owned and paid courses

See the [open issues](https://github.com/muhammadazzazy/udemate/issues) for a full list of proposed features (and known issues).

<p align="right">(<a href="#udemate">back to top</a>)</p>

<!-- CONTRIBUTING -->

## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#udemate">back to top</a>)</p>

<!-- LICENSE -->

## License

Distributed under the MIT License. See [LICENSE](LICENSE) for more information.

<p align="right">(<a href="#udemate">back to top</a>)</p>

> **Disclaimer:** This software is not affiliated with, endorsed by, or sponsored by Udemy, Inc. "Udemy" is a registered trademark of Udemy, Inc. All other trademarks are the property of their respective owners.

<!-- CONTACT -->

## Contact

Muhammad Azzazy - muhammadazzazy8@gmail.com

Project Link: [https://github.com/muhammadazzazy/udemate](https://github.com/muhammadazzazy/udemate)

<p align="right">(<a href="#udemate">back to top</a>)</p>

<!-- ACKNOWLEDGMENTS -->

## Acknowledgments

- [Choose an Open Source License](https://choosealicense.com)
- [GitHub Emoji Cheat Sheet](https://www.webpagefx.com/tools/emoji-cheat-sheet)
- [Img Shields](https://shields.io)
- [Python](https://www.python.org/)
- [Pylint (VS Code Extension)](https://marketplace.visualstudio.com/items?itemName=ms-python.pylint)
- [Pylance (VS Code Extension)](https://marketplace.visualstudio.com/items?itemName=ms-python.vscode-pylance)
- [autopep8 (VS Code Extension)](https://marketplace.visualstudio.com/items?itemName=ms-python.autopep8)

<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->

[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/muhammad-azzazy
[Python]: https://img.shields.io/badge/python-000000?style=for-the-badge&logo=python
[Python-url]: https://python.org
[PRAW]: https://avatars.githubusercontent.com/u/1696888?s=50&v=4
[PRAW-url]: https://github.com/praw-dev/praw
