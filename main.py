import tkinter as tk
from tkinter import ttk, messagebox
import poker_logic as pl

class PokerAnalyzerGUI:
    def __init__(self, master):
        self.master = master
        master.title("Poker Hand Analyzer")
        master.geometry("500x600")
        master.config(bg="#333333")
        
        self.style = ttk.Style()
        self.style.configure('TFrame', background='#333333')
        self.style.configure('TLabel', background='#333333', foreground='white', font=('Inter', 12))
        self.style.configure('TButton', font=('Inter', 12, 'bold'), background='#555555', foreground='white')
        self.style.map('TButton', background=[('active', '#777777')])
        self.style.configure('TEntry', font=('Inter', 12))
        self.style.configure('TScale', background='#333333', troughcolor='#555555')
        self.style.configure('TSpinbox', font=('Inter', 12))

        self.create_widgets()

    def create_widgets(self):
        main_frame = ttk.Frame(self.master, padding="20")
        main_frame.pack(fill='both', expand=True)

        # Instructions
        ttk.Label(main_frame, text="Enter your hand and the community cards.", font=('Inter', 14, 'bold')).pack(pady=(0, 10))
        ttk.Label(main_frame, text="Use 'T' for 10, 'J' for Jack, 'Q' for Queen, 'K' for King, 'A' for Ace.", justify='center').pack(pady=(0, 5))
        ttk.Label(main_frame, text="Example: 'Ah' for Ace of Hearts, 'Ks' for King of Spades.", justify='center').pack(pady=(0, 20))
        
        # Player Hand Input
        hand_frame = ttk.Frame(main_frame)
        hand_frame.pack(fill='x', pady=10)
        ttk.Label(hand_frame, text="Your Hand:").pack(side='left', padx=(0, 10))
        self.my_card_1_entry = ttk.Entry(hand_frame, width=5)
        self.my_card_1_entry.pack(side='left', padx=5)
        self.my_card_2_entry = ttk.Entry(hand_frame, width=5)
        self.my_card_2_entry.pack(side='left', padx=5)

        # Community Cards Input
        board_frame = ttk.Frame(main_frame)
        board_frame.pack(fill='x', pady=10)
        ttk.Label(board_frame, text="Board Cards (optional):").pack(side='left', padx=(0, 10))
        self.board_entries = [ttk.Entry(board_frame, width=5) for _ in range(5)]
        for entry in self.board_entries:
            entry.pack(side='left', padx=2)

        # Opponent/Game Stats Input
        stats_frame = ttk.Frame(main_frame)
        stats_frame.pack(fill='x', pady=10)
        ttk.Label(stats_frame, text="Number of Opponents:").pack(side='left', padx=(0, 5))
        self.num_opponents_spinbox = ttk.Spinbox(stats_frame, from_=1, to=8, width=3, justify='center')
        self.num_opponents_spinbox.pack(side='left', padx=5)
        self.num_opponents_spinbox.set(1)

        pot_frame = ttk.Frame(main_frame)
        pot_frame.pack(fill='x', pady=10)
        ttk.Label(pot_frame, text="Pot Size ($):").pack(side='left', padx=(0, 5))
        self.pot_size_entry = ttk.Entry(pot_frame, width=8)
        self.pot_size_entry.pack(side='left', padx=5)
        self.pot_size_entry.insert(0, "0")

        bet_frame = ttk.Frame(main_frame)
        bet_frame.pack(fill='x', pady=10)
        ttk.Label(bet_frame, text="Opponent's Bet ($):").pack(side='left', padx=(0, 5))
        self.opponent_bet_entry = ttk.Entry(bet_frame, width=8)
        self.opponent_bet_entry.pack(side='left', padx=5)
        self.opponent_bet_entry.insert(0, "0")

        # Opponent Model Slider
        aggro_frame = ttk.Frame(main_frame)
        aggro_frame.pack(fill='x', pady=10)
        ttk.Label(aggro_frame, text="Opponent Aggressiveness:").pack(side='left')
        self.aggro_slider = ttk.Scale(aggro_frame, from_=0, to=10, orient='horizontal', length=150)
        self.aggro_slider.pack(side='left', padx=(10, 5))
        self.aggro_slider.set(5)

        # Calculate Button
        self.calculate_button = ttk.Button(main_frame, text="Analyze Hand", command=self.run_analysis)
        self.calculate_button.pack(pady=20)

        # Results Display
        self.result_frame = ttk.Frame(main_frame, relief='groove', padding="10")
        self.result_frame.pack(fill='x')
        self.prob_label = ttk.Label(self.result_frame, text="Win Probability: -", font=('Inter', 12, 'bold'))
        self.prob_label.pack(pady=5)
        self.action_label = ttk.Label(self.result_frame, text="Recommended Action: -", font=('Inter', 12, 'bold'))
        self.action_label.pack(pady=5)

    def run_analysis(self):
        try:
            # Get user inputs
            my_cards = [self.my_card_1_entry.get().capitalize(), self.my_card_2_entry.get().capitalize()]
            board_cards = [entry.get().capitalize() for entry in self.board_entries if entry.get()]
            num_opponents = int(self.num_opponents_spinbox.get())
            pot_size = float(self.pot_size_entry.get())
            opponent_bet = float(self.opponent_bet_entry.get())
            opponent_aggro = self.aggro_slider.get() / 10.0

            # Validate inputs
            valid_cards = [f'{r}{s}' for s in pl.SUITS for r in pl.RANKS]
            all_input_cards = my_cards + board_cards
            if not all(c in valid_cards for c in all_input_cards):
                messagebox.showerror("Invalid Input", "Please enter valid card formats (e.g., 'As', 'Kh', 'T' for 10).")
                return

            # Run the core logic
            win_prob = pl.calculate_win_probability(my_cards, board_cards, num_opponents)
            recommended_action = pl.make_decision(win_prob, pot_size, opponent_bet, opponent_aggro)

            # Display results
            self.prob_label.config(text=f"Win Probability: {win_prob:.2%}")
            self.action_label.config(text=f"Recommended Action: {recommended_action}")

        except ValueError:
            messagebox.showerror("Invalid Input", "Please ensure numerical fields contain valid numbers.")
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = PokerAnalyzerGUI(root)
    root.mainloop()
