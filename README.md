# UdemyUnlocked

<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->

[![LinkedIn][linkedin-shield]][linkedin-url]

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

A Reddit bot that collects free Udemy coupons from Reddit posts on specific subreddits.

### Built With

- [![Python][Python]][Python-url]
- [![PRAW][PRAW]][PRAW-url]

<!-- GETTING STARTED -->

## Getting Started

### Prerequisites

[Python 3](https://python.org/downloads)

Create a Reddit bot and get environment variables:

1. Visit [Third-party app authorizations](https://www.reddit.com/prefs/apps/)
2. Click on **create another app** button at the bottom
3. Set **name** to `UdemyUnlocked`
4. Select **script**
5. Set **description** to an appropriate description (e.g. repo description)
6. Set **redirect uri** to `http://localhost:8080`

📝 Note: On the first run, the script will provide you with a link that you need to click on to generate a Reddit refresh token and authorize access.

### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/muhammadazzazy/udemy-unlocked.git
   ```
2. Navigate into the project directory
   ```sh
   cd udemy-unlocked
   ```
3. Create a .env file
   ```env
   CLIENT_ID=""
   CLIENT_SECRET=""
   USER_AGENT=""
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

<p align="right">(<a href="#udemyunlocked">back to top</a>)</p>

<!-- ROADMAP -->

## Roadmap

- [x] Implement environment variable parsing
- [x] Add requirements.txt
- [x] Implement refresh token authentication
- [ ] Add functionality to generate JSON files of submissions grouped by hostname

See the [open issues](https://github.com/muhammadazzazy/udemy-unlocked/issues) for a full list of proposed features (and known issues).

<p align="right">(<a href="#udemyunlocked">back to top</a>)</p>

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

<p align="right">(<a href="#udemyunlocked">back to top</a>)</p>

<!-- LICENSE -->

## License

Distributed under the MIT License. See [LICENSE](LICENSE) for more information.

<p align="right">(<a href="#udemyunlocked">back to top</a>)</p>

<!-- CONTACT -->

## Contact

Muhammad Azzazy - muhammadazzazy8@gmail.com

Project Link: [https://github.com/muhammadazzazy/udemy-unlocked](https://github.com/muhammadazzazy/udemy-unlocked)

<p align="right">(<a href="#udemyunlocked">back to top</a>)</p>

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
