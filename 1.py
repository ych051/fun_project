import tkinter as tk
from tkinter import font, simpledialog, messagebox, Toplevel


match_results = []
result_text_widget = None
result_window = None


def create_scoreboard():
    global player1_label, player2_label, timer_button, timer_var, score1, score2

    def increase_player1(amount):
        score1.set(score1.get() + amount)

    def decrease_player1():
        score1.set(max(0, score1.get() - 1))

    def increase_player2(amount):
        score2.set(score2.get() + amount)

    def decrease_player2():
        score2.set(max(0, score2.get() - 1))

    def reset_scores():
        score1.set(0)
        score2.set(0)
        reset_timer()

    def update_timer():
        if timer_running[0]:
            if timer_seconds[0] > 0:
                timer_seconds[0] -= 1
                minutes = timer_seconds[0] // 60
                seconds = timer_seconds[0] % 60
                timer_var.set(f"{minutes:02}:{seconds:02}")
                root.after(1000, update_timer)
            else:
                timer_running[0] = False
                timer_button.config(text="Start", bg="#5cb85c")

    def toggle_timer():
        if not timer_running[0]:
            timer_running[0] = True
            timer_button.config(text="Stop", bg="#f0ad4e")
            update_timer()
        else:
            timer_running[0] = False
            timer_button.config(text="Start", bg="#5cb85c")

    def reset_timer():
        timer_running[0] = False
        timer_seconds[0] = 120
        timer_var.set("02:00")
        timer_button.config(text="Start", bg="#5cb85c")

    def adjust_timer():
        new_time = simpledialog.askinteger("타이머 설정", "타이머 시간을 (초)로 입력하세요:", minvalue=30, maxvalue=300)
        if new_time:
            timer_seconds[0] = new_time
            minutes = new_time // 60
            seconds = new_time % 60
            timer_var.set(f"{minutes:02}:{seconds:02}")

    def change_player_name(player):
        if player == 1:
            new_name = simpledialog.askstring("Player 1 이름 변경", "새로운 이름을 입력하세요:")
            if new_name:
                player1_label.config(text=new_name)
        else:
            new_name = simpledialog.askstring("Player 2 이름 변경", "새로운 이름을 입력하세요:")
            if new_name:
                player2_label.config(text=new_name)

    # 경기 결과 저장
    def save_match_results():
        elapsed_seconds = 120 - timer_seconds[0]
        minutes = elapsed_seconds // 60
        seconds = elapsed_seconds % 60
        elapsed_time = f"{minutes:02}:{seconds:02}"

        match_result = (
            f"{player1_label.cget('text')}: {score1.get()} | "
            f"{player2_label.cget('text')}: {score2.get()} | "
            f"Time: {elapsed_time}"
        )
        match_results.append(match_result)
        messagebox.showinfo("저장 완료", "경기 결과가 저장되었습니다.")
        reset_scores()

    # 경기 결과 보기 창
    def show_results_page():
        global result_window, result_text_widget
        if result_window and result_window.winfo_exists():
            result_window.lift()
            return

        result_window = Toplevel(root)
        result_window.title("경기 결과")
        result_window.geometry("600x400")

        result_label = tk.Label(result_window, text="저장된 경기 결과", font=title_font)
        result_label.pack(pady=20)

        result_text_widget = tk.Text(result_window, wrap="word", font=button_font, height=15)
        result_text_widget.pack(padx=20, pady=10, fill="both", expand=True)

        result_text_widget.config(state="normal")
        result_text_widget.delete("1.0", tk.END)
        result_text_widget.insert("1.0", "\n".join(match_results))
        result_text_widget.config(state="disabled")

        tk.Button(result_window, text="결과 내보내기", font=button_font, command=export_results, bg="#5bc0de").pack(pady=10)

    def export_results():
        if match_results:
            with open("match_results_export.txt", "w") as file:
                file.write("\n".join(match_results))
            messagebox.showinfo("내보내기 완료", "경기 결과가 파일로 저장되었습니다.")
        else:
            messagebox.showwarning("경기 결과 없음", "저장된 경기 결과가 없습니다.")

    root = tk.Tk()
    root.title("Scoreboard")
    root.geometry("1920x1080")
    root.configure(bg="#f4f4f9")

    score1 = tk.IntVar(value=0)
    score2 = tk.IntVar(value=0)
    timer_var = tk.StringVar(value="02:00")
    timer_seconds = [120]
    timer_running = [False]

    title_font = font.Font(size=22, weight="bold")
    score_font = font.Font(size=150, weight="bold")
    button_font = font.Font(size=16, weight="bold")
    timer_font = font.Font(size=60, weight="bold")

    # Player 1 Section (Left)
    frame1 = tk.Frame(root, bg="#007acc", width=640, height=1080)
    frame1.pack_propagate(False)
    frame1.pack(side="left", fill="y")

    player1_label = tk.Label(frame1, text="Player 1", font=title_font, fg="black", bg="#007acc", cursor="hand2")
    player1_label.pack(pady=20)
    player1_label.bind("<Button-1>", lambda e: change_player_name(1))

    tk.Label(frame1, textvariable=score1, font=score_font, fg="white", bg="#007acc").pack(expand=True)

    tk.Button(frame1, text="+1", font=button_font, command=lambda: increase_player1(1)).pack(pady=10)
    tk.Button(frame1, text="+2", font=button_font, command=lambda: increase_player1(2)).pack(pady=10)
    tk.Button(frame1, text="-1", font=button_font, command=decrease_player1).pack(pady=10)

    # Player 2 Section (Right)
    frame2 = tk.Frame(root, bg="#d9534f", width=640, height=1080)
    frame2.pack_propagate(False)
    frame2.pack(side="right", fill="y")

    player2_label = tk.Label(frame2, text="Player 2", font=title_font, fg="black", bg="#d9534f", cursor="hand2")
    player2_label.pack(pady=20)
    player2_label.bind("<Button-1>", lambda e: change_player_name(2))

    tk.Label(frame2, textvariable=score2, font=score_font, fg="white", bg="#d9534f").pack(expand=True)

    tk.Button(frame2, text="+1", font=button_font, command=lambda: increase_player2(1)).pack(pady=10)
    tk.Button(frame2, text="+2", font=button_font, command=lambda: increase_player2(2)).pack(pady=10)
    tk.Button(frame2, text="-1", font=button_font, command=decrease_player2).pack(pady=10)

    # Timer Section (Center)
    center_frame = tk.Frame(root, bg="#f4f4f9")
    center_frame.pack(side="left", fill="y")

    tk.Label(center_frame, textvariable=timer_var, font=timer_font, fg="black", bg="#f4f4f9").pack(pady=60)
    timer_button = tk.Button(center_frame, text="Start", font=button_font, command=toggle_timer, bg="#5cb85c")
    timer_button.pack(pady=20)

    tk.Button(center_frame, text="Reset", font=button_font, command=reset_scores, bg="#d9534f").pack(pady=10)
    tk.Button(center_frame, text="경기 저장", font=button_font, command=save_match_results, bg="#f0ad4e").pack(pady=10)
    tk.Button(center_frame, text="경기 결과 보기", font=button_font, command=show_results_page, bg="#0275d8").pack(pady=10)

    root.mainloop()


if __name__ == "__main__":
    create_scoreboard()
