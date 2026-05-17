## Contributors

| UWA ID   | Name            | GitHub User |
| -------- | --------------- | ----------- |
| 24228963 | Taleena Watts   | taleenaw    |
| 24227537 | Ryan Ramaprasad | 24227537    |
| 24270886 | Aron Zombori    | ChegGH      |
| 24218174 | Bansi Patel     | bansi7306   |

## Application Purpose

Xenotype is a sci-fi themed typing game designed to improve typing speed and accuracy through interactive gameplay. The application combines traditional typing tests with alien-themed missions, branching storylines, and competitive score tracking to create a more engaging typing experience.

The game allows users to:

- Complete practice scenarios across Easy, Medium, and Hard difficulties
- Play multi-stage campaign missions with branching choices
- Track typing performance through WPM, accuracy, grades, and error counts
- View personal progress statistics and WPM improvement over time through profile graphs
- Earn personalised profile borders based on player rank and performance
- Compare scores on a global leaderboard
- Create accounts and save personal progress

The application was designed with a futuristic terminal-inspired interface to match the sci-fi atmosphere of the game. Real-time typing feedback, progress bars, timers, animated popups, mission outcomes, and profile progression systems are used to make typing practice feel more immersive and game-like rather than a standard typing test.

Xenotype is built as a Flask web application using Python, HTML, CSS, JavaScript, and SQLite. The backend manages users, scenarios, missions, profile statistics, and leaderboard data, while the frontend focuses on responsive gameplay and interactive UI elements.

## Features

### Scenarios

Players can access a large collection of practice typing scenarios categorised into Easy, Medium, and Hard difficulties. Each scenario contains unique sci-fi themed passages with different vocabulary complexity, punctuation difficulty, and time limits. The scenario system is designed to help users gradually improve their typing speed and accuracy while keeping gameplay varied and engaging. Both official and community-generated scenarios are supported, allowing the game to continuously expand with new content.

### Missions

The mission system provides a more immersive and story-driven gameplay experience. Missions are made up of multiple stages where players complete typing passages and then choose between branching decisions that affect the next stage of the mission. Each mission contains alien-themed narratives, humorous dialogue, and progressively more difficult typing challenges. This system transforms traditional typing practice into an interactive campaign experience with multiple possible outcomes.

### Leaderboard

The leaderboard system allows players to compare their performance with other users across the platform. Statistics such as Words Per Minute (WPM), typing accuracy, grades, and errors are recorded after each completed run. The leaderboard encourages competition and motivates players to improve their typing performance in order to achieve higher rankings.

### Real-Time Typing Feedback

During gameplay, players receive live performance feedback including WPM counters, accuracy percentages, timers, progress bars, and error tracking. Incorrectly typed characters are highlighted in real time, allowing players to instantly identify mistakes and improve typing precision. Dynamic progress indicators and visual effects help create a more interactive and engaging typing experience.

### Animated Results & Ranking System

At the end of scenarios and missions, players receive animated score popups displaying grades, themed visuals, and randomised result messages based on performance. Grades are calculated using both typing speed and accuracy, rewarding balanced performance rather than speed alone. This feature helps make typing practice feel more rewarding and game-like.

### Xeno Assistant

The Xeno Assistant is a Xenotype curated bot, sourced from our own flavour of local code to make your experience a bit easier. Is it the most advanced agent to speak to? No. But it's got heart, it uses some basic NLP to curate an undeniably delicious response with certain fallback phrases that it may revert to when a real thinker is put upon it. Don't worry there is no awkward pause, the assistant would never do that to you. A simple response from a young agent building itself through the conversation. Its learning. Kind of...

### Campaigns

Campaigns are generated text based games that rely on wpm to move on to the next move, this is done using a bot like structure to create a simple yet engaging gam play. If invalid commands are typed it will say so and you can track your progress with the status command. This has no bearing on your scores because this is more like a learning ground to bring up your WPM.

### Player Chat

The PlayerChat system allows users to communicate with one another within the application. This feature encourages community interaction, discussion, and engagement between players while using the platform.

### Profile System

Each user has a personalised profile page that stores gameplay history and performance statistics. Players can upload and use their own custom profile pictures, allowing them to personalise their accounts and identity within the game. The profile system also tracks player progress by displaying graphs that visualise how their WPM has improved over time throughout their typing journey. In addition, players can unlock personalised borders around their profile pictures based on rank and achievements, providing visual progression and rewarding continued improvement.

### Authentication System

The application includes a complete user authentication system where players can register, log in, and securely maintain personal accounts. User data such as mission progress, statistics, leaderboard rankings, and profile customisations are stored between sessions, allowing players to continue progressing over time.

## How to Launch the Application

### 1. Clone the Repository

```bash
git clone https://github.com/taleenaw/xenotype.git
cd xenotype
```

### 2. Create and Activate a Virtual Environment

#### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

#### Mac/Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Initialise the Database

```bash
python xenotype_DB.py
```

### 5. Run the Application

```bash
python run.py
```

### 6. Open the Application

Go to:

```text
http://127.0.0.1:5000
```

---

## Running Tests

To run the automated tests for the application, first make sure you are in the project folder and your virtual environment is activated.

### 1. Activate the Virtual Environment

#### Windows

```bash
venv\Scripts\activate
```

#### Mac/Linux

```bash
source venv/bin/activate
```

### 2. Install Required Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the Tests

```bash
python tests.py
```

This will execute the application’s automated test suite and display the results in the terminal.
