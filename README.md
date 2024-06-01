# Classroom Copilot

An AI copilot for learners and educators.

## Table of Contents

- [Classroom Copilot](#classroom-copilot)
  - [Table of Contents](#table-of-contents)
  - [Project Overview](#project-overview)
  - [Tech Stack](#tech-stack)
  - [Installation](#installation)
    - [Prerequisites](#prerequisites)
    - [Steps](#steps)
  - [Usage](#usage)
    - [Transcribe Audio](#transcribe-audio)
  - [Roadmap](#roadmap)
  - [Contributing](#contributing)
  - [License](#license)
  - [Contact](#contact)

## Project Overview
Classroom Copilot is an AI-driven application designed to assist both learners and educators by providing various tools and features to enhance the educational experience. The project leverages modern web technologies and AI to deliver a seamless and interactive user experience.

## Tech Stack
- **Frontend:** React, TypeScript, Vite, React Router, Emotion, MUI, ReactFlow, Tldraw
- **Backend:** FastAPI, Python, Neo4j, Pandas
- **Testing:** Vitest, Testing Library
- **DevOps:** Docker, Docker Compose

## Installation

### Prerequisites
- Node.js
- Docker

### Steps
1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/classroom-copilot.git
    cd classroom-copilot
    ```
2. Copy the environment variables:
    ```sh
    cp .env.example .env
    ```
3. Build and start the Docker containers:
    ```sh
    docker-compose up --build
    ```
4. Run tests:
    ```sh
    npm run test
    ```

## Usage
### Transcribe Audio
To transcribe an MP3 file, send a POST request to `/transcribe` with the file.
Example using `curl`:
```sh
curl -X POST "http://localhost:8000/transcribe" -H "accept: application/json" -H "Content-Type: multipart/form-data" -F "file=@path/to/your/audio.mp3"
```

## Roadmap
- [ ] Feature 1: Description
- [ ] Feature 2: Description
- [ ] Feature 3: Description

## Contributing
1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Commit your changes (`git commit -m 'Add new feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Open a Pull Request.

## License
This project is licensed under the MIT License.

## Contact
For any inquiries, please contact [kcar@kevlarai.com](mailto:kcar@kevlarai.com).