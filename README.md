#  Go Game Implementation with Heuristic AI Engine

A fully functional, desktop-based implementation of the traditional board game **Go (19x19)** built in Python using **Pygame**. 

This project was engineered to simulate game theory mechanics, state space evaluation, and custom heuristic decision-making for single-player gameplay against an AI opponent.

---

##  Key Technical Features

* **Standard 19x19 Go Grid:** Implemented with official coordinate notation ($A-T$ excluding $I$, $1-19$ numbers) and precise click-collision math for line intersections.
* **Heuristic AI Engine:**
  * **Positional Weighting:** Evaluates board control based on distance from the center.
  * **Tactical Aggression:** Prioritizes moves that directly engage opponent stones.
  * **Dynamic Passing Threshold:** Calculates board saturation; if maximum positional value drops below a strategic threshold ($score < 5$), the AI dynamically yields its turn (Pass).
* **Game Rules Engine:**
  * **Liberties & Capture Logic:** Recursive depth-first tracking of group liberties to identify surrounding conditions and automatically clear captured stones.
  * **Legality Check:** Prevents illegal/suicidal moves unless the placement results in an immediate capture.
* **State Management & Passing System:**
  * Keyboard-triggered user pass system (`P` key).
  * Game end detection triggered by 2 consecutive passes, evaluating total board territory + captured stones.
* **Real-time Game Analytics & UI Panel:** Bottom dashboard rendering live stone counts, prisoner counts, and game status overlays.

---

## Tech Stack & Dependencies

* **Language:** Python 3.10+
* **GUI Engine:** Pygame
* **Graphics & Rendering:** Custom surface vector rendering with dynamic HUD/Overlay support.

---

## Getting Started

### Prerequisites
Make sure you have **Python 3.x** installed on your system.

### Installation

1. Clone the repository:
   ```bash
   git clone [https://github.com/I-Jojua/GO_project.git](https://github.com/I-Jojua/GO_project.git)
   cd GO_project