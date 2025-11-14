<a id="udemate"></a>
[![BuyMeACoffee][buymeacoffee-shield]][buymeacoffee-url]
[![LinkedIn][linkedin-shield]][linkedin-url]
[![Peerlist][peerlist-shield]][peerlist-url]

<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/muhammadazzazy/udemate">
    <img src="./assets/images/udemate-logo.png" alt="Udemate Logo" width="250" height="250" >
  </a>
</div>

  <h3 align="center">Udemate</h3>

  <p align="center">
    Effortless Udemy course enrollment automation
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

<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->

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
- <a href="https://github.com/ultrafunkamsterdam/undetected-chromedriver">
    <img src="https://avatars.githubusercontent.com/u/21027969?v=4" width="50" alt="undetected-chromedriver">
  </a>

<!-- GETTING STARTED -->

## Getting Started

### Prerequisites

#### Option 1: Run from Source (Recommended for Full Automation)

- [Python 3.13+](https://www.python.org/downloads)

- [Brave Browser](https://brave.com/) OR [Google Chrome](https://www.google.com/chrome/)

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

Udemate was tested on Windows 11 and Ubuntu 24.04 LTS.

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
   # Required.
   REDDIT_CLIENT_ID=""
   # Required.
   REDDIT_CLIENT_SECRET=""
   # Optional. Default is 'script:Udemate:v1.0 (by u/kemitche)'.
   REDDIT_USER_AGENT=""
   # Required if 2FA is not enabled.
   REDDIT_PASSWORD=""
   # Required if 2FA is not enabled.
   REDDIT_USERNAME=""
   # Optional. Default is 500.
   REDDIT_LIMIT=1000

   # Browser config
   # Required if you want to enroll in courses with a user profile.
   USER_DATA_DIR="C:\\Users\\username\\AppData\\Local\\BraveSoftware\\Brave-Browser\\User Data\\Udemate"

   # Gotify config
   GOTIFY_BASE_URL=""
   GOTIFY_APP_TOKEN=""

   # CourseCouponz config
   COURSECOUPONZ_RETRIES=3
   COURSECOUPONZ_TIMEOUT=30

   # Easy Learn config
   EASY_LEARN_RETRIES=3
   EASY_LEARN_TIMEOUT=30

   # Freewebcart config
   FREEWEBCART_RETRIES=3
   FREEWEBCART_TIMEOUT=30

   # iDC config
   IDC_RETRIES=3
   IDC_TIMEOUT=30

   # InventHigh config
   INVENTHIGH_RETRIES=3
   INVENTHIGH_TIMEOUT=30

   # Line51 config
   LINE51_RETRIES=3
   LINE51_TIMEOUT=30

   # WebHelperApp config
   WEBHELPERAPP_RETRIES=3
   WEBHELPERAPP_TIMEOUT=30

   # Udemy bot enrollment config
   UDEMY_RETRIES=3
   UDEMY_TIMEOUT=10
   ```

#### Option 1: Run from Source

4. Create a virtual environment

   ```sh
   # Windows
   python -m venv .venv

   # Linux
   python3.12 -m venv .venv
   ```

5. Activate the virtual environment

   ```sh
   # Windows
   .\.venv\Scripts\activate

   # Linux
   source .venv/bin/activate
   ```

6. Install dependencies

   ```sh
     pip install -r requirements.txt
   ```

7. Run the automation tool in headless mode to scrape intermediate links

   ```sh
    # Windows
    python .\src\main.py --mode headless

    # Linux
    python3 src/main.py --mode headless
   ```

8. Run the tool in GUI mode to automate course enrollment

   ```sh
   # Windows
   python .\src\main.py --mode gui

   # Linux
   python3 src/main.py --mode gui
   ```

> Note the following:
>
> 1. Command-line arguments override environment variables
> 2. All command-line arguments are optional
> 3. Default `mode` is `hybrid`

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
- [x] Add functionality to generate JSON files containing middleman links grouped by hostname
- [x] Scrape intermediate links from the following middlemen:

  - [x] CourseCouponz
  - [x] Course Treat
  - [x] Easy Learning
  - [x] Freewebcart
  - [x] iDC
  - [x] Invent High
  - [x] Line51
  - [x] WebHelperApp

- [x] Automate enrollment into Udemy courses
- [x] Implement caching mechanism for middleman and Udemy links
- [x] Transform codebase from standalone functions to class-based structure
- [x] Split driver into headless (for scraping) and non-headless (for enrollment)
- [x] Add logging across modules
- [x] Support Reddit accounts without 2FA enabled
- [x] Add argument parsing for different modes (headless, non-headless, hybrid)
- [x] Provide a docker image for headless mode to facilitate deployment
- [x] Improve performance of Udemy bot by skipping owned and paid courses
- [x] Migrate from Selenium webdriver to undetected-chromedriver to reduce detection by Cloudflare anti-bot checks
- [x] Standardize & dedupe middleman links pre-crawl
- [x] Remove affiliate marketing parts from Udemy links before caching the URLs and automatic enrollment
- [x] Improve performance via per-domain concurrent spidering
- [x] Add command-line arguments for specifying
  - [x] mode (hybrid, headless, or gui)
  - [x] timeout for each spider and enrollment bot (in seconds)
  - [x] retries for each spider and enrollment bot
- [x] Fix issue where the enrollment bot failed to detect the first button by considering both values of `data-purpose`: 'buy-this-course-button' and 'buy-now-button'
- [x] Support Google Chrome for converting middleman links to Udemy links and automating course enrollment
- [x] Fix issue where Brave Browser runs out of VRAM in non-headless mode
- [x] Clean LinkSynergy links generated by iDownloadCoupon spider
- [x] Add push notifications using Gotify for informing the user about events occurring during each run
- [ ] Delete the user data directory before GUI mode starts and wait for the user to login to Udemy
- [ ] Automatically detect the browser major version

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

[buymeacoffee-shield]: https://img.shields.io/badge/Buy%20Me%20a%20Coffee-yellow?style=for-the-badge&logo=buy-me-a-coffee
[buymeacoffee-url]: https://www.buymeacoffee.com/muhammadazzazy
[linkedin-shield]: https://img.shields.io/badge/LinkedIn-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white
[linkedin-url]: https://linkedin.com/in/muhammad-azzazy
[peerlist-shield]: https://img.shields.io/badge/Peerlist-00AA6C?style=for-the-badge&logo=peerlist&logoColor=white
[peerlist-url]: https://peerlist.io/muhammadazzazy
[Python]: https://img.shields.io/badge/python-000000?style=for-the-badge&logo=python
[Python-url]: https://python.org
[PRAW]: https://avatars.githubusercontent.com/u/1696888?s=50&v=4
[PRAW-url]: https://github.com/praw-dev/praw
