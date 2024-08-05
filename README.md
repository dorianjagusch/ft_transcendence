# ft_transcendence

Welcome to the "ft_transcendence" project! This project is part of the curriculum at Hive Helsinki (School 42) and aims to create a real-time web application - a multiplayer online game. The game is designed to showcase various skills, including web development, database management, and networking. This project was done in collaboration between
- [Meri Eskelinen](https://github.com/merituulie)
- [Josefina Husso](https://github.com/hussojo)
- [Dorian Jagusch](https://github.com/dorianjagusch)
- [Sakari Salmi](https://github.com/sakarisalmi)
- [Azär Sarikhani](https://github.com/azarSarikhani/)

## Demonstration

### Registration & Login


[Watch the video](https://raw.githubusercontent.com/dorianjagusch/repository/main/demo/login.mp4)



### Editing Profile

https://github.com/dorianjagusch/ft_transcendence/blob/main/demo/user-profile.mov

### Friends

https://github.com/dorianjagusch/ft_transcendence/blob/main/demo/friends.mov

### Pong

https://github.com/dorianjagusch/ft_transcendence/blob/main/demo/pong.mov

### Tournament

https://github.com/dorianjagusch/ft_transcendence/blob/main/demo/setup-tournament.mov

### Stats

https://github.com/dorianjagusch/ft_transcendence/blob/main/demo/stats.mov


## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Getting Started](#getting-started)
- [Usage](#usage)

## Getting Started

To get started with the "ft_transcendence" project, follow these steps:

1. Clone the repository:
    ```sh
    git clone https://github.com/dorianjagusch/ft_transcendence.git
    ```
2. Navigate to the project directory:
    ```sh
    cd ft_transcendence
    ```
3. Run the application using the Makefile:
    ```sh
    make
    ```

Ensure Docker is installed on your machine.
The site can be reached on `https://localhost:8443`

## Usage

Once the project is set up, you can:

- Start the application locally:
    ```sh
    make run
    ```
- Access the application in your web browser:
    ```sh
    http://localhost:3000
    ```
- Explore the game features, play matches, and interact with other players.

## Structure
The "ft_transcendence" project is structured into two main components: the server-side application written in Django and the client-side Single Page Application (SPA) written in vanilla JavaScript. Both components are containerized using Docker for easy deployment and management. The frontend is composed of a single container, while the backend, uses gunicorn, daphne, django and Postgres. Nginx is used for securing the connection with a reverse proxy and keep the backend separated from the outside world.

## Features
- User Management and Friends: Implemented using Django's built-in authentication system. Users can register, log in, and manage their profiles, by uploading avatars and editing their usernames. Friend relationships are managed through database relationships.
- Real-time Gameplay: Utilizes WebSockets for real-time communication between the server and clients. Django Channels is used to handle WebSocket connections.
- Optional 3D Graphics: Implemented using WebGL for rendering 3D graphics in the browser.
- Server-side Pong: The game logic is handled on the server-side to ensure fair play and synchronization between players.
- User Dashboards: Each user has a personalized dashboard that displays their stats, game history, and friends list. Implemented using Django views and templates.
- PostgreSQL Database: All user data, game data, and other persistent information are stored in a PostgreSQL database.
- Secure Connections: All communications between the client and server are secured using HTTPS. Django's security features are utilized to protect against common vulnerabilities.
- GDPR Compliance: User data is handled in accordance with GDPR guidelines. Users can request data deletion and access their data.

## Project Learnings
- Containerization: Docker was used to containerize both the backend and frontend, making the application easy to deploy and manage. This approach also ensures consistency across different environments.
- Real-time Communication: Implementing real-time features using WebSockets and Django Channels was a valuable learning experience. It highlighted the importance of efficient data handling and synchronization.
- 3D Graphics: Integrating WebGL for optional 3D graphics provided insights into advanced browser rendering techniques and performance optimization.
- Security: Ensuring secure connections and following best practices for data protection was crucial. This included using HTTPS, securing WebSocket connections, and adhering to GDPR guidelines.
- AI Development: Creating an AI opponent for single-player mode involved understanding game theory and implementing algorithms that provide a challenging yet fair experience.
- User Experience: Designing user-friendly interfaces and ensuring smooth navigation within the SPA was essential for user engagement. This included implementing client-side routing and dynamic content updates.

## Contributing

We welcome contributions to the "ft_transcendence" project. Please refer to the [Contributing Guide](docs/contributing.md) for guidelines on how to contribute.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
