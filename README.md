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
    - [Current Development Phase](#current-development-phase)
    - [Future Plans](#future-plans)
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

### Current Development Phase
- [ ] **Neo4J Graph Database**
  - Provides semantic search capabilities using CYPHER queries on rich connected data stored in a graph database.
  - Data stored in the Neo4J database:
    - School data (name, location, type, learning stages, staff, students, rooms etc)
    - User data
      - Teacher (name, timetable, teaching styles etc)
      - Student (name, timetable, learning styles etc)
    - Scheduling data (global calendar, school calendars, teacher calendars, student calendars etc)
    - Curriculum data (subjects, topics, lessons, learning statements etc)

- [ ] **File Storage**
  - Files are currently stored locally alongside the backend
  - File storage platforms may be implemented later
  - Types of files stored
    - School files
    - Curriculum files
    - Teaching files
    - Student work files

- [ ] **TlDraw**
  - Provides a canvas for structuring teaching and learning content
  - TODO:
    - [ ] Create a canvas for every lesson
    - [ ] Implement transcription and text generation tools (for example for creating keyword definitions for lessons)

- [ ] **React-Flow**
  - Provides a GUI for planning and scheduling teaching and learning
    - TODO:
      - [ ] Get data from Neo4J databases to populate nodes and edges
      - [ ] Reflect Neo4J database data graph structure in layout of nodes and edges
      - [ ] Edit data within nodes (for example change lesson titles)
      - [ ] Allow changes to nodes and relationships to be updated in the Neo4J backend
      - [ ] Stylise nodes and edges
  
- [ ] **CopilotKit**
  - Provides an interactive chatbot

- [ ] **User Authentication**
  - Implement user registration and login.
  - Secure user data with encryption. production
  
- [ ] **Advanced AI Features**
  - Enhance transcription accuracy.
  - Develop AI-driven study recommendations based on user behavior.

### Future Plans
- [ ] **Real-Time Collaboration**
  - Develop features for real-time document editing.

- [ ] **Mobile Application**
  - Develop a mobile version of the application for iOS and Android.

- [ ] **Integration with LMS**
  - Integrate with popular Learning Management Systems (LMS) like Moodle and Canvas.

- [ ] **Gamification**
  - Implement gamification features to increase user engagement.

## Contributing
1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Commit your changes (`git commit -m 'Add new feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Open a Pull Request.

## License
This project is licensed under a KevlarAI license.

## Contact
For any inquiries, please contact [kcar@kevlarai.com](mailto:kcar@kevlarai.com).
