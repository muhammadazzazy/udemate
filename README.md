# Udemate

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
        <li><a href="#installation">Installation</a></li>
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

A collection of automation tools that read Reddit posts from [r/udemyfreebies](https://www.reddit.com/r/udemyfreeebies/), extract course links from middleman websites, convert them into direct Udemy links with coupons, and automate the enrollment process into free courses.

### Built With

- [![Python][Python]][Python-url]
- [![PRAW][PRAW]][PRAW-url]
- <a href="https://github.com/SeleniumHQ/selenium">
    <img src="https://raw.githubusercontent.com/SeleniumHQ/selenium/trunk/common/images/selenium_logo_mark_green.svg" width="50" alt="Selenium">
  </a>
  <!-- GETTING STARTED -->

## Getting Started

### Prerequisites

- [Python 3.12.7](https://www.python.org/downloads/release/python-3127/)

- [ChromeDriver Version: 137.0.7151.119 (r1453031)](https://storage.googleapis.com/chrome-for-testing-public/137.0.7151.119/linux64/chromedriver-linux64.zip).

  📌 Follow this [guide](#download-and-install-chromedriver-version-13707151119-r1453031) to download and install the appropriate version.

- [Brave Browser](https://brave.com/linux/)

#### Reddit Bot Setup

Create a Reddit bot and get environment variables

1. Visit [Third-party app authorizations](https://www.reddit.com/prefs/apps/)
2. Click on **create another app** button at the bottom
3. Set **name** to `Udemate`
4. Select **script**
5. Set **description** to an appropriate description (e.g. repo description)
6. Set **redirect uri** to `http://localhost:8080`

📝 Note: On the first run, the script will provide you with a link that you need to click on to generate a Reddit refresh token and authorize access.

#### Download and Install ChromeDriver (Version 137.0.7151.119)

```sh
wget https://storage.googleapis.com/chrome-for-testing-public/137.0.7151.119/linux64/chromedriver-linux64.zip && unzip chrome-linux64.zip && cd chromedriver-linux64
sudo mv chromedriver /usr/local/bin
```

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
    # Required
    CLIENT_ID=""
    CLIENT_SECRET=""
    BROWSER_USER_AGENT="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36"

    # Optional
    REDDIT_USER_AGENT=""
    LIMIT=1000
    PORT=9222
    USER_DATA_DIR="/home/<username>/.config/BraveSoftware/Brave-Browser" # Replace <username> with your Linux username
    PROFILE_DIR="Default"
   ```

4. Create a virtual environment

   ```sh
     python3 -m venv .venv
   ```

5. Install dependencies

   ```sh
     pip install -r requirements.txt
   ```

6. Run the script
   ```sh
     python3 src/main.py
   ```

<p align="right">(<a href="#udemate">back to top</a>)</p>

<!-- ROADMAP -->

## Roadmap

- [x] Implement environment variable parsing
- [x] Add requirements.txt
- [x] Implement refresh token authentication
- [x] Add functionality to generate JSON files of submissions grouped by hostname
- [ ] Scrape intermediate links from the following middlemen:

  - [x] Easy Learning
  - [x] Freewebcart
  - [x] IDC
  - [ ] Line51

- [x] Automate enrollment into Udemy courses
- [x] Implement caching mechanism
- [x] Transform codebase from standalone functions to class-based structure
- [x] Split driver into headless (for scraping) and non-headless (for enrollment)
- [x] Add logging across modules
- [x] Spoof User-Agent in browser when scraping intermediary websites

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
