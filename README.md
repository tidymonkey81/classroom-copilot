# Classroom Copilot

An AI copilot for learners and educators.

## Table of Contents

- [Classroom Copilot](#classroom-copilot)
  - [Table of Contents](#table-of-contents)
  - [Project Overview](#project-overview)
  - [Tech Stack](#tech-stack)
  - [Installation](#installation)
    - [Prerequisites](#prerequisites)
      - [WhisperLive](#whisperlive)
  - [User Authentication and Role Management](#user-authentication-and-role-management)
    - [Setting up Firebase Authentication](#setting-up-firebase-authentication)
    - [Managing User Roles and Permissions](#managing-user-roles-and-permissions)
  - [Roadmap](#roadmap)
    - [Current Development Phase](#current-development-phase)
    - [Future Plans](#future-plans)
  - [Contributing](#contributing)
  - [License](#license)
  - [Contact](#contact)

## Project Overview

plan/teach/journal/learn

## Tech Stack

- **Frontend:** React, TypeScript, Vite, React Router, Emotion, MUI, ReactFlow, Tldraw
- **Backend:** FastAPI, Python, Neo4j, Pandas
- **Testing:** Vitest, Testing Library
- **DevOps:** Docker, Docker Compose

## Installation

### Prerequisites

- Node.js
- Docker
- WhisperLive
- Ollama

#### WhisperLive

- [WhisperLive GitHub repo](https://github.com/collabora/WhisperLive)
- [Installing the NVIDIA Container Toolkit](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html)

## User Authentication and Role Management

To set up user authentication and manage user roles and permissions, follow these guidelines:

### Setting up Firebase Authentication

1. Go to the [Firebase Console](https://console.firebase.google.com/).
2. Create a new project or select an existing one.
3. Navigate to the "Authentication" section and enable the sign-in methods you want to use (e.g., email/password, Google, Facebook).
4. Install the Firebase SDK in your project: `npm install firebase`.
5. Initialize Firebase in your application with your project's credentials. You can find the necessary configuration in your Firebase project settings.

### Managing User Roles and Permissions

1. Use the React Context API to manage user state across your application.
2. Create a context that holds the user's authentication state and role.
3. On user login, fetch the user's role from your database and store it in the context.
4. Use React Router to create protected routes that check the user's role before rendering the appropriate dashboard or redirecting to a login page.

## Dash Frontend Application

To set up and run the Dash frontend application for managing Neo4j database instances, follow these steps:

1. Ensure you have Python installed on your system.
2. Navigate to the `dash_frontend` directory within the project.
3. Install the required Python packages by running `pip install -r requirements.txt`.
4. Run the Dash app by executing `python app.py`.
5. The Dash app will start, and you can access it by navigating to `http://127.0.0.1:8050` in your web browser.

The Dash frontend application interacts with the FastAPI backend to perform database management tasks such as creating, updating, and deleting Neo4j database instances. This allows for a seamless integration between the frontend and backend, providing a user-friendly interface for database management.

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
  - Note: We are planning a transition towards a distributed graph database solution to enhance scalability and performance.
  - TODO:
    - [ ] Rewrite curriculum import code
    - [ ] Move remaining code from ipynb

- [ ] **Transition to Distributed Graph Database**
  - We are moving away from Neo4J to an open-source distributed graph database to improve scalability and fault tolerance.
  - This transition will allow us to handle larger datasets and provide a more robust infrastructure for our application.
  - TODO:
    - [ ] Evaluate and select a suitable distributed graph database
    - [ ] Design and implement the migration strategy
    - [ ] Test the new database with existing data and queries

- [ ] **Permanent Ledger for User-Generated Content**
  - Implementing a permanent ledger using IPFS and Filecoin for user-generated content to ensure data permanence and incentivize content creation.
  - This will allow users to access their data in a permanent ledger and incentivize both students and teachers to create content.
  - TODO:
    - [ ] Integrate IPFS for storing user-generated content
    - [ ] Implement Filecoin incentivization structure
    - [ ] Develop user interfaces for content creation and access

- [ ] **Dashboard**
  - Provides users with a view of personal data
  - TODO:
    - [ ] Decide dashboard template or app

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
  - TODO:
    - [ ] Implement OpenAI API requests
    - [ ] Implement local Ollama requests

- [ ] **File Storage**
  - Files are currently stored locally alongside the backend
  - File storage platforms may be implemented later
  - Types of files stored
    - School files
    - Curriculum files
    - Teaching files
    - Student work files
  - TODO:
    - [ ] Create directory structure for expected data

- [ ] **Advanced AI Features**
  - Background Agents and User Agents are employed to manage planning, scheduling, teaching and learning
  - TODO:
    - [ ] Decide agent framework

- [ ] **User Authentication**
  - Teachers and students can access the applicationa and are provided personalised user interfaces.
  - TODO:
    - [ ] Implement teacher users
    - [ ] Implement student users
    - [ ] Route users to personal pages

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

For any inquiries, please contact [kcar@kevlarai.com](mailto:kcar@kevlarai.com)
