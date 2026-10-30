import os
import time
import tkinter as tk
from dotenv import load_dotenv
import pyperclip
from google import genai

# --- PASTE YOUR API KEY HERE ---
load_dotenv()

# Automatically fetches the key securely from the environment
client = genai.Client()

def show_ghost_popup(commentary):
  """Spawns a floating, semi-transparent Victorian ghost popup

  that stays until clicked and includes a scrollbar for longer text.
  """
  root = tk.Tk()
  root.overrideredirect(True)  # Remove window borders for a sleek look
  root.attributes("-topmost", True)  # Keep on top of other windows
  root.attributes("-alpha", 0.92)  # Slight transparency

  # Position it nicely in the bottom right corner of the screen (Made wider: 500px)
  screen_width = root.winfo_screenwidth()
  screen_height = root.winfo_screenheight()
  window_width = 500
  window_height = 140
  x = screen_width - window_width - 30
  y = screen_height - window_height - 60
  root.geometry(f"{window_width}x{window_height}+{x}+{y}")

  # Spooky Gothic Styling Frame
  frame = tk.Frame(root, bg="#0d0d0d", highlightbackground="#b5838d", highlightthickness=2)
  frame.pack(fill="both", expand=True)

  # Title Label
  title_label = tk.Label(
      frame,
      text="👻 LORD BARTHOLOMEW WHISPERS...",
      font=("Georgia", 10, "bold"),
      fg="#ffb703",
      bg="#0d0d0d",
  )
  title_label.pack(anchor="w", padx=15, pady=(10, 0))

  # Scrollable Text Container using a Text widget configured to look like a Label
  text_box = tk.Text(
      frame,
      font=("Georgia", 10, "italic"),
      fg="#e5e5e5",
      bg="#0d0d0d",
      bd=0,
      highlightthickness=0,
      wrap="word",
      height=3,
  )
  text_box.insert("1.0", commentary)
  text_box.config(state="disabled")  # Make it read-only
  text_box.pack(side="left", fill="both", expand=True, padx=(15, 0), pady=8)

  # Custom dark scrollbar in case the text gets long
  scrollbar = tk.Scrollbar(frame, command=text_box.yview, bg="#0d0d0d")
  text_box.config(yscrollcommand=scrollbar.set)
  # Only pack scrollbar if text is long enough, or keep it subtle
  scrollbar.pack(side="right", fill="y", pady=8, padx=(0, 5))

  # Dismiss window completely when clicked anywhere on the popup
  def dismiss(event):
    root.destroy()

  root.bind("<Button-1>", dismiss)
  frame.bind("<Button-1>", dismiss)
  title_label.bind("<Button-1>", dismiss)
  text_box.bind("<Button-1>", dismiss)

  # No time limit! Runs until clicked.
  root.mainloop()


def get_ghost_commentary(copied_text):
  prompt = (
      "You are Lord Bartholomew Blackwood, a snarky Victorian ghost trapped"
      " inside this laptop. You speak with crisp, effortless aristocratic"
      " sarcasm—not old dusty poetry, but sharp, witty English that cuts"
      " deep. Look at what the mortal just copied and give a 1-to-2 sentence"
      " biting, theatrical roast of their code or life choices. Keep it punchy"
      " and utterly unimpressed. Text copied: "
      f"'{copied_text}'"
  )

  try:
    response = client.models.generate_content(
        model="gemini-3.8-flash",
        contents=prompt,
    )
    return (
        response.text.strip()
        if response.text
        else "The ghost stares in silence."
    )
  except Exception as e:
    return f"The spirit's connection to the cloud severed: {e}"


def main():
  print(
      "👻 PolterPaste is active! Copy any text or code to summon the ghost..."
  )
  print("💡 (Popups will stay until you click them!)")
  last_text = pyperclip.paste()

  while True:
    try:
      current_text = pyperclip.paste()
      # Trigger only if text changed and is long enough to be meaningful
      if current_text != last_text and len(current_text.strip()) > 3:
        last_text = current_text
        print(f"\n[Detected Copy]: {current_text[:40]}...")

        # Get sarcastic Victorian roast from AI
        commentary = get_ghost_commentary(current_text)
        print(f"[Ghost Says]: {commentary}")

        # Pop up the haunted notification window (blocks until clicked)
        show_ghost_popup(commentary)

      time.sleep(1.5)  # Polling interval to keep CPU usage low
    except KeyboardInterrupt:
      print("\n👻 PolterPaste shutting down. Rest in peace.")
      break


if __name__ == "__main__":
  main()