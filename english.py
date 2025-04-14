import tkinter as tk
from tkinter import messagebox, simpledialog
import json
import random

# ------------------ 학습 모드 선택 ------------------

class ModeSelectApp:
    def __init__(self, root):
        self.root = root
        self.root.title("학습 모드 선택")
        self.root.geometry("400x300")
        self.root.resizable(False, False)

        self.label = tk.Label(root, text="학습 모드를 선택하세요", font=("Arial", 20, "bold"))
        self.label.pack(pady=30)

        self.all_words_button = tk.Button(root, text="모든 단어 학습", font=("Arial", 14), bg="#4CAF50", fg="white", command=self.select_all_words)
        self.all_words_button.pack(pady=10)

        self.wrong_words_button = tk.Button(root, text="오답 단어 복습", font=("Arial", 14), bg="#2196F3", fg="white", command=self.select_wrong_words)
        self.wrong_words_button.pack(pady=10)

    def select_all_words(self):
        self.root.destroy()
        start_learning("words.json")

    def select_wrong_words(self):
        self.root.destroy()
        start_learning("wrong_words.json")

# ------------------ 단어 학습 ------------------

class WordApp:
    def __init__(self, root, word_file):
        self.root = root
        self.root.title("영어 단어 암기 프로그램")
        self.root.geometry("450x500")
        self.root.resizable(False, False)

        self.word_file = word_file
        self.words = self.load_words()
        self.current_word = None
        self.correct_count = 0
        self.total_count = 0

        self.word_label = tk.Label(root, text="단어를 불러오는 중...", font=("Arial", 24, "bold"))
        self.word_label.pack(pady=30)

        self.entry = tk.Entry(root, font=("Arial", 16))
        self.entry.pack(pady=20)

        self.check_button = tk.Button(root, text="확인", font=("Arial", 14), bg="#4CAF50", fg="white", command=self.check_answer)
        self.check_button.pack(pady=8)

        self.next_button = tk.Button(root, text="다음 문제", font=("Arial", 14), bg="#2196F3", fg="white", command=self.next_word)
        self.next_button.pack(pady=8)

        self.manage_button = tk.Button(root, text="단어 수정/삭제", font=("Arial", 14), bg="#FFC107", command=self.open_word_manager)
        self.manage_button.pack(pady=15)

        self.score_label = tk.Label(root, text="점수: 0/0", font=("Arial", 14))
        self.score_label.pack(pady=10)

        self.next_word()

    def load_words(self):
        try:
            with open(self.word_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            messagebox.showerror("에러", f"{self.word_file} 파일을 찾을 수 없습니다.")
            self.root.destroy()

    def next_word(self):
        if not self.words:
            messagebox.showinfo("완료", "모든 문제를 풀었습니다!")
            self.root.destroy()
            return
        self.current_word = random.choice(self.words)
        self.word_label.config(text=self.current_word["english"])
        self.entry.delete(0, tk.END)

    def check_answer(self):
        user_input = self.entry.get().strip()
        correct_answer = self.current_word["korean"]

        self.total_count += 1

        if user_input == correct_answer:
            messagebox.showinfo("정답!", "정답입니다!")
            self.correct_count += 1
        else:
            messagebox.showerror("오답", f"틀렸어요!\n정답: {correct_answer}")
            self.save_wrong_word(self.current_word)

        self.update_score()
        self.next_word()

    def update_score(self):
        self.score_label.config(text=f"점수: {self.correct_count}/{self.total_count}")

    def save_wrong_word(self, word):
        try:
            with open("wrong_words.json", "r", encoding="utf-8") as f:
                wrong_words = json.load(f)
        except FileNotFoundError:
            wrong_words = []

        if word not in wrong_words:
            wrong_words.append(word)
            with open("wrong_words.json", "w", encoding="utf-8") as f:
                json.dump(wrong_words, f, indent=4, ensure_ascii=False)

    def open_word_manager(self):
        WordManagerApp(tk.Toplevel(self.root))

# ------------------ 단어 수정/삭제 ------------------

class WordManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("단어 수정/삭제")
        self.root.geometry("400x300")
        self.root.resizable(False, False)

        self.words = self.load_words()

        self.modify_button = tk.Button(root, text="단어 수정", font=("Arial", 14), bg="#00BCD4", fg="white", command=self.modify_word)
        self.modify_button.pack(pady=20)

        self.delete_button = tk.Button(root, text="단어 삭제", font=("Arial", 14), bg="#F44336", fg="white", command=self.delete_word)
        self.delete_button.pack(pady=20)

    def load_words(self):
        try:
            with open("words.json", "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            messagebox.showerror("에러", "words.json 파일을 찾을 수 없습니다.")
            return []

    def save_words(self):
        with open("words.json", "w", encoding="utf-8") as f:
            json.dump(self.words, f, indent=4, ensure_ascii=False)

    def modify_word(self):
        target = simpledialog.askstring("수정할 단어", "수정할 영어 단어를 입력하세요:")
        for word in self.words:
            if word['english'] == target:
                new_english = simpledialog.askstring("새 영어 단어", "새 영어 단어를 입력하세요:")
                new_korean = simpledialog.askstring("새 한국어 뜻", "새 한국어 뜻을 입력하세요:")
                word['english'] = new_english
                word['korean'] = new_korean
                self.save_words()
                messagebox.showinfo("완료", "단어 수정이 완료되었습니다.")
                return
        messagebox.showerror("오류", "해당 단어를 찾을 수 없습니다.")

    def delete_word(self):
        target = simpledialog.askstring("삭제할 단어", "삭제할 영어 단어를 입력하세요:")
        for word in self.words:
            if word['english'] == target:
                self.words.remove(word)
                self.save_words()
                messagebox.showinfo("완료", "단어 삭제가 완료되었습니다.")
                return
        messagebox.showerror("오류", "해당 단어를 찾을 수 없습니다.")

# ------------------ 프로그램 시작 ------------------

def start_learning(word_file):
    root = tk.Tk()
    app = WordApp(root, word_file)
    root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    app = ModeSelectApp(root)
    root.mainloop()
