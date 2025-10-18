# ♠️♥️ Poker Hand Analyzer ♦️♣️

The **Poker Hand Analyzer** is a Python desktop application built with **Tkinter** that provides a strategic edge in Texas Hold'em. It calculates your estimated hand equity (win probability) against multiple opponents using a Monte Carlo simulation and offers a recommended action (Fold, Call, or Raise) based on pot odds and perceived opponent aggressiveness.



## ✨ Features

* **Interactive GUI:** A visually appealing and intuitive interface for card selection and game parameter input.
* **Card Selection:** Clickable deck to select your two-card hand and up to five community cards (Flop, Turn, River).
* **Monte Carlo Simulation:** Estimates your **Win Probability** by simulating thousands of outcomes with randomly dealt opponent hands and remaining community cards.
* **Action Recommendation:** Suggests the optimal move (**Fold**, **Call**, or **Raise**) by comparing your calculated win probability against the implied pot odds, with adjustments for opponent tendencies.
* **Customizable Parameters:** Input for **Number of Opponents**, **Pot Size**, **Opponent's Bet**, and a slider for **Opponent Aggressiveness**.

---

## ⚙️ Setup and Installation

### Prerequisites

You need **Python 3.x** and **Git** installed on your system.

### Installation Steps

1.  **Clone the Repository:**
    Open your terminal or command prompt and clone the project.
    *(Replace `YOUR_REPOSITORY_URL` with the actual URL.)*

    ```bash
    git clone YOUR_REPOSITORY_URL
    cd Poker-Hand-Analyzer
    ```

2.  **Install Dependencies (Optional but Recommended):**
    The application uses standard Python libraries, with **Pillow (PIL)** being an optional dependency for displaying the background image.

    ```bash
    pip install Pillow
    ```

3.  **Run the Application:**
    Execute the main file from the project directory:

    ```bash
    python main.py
    ```

---

## 🖥️ How to Use

1.  **Select Cards:** Click on two cards from the grid for your **Hand**, and then select 3, 4, or 5 cards for the **Community Cards**.
2.  **Enter Game Data:**
    * Set the **Number of Opponents** (1-8).
    * Input the **Pot Size** and the **Opponent's Bet**.
    * Adjust the **Opponent Aggressiveness** slider (0=Passive, 10=Very Aggressive).
3.  **Analyze:** Click the **"Analyze Hand"** button.
4.  **View Results:** The application will display the calculated **Win Probability** (Equity) and a **Recommended Action** based on the built-in poker logic.

---

## 🔎 Technical Deep Dive

### `poker_logic.py`

This file contains the core algorithms of the analyzer:

* **Hand Ranking (`get_hand_rank`):** This function determines the strength of the best 5-card hand possible from the 7 total cards (2 hole cards + 5 board cards). It returns a tuple-based rank for accurate comparison (e.g., `(7, quad_rank, kicker)` for Quads).
* **Monte Carlo Simulation (`calculate_win_probability`):** This is the heart of the equity calculation. It performs **50,000 simulations** by randomly dealing all remaining unknown cards (opponents' hole cards and future board cards) to determine how often your hand wins or ties.
* **Decision Logic (`make_decision`):** This function translates the raw win probability into an action using pot odds, which are calculated as:

    $$\text{Pot Odds} = \frac{\text{Opponent's Bet}}{\text{Pot Size} + \text{Opponent's Bet}}$$

    The recommendation is made by comparing $\text{Win Probability}$ against $\text{Pot Odds}$, and adjusting the required probability thresholds based on the **Opponent Aggressiveness** slider.

### Hand Rank Hierarchy

The rank IDs used in `get_hand_rank` are (higher is better):

| Rank ID | Hand Type | Example Rank Tuple |
| :--- | :--- | :--- |
| **9** | Royal Flush | `(9, 12)` |
| **8** | Straight Flush | `(8, high_card_rank)` |
| **7** | Four of a Kind | `(7, quad_rank, kicker_rank)` |
| **6** | Full House | `(6, trips_rank, pair_rank)` |
| **5** | Flush | `(5, high_card_1, \dots)` |
| **4** | Straight | `(4, high_card_rank)` |
| **3** | Three of a Kind | `(3, trips_rank, k1, k2)` |
| **2** | Two Pair | `(2, high_pair, low_pair, kicker)` |
| **1** | One Pair | `(1, pair_rank, k1, k2, k3)` |
| **0** | High Card | `(0, k1, k2, k3, k4, k5)` |

⚠️ **A Note on Responsible Gaming:** While this tool uses logic and math to improve decision-making, poker remains a game of chance. Please only play with money you can afford to lose and seek help if gambling becomes a problem. Play smart, play responsibly.
