import tkinter as tk
from tkinter import ttk, messagebox
import poker_logic as pl
from urllib.request import urlopen
try:
    from PIL import Image, ImageTk
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False
import io

class PokerAnalyzerGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Poker Hand Analyzer")
        self.master.geometry("1100x850")
        
        if PIL_AVAILABLE:
            try:
                image_url = "https://images.unsplash.com/photo-1549419137-97d519d5543c?q=80&w=2940&auto=format&fit=crop"
                with urlopen(image_url) as u:
                    raw_data = u.read()
                im = Image.open(io.BytesIO(raw_data))
                self.background_image = ImageTk.PhotoImage(im)
                self.background_label = tk.Label(master, image=self.background_image)
                self.background_label.place(x=0, y=0, relwidth=1, relheight=1)
            except Exception as e:
                self.master.config(bg="#006400")
                print(f"Warning: Failed to load background image. Using solid color. Error: {e}")
        else:
            self.master.config(bg="#006400")
            print("Warning: Pillow not installed. Please install it with 'pip install Pillow' to use background images.")

        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        self.style.configure('TButton', font=('Inter', 12, 'bold'), relief='raised', padding=10, background='#333333', foreground='white')
        self.style.map('TButton', background=[('active', '#555555')])
        
        self.style.configure('Card.TButton', font=('Inter', 10, 'bold'), relief='raised', borderwidth=2, padding=(5, 20), background='white')
        self.style.map('Card.TButton', background=[('disabled', '#555555')], foreground=[('disabled', '#A0A0A0')])

        self.style.configure('TFrame', background='#006400')
        self.style.configure('TLabel', background='#006400', foreground='gold', font=('Inter', 12, 'bold', 'italic'))
        self.style.configure('TEntry', font=('Inter', 12), foreground='white', fieldbackground='#333333')
        self.style.configure('TScale', background='#006400', troughcolor='#3C3C3C')
        self.style.configure('TSpinbox', font=('Inter', 12), foreground='white', background='#333333')
        
        self.SUIT_SYMBOLS = {'c': '♣', 'd': '♦', 'h': '♥', 's': '♠'}
        self.selected_hand = []
        self.selected_board = []
        self.all_card_buttons = {}

        self.create_widgets()

    def create_widgets(self):
        self.main_frame = ttk.Frame(self.master, padding="20")
        self.main_frame.pack(fill='both', expand=True)
        
        title_label = ttk.Label(self.main_frame, text="Select your hand and community cards from the deck.", font=('Inter', 16, 'bold', 'italic'), foreground='gold', background='#006400')
        title_label.pack(pady=(0, 20))
        
        selected_cards_frame = ttk.Frame(self.main_frame)
        selected_cards_frame.pack(pady=10)
        self.hand_label = ttk.Label(selected_cards_frame, text="Your Hand: ", font=('Inter', 14, 'bold', 'italic'))
        self.hand_label.pack(side='left', padx=10)
        self.board_label = ttk.Label(selected_cards_frame, text="Community Cards: ", font=('Inter', 14, 'bold', 'italic'))
        self.board_label.pack(side='left', padx=10)

        card_selection_frame = ttk.Frame(self.main_frame, relief='groove', padding=10, style='TFrame', borderwidth=2)
        card_selection_frame.pack(pady=10, padx=10)
        
        for i, suit in enumerate(pl.SUITS):
            suit_frame = ttk.Frame(card_selection_frame, style='TFrame')
            suit_frame.grid(row=i, column=0, columnspan=13, pady=5)
            
            for j, rank in enumerate(pl.RANKS):
                card = f"{rank}{suit}"
                text = f"{rank.upper()}{self.SUIT_SYMBOLS[suit]}"
                
                suit_color = 'red' if suit in ['h', 'd'] else 'black'
                self.style.configure(f'Card.{suit}.TButton', background='white', foreground=suit_color)
                
                button = ttk.Button(suit_frame,text=text,width=4,style=f'Card.{suit}.TButton',command=lambda c=card: self.select_card(c))
                button.pack(side='left', padx=2, pady=2)
                self.all_card_buttons[card] = button

        stats_frame = ttk.Frame(self.main_frame)
        stats_frame.pack(fill='x', pady=10)
        ttk.Label(stats_frame, text="Number of Opponents:", font=('Inter', 12, 'bold', 'italic')).pack(side='left', padx=(0, 5))
        self.num_opponents_spinbox = ttk.Spinbox(stats_frame, from_=1, to=8, width=3, justify='center')
        self.num_opponents_spinbox.pack(side='left', padx=5)
        self.num_opponents_spinbox.set(1)

        pot_frame = ttk.Frame(self.main_frame)
        pot_frame.pack(fill='x', pady=10)
        ttk.Label(pot_frame, text="Pot Size ($):", font=('Inter', 12, 'bold', 'italic')).pack(side='left', padx=(0, 5))
        self.pot_size_entry = ttk.Entry(pot_frame, width=8)
        self.pot_size_entry.pack(side='left', padx=5)
        self.pot_size_entry.insert(0, "0")

        bet_frame = ttk.Frame(self.main_frame)
        bet_frame.pack(fill='x', pady=10)
        ttk.Label(bet_frame, text="Opponent's Bet ($):", font=('Inter', 12, 'bold', 'italic')).pack(side='left', padx=(0, 5))
        self.opponent_bet_entry = ttk.Entry(bet_frame, width=8)
        self.opponent_bet_entry.pack(side='left', padx=5)
        self.opponent_bet_entry.insert(0, "0")

        aggro_frame = ttk.Frame(self.main_frame)
        aggro_frame.pack(fill='x', pady=10)
        ttk.Label(aggro_frame, text="Opponent Aggressiveness:", font=('Inter', 12, 'bold', 'italic')).pack(side='left')
        self.aggro_slider = ttk.Scale(aggro_frame, from_=0, to=10, orient='horizontal', length=150)
        self.aggro_slider.pack(side='left', padx=(10, 5))
        self.aggro_slider.set(5)

        button_frame = ttk.Frame(self.main_frame)
        button_frame.pack(pady=20)
        self.calculate_button = ttk.Button(button_frame, text="Analyze Hand", command=self.run_analysis)
        self.calculate_button.pack(side='left', padx=10)
        self.clear_button = ttk.Button(button_frame, text="Clear", command=self.clear_cards)
        self.clear_button.pack(side='left', padx=10)

        self.result_frame = ttk.Frame(self.main_frame, relief='groove', padding="10")
        self.result_frame.pack(fill='x')
        self.prob_label = ttk.Label(self.result_frame, text="Win Probability: -", font=('Inter', 12, 'bold', 'italic'))
        self.prob_label.pack(pady=5)
        self.action_label = ttk.Label(self.result_frame, text="Recommended Action: -", font=('Inter', 12, 'bold', 'italic'))
        self.action_label.pack(pady=5)
            
    def select_card(self, card):
        if len(self.selected_hand) + len(self.selected_board) >= 7:
            messagebox.showinfo("Selection Limit Reached", "You can only select a maximum of 7 cards.")
            return

        if len(self.selected_hand) < 2:
            self.selected_hand.append(card)
            self.hand_label.config(text=f"Your Hand: {', '.join([c[0].upper() + self.SUIT_SYMBOLS[c[1]] for c in self.selected_hand])}")
        elif len(self.selected_board) < 5:
            self.selected_board.append(card)
            self.board_label.config(text=f"Community Cards: {', '.join([c[0].upper() + self.SUIT_SYMBOLS[c[1]] for c in self.selected_board])}")
        
        self.all_card_buttons[card].config(state='disabled')
        
    def clear_cards(self):
        self.selected_hand = []
        self.selected_board = []
        self.hand_label.config(text="Your Hand: ")
        self.board_label.config(text="Community Cards: ")
        for button in self.all_card_buttons.values():
            button.config(state='normal')
        self.prob_label.config(text="Win Probability: -")
        self.action_label.config(text="Recommended Action: -")
        
    def run_analysis(self):
        if len(self.selected_hand) != 2:
            messagebox.showerror("Invalid Selection", "Please select exactly 2 cards for your hand.")
            return

        try:
            num_opponents = int(self.num_opponents_spinbox.get())
            pot_size = float(self.pot_size_entry.get())
            opponent_bet = float(self.opponent_bet_entry.get())
            opponent_aggro = self.aggro_slider.get() / 10.0

            win_prob = pl.calculate_win_probability(self.selected_hand, self.selected_board, num_opponents)
            recommended_action = pl.make_decision(win_prob, pot_size, opponent_bet, opponent_aggro)

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
