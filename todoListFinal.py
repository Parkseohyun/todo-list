import json  # JSON 파일 작업을 위한 라이브러리
import os  # 파일 경로 및 파일 존재 여부 확인을 위한 라이브러리
import tkinter as tk  # GUI를 구성하기 위한 Tkinter 라이브러리
from tkinter import messagebox, simpledialog, ttk  # 메시지 박스, 입력창 및 스타일을 위한 모듈

# Task 클래스 정의: 개별 할 일을 관리
class Task:
    def __init__(self, title, description="", category="", priority="Low", completed=False):
        self.title = title  # 할 일 제목
        self.description = description  # 할 일 설명
        self.category = category  # 할 일 카테고리
        self.priority = priority  # 우선순위 (기본값: Low)
        self.completed = completed  # 완료 여부 (기본값: False)

    def mark_completed(self):
        self.completed = True  # 할 일을 완료 상태로 변경

    def __repr__(self):
        # 객체를 문자열로 표현할 때 반환할 형식
        return f"{self.title} ({self.category}, {self.priority}) - {'✔' if self.completed else '❌'}"

# JSON 파일로부터 할 일 목록을 불러오는 함수
def load_tasks():
    if os.path.exists('tasks.json'):  # tasks.json 파일이 존재하는지 확인
        with open('tasks.json', 'r') as file:  # 파일을 읽기 모드로 열기
            task_list = json.load(file)  # JSON 데이터를 파싱
            return [Task(**task) for task in task_list]  # Task 객체로 변환하여 반환
    return []  # 파일이 없을 경우 빈 리스트 반환

# 현재 할 일 목록을 JSON 파일에 저장하는 함수
def save_tasks(tasks):
    with open('tasks.json', 'w') as file:  # 파일을 쓰기 모드로 열기
        json.dump([task.__dict__ for task in tasks], file, indent=4)  # Task 객체를 딕셔너리로 변환 후 저장

# To-Do List 애플리케이션 클래스
class ToDoApp:
    def __init__(self, root):
        self.root = root  # Tkinter 창 객체 저장
        self.root.title("To-Do List Application")  # 창 제목 설정
        self.root.geometry("600x600")  # 창 크기 설정
        self.root.config(bg="#F0F4F8")  # 배경색 설정

        self.tasks = load_tasks()  # 저장된 할 일 목록 불러오기
        self.points = 0  # 초기 포인트 설정
        self.level = 1  # 초기 레벨 설정
        self.points_threshold = 100  # 레벨업 기준 포인트

        # 제목 라벨 생성
        tk.Label(root, text="My To-Do List", font=("Helvetica", 24, "bold"), bg="#F0F4F8", fg="#2C3E50").pack(pady=10)

        # 할 일 목록 프레임 생성
        self.task_list_frame = tk.Frame(root, bg="#F0F4F8")
        self.task_list_frame.pack(pady=10)

        # 할 일 목록 리스트박스 생성
        self.task_listbox = tk.Listbox(self.task_list_frame, width=50, height=10, font=("Helvetica", 12),
                                       bg="#ECF0F1", selectbackground="#3498DB", selectforeground="white")
        self.task_listbox.pack(side=tk.LEFT)

        # 스크롤바 생성
        self.scrollbar = tk.Scrollbar(self.task_list_frame)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.task_listbox.config(yscrollcommand=self.scrollbar.set)  # 리스트박스와 스크롤바 연결
        self.scrollbar.config(command=self.task_listbox.yview)  # 스크롤 이벤트 처리

        # 버튼 프레임 생성
        self.button_frame = tk.Frame(root, bg="#F0F4F8")
        self.button_frame.pack(pady=10)

        # 버튼 추가
        ttk.Button(self.button_frame, text="Add Task", command=self.add_task).grid(row=0, column=0, padx=5, pady=5)
        ttk.Button(self.button_frame, text="Mark as Completed", command=self.complete_task).grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(self.button_frame, text="Delete Task", command=self.delete_task).grid(row=0, column=2, padx=5, pady=5)
        ttk.Button(self.button_frame, text="Save Tasks", command=lambda: save_tasks(self.tasks)).grid(row=1, column=0, padx=5, pady=5)
        ttk.Button(self.button_frame, text="Load Tasks", command=self.refresh_task_list).grid(row=1, column=1, padx=5, pady=5)
        ttk.Button(self.button_frame, text="Search Task", command=self.search_task).grid(row=1, column=2, padx=5, pady=5)

        # 대시보드 프레임 생성
        self.dashboard_frame = tk.Frame(root, bg="#F0F4F8")
        self.dashboard_frame.pack(pady=20)

        # 대시보드 라벨 생성
        self.success_label = tk.Label(self.dashboard_frame, text="Completed: 0", font=("Helvetica", 14), bg="#F0F4F8")
        self.success_label.grid(row=0, column=0, padx=5, pady=5)
        self.failure_label = tk.Label(self.dashboard_frame, text="Failed: 0", font=("Helvetica", 14), bg="#F0F4F8")
        self.failure_label.grid(row=0, column=1, padx=5, pady=5)
        self.success_rate_label = tk.Label(self.dashboard_frame, text="Success Rate: 0%", font=("Helvetica", 14), bg="#F0F4F8")
        self.success_rate_label.grid(row=1, column=0, padx=5, pady=5)
        self.points_label = tk.Label(self.dashboard_frame, text="Points: 0", font=("Helvetica", 14), bg="#F0F4F8")
        self.points_label.grid(row=1, column=1, padx=5, pady=5)
        self.level_label = tk.Label(self.dashboard_frame, text="Level: 1", font=("Helvetica", 14), bg="#F0F4F8")
        self.level_label.grid(row=1, column=2, padx=5, pady=5)

        self.refresh_task_list()  # 할 일 목록 갱신

    # 리스트박스를 갱신하는 함수
    def refresh_task_list(self):
        self.task_listbox.delete(0, tk.END)  # 기존 리스트박스 내용 제거
        for task in self.tasks:
            self.task_listbox.insert(tk.END, task)  # 할 일 추가
        self.update_dashboard()  # 대시보드 갱신

    # 대시보드 갱신 함수
    def update_dashboard(self):
        completed_tasks = len([task for task in self.tasks if task.completed])  # 완료된 작업 수
        failed_tasks = len([task for task in self.tasks if not task.completed])  # 실패한 작업 수
        total_tasks = len(self.tasks)  # 전체 작업 수

        success_rate = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0  # 성공률 계산
        self.success_label.config(text=f"Completed: {completed_tasks}")  # 완료된 작업 라벨 갱신
        self.failure_label.config(text=f"Failed: {failed_tasks}")  # 실패한 작업 라벨 갱신
        self.success_rate_label.config(text=f"Success Rate: {success_rate:.2f}%")  # 성공률 라벨 갱신
        self.points_label.config(text=f"Points: {self.points}")  # 포인트 라벨 갱신
        self.level_label.config(text=f"Level: {self.level}")  # 레벨 라벨 갱신

    # 새로운 할 일 추가 함수
    def add_task(self):
        def save_new_task():
            title = title_entry.get()  # 제목 가져오기
            description = description_entry.get()  # 설명 가져오기
            category = category_entry.get()  # 카테고리 가져오기
            priority = priority_var.get()  # 우선순위 가져오기

            if title and category:  # 제목과 카테고리가 비어있지 않은 경우
                new_task = Task(title, description, category, priority)  # 새로운 Task 객체 생성
                self.tasks.append(new_task)  # 리스트에 추가
                save_tasks(self.tasks)  # 저장
                self.refresh_task_list()  # 갱신
                task_window.destroy()  # 창 닫기
            else:
                messagebox.showwarning("Input Error", "Title and Category are required!")  # 경고 메시지

        task_window = tk.Toplevel(self.root)  # 새 창 생성
        task_window.title("Add Task")  # 창 제목 설정
        task_window.geometry("400x300")  # 창 크기 설정

        # 입력 필드 및 라벨 생성
        tk.Label(task_window, text="Title:").pack(pady=5)
        title_entry = tk.Entry(task_window, width=30)
        title_entry.pack(pady=5)

        tk.Label(task_window, text="Description:").pack(pady=5)
        description_entry = tk.Entry(task_window, width=30)
        description_entry.pack(pady=5)

        tk.Label(task_window, text="Category:").pack(pady=5)
        category_entry = tk.Entry(task_window, width=30)
        category_entry.pack(pady=5)

        tk.Label(task_window, text="Priority:").pack(pady=5)
        priority_var = tk.StringVar(value="Low")
        priority_menu = tk.OptionMenu(task_window, priority_var, "High", "Medium", "Low")
        priority_menu.pack(pady=5)

        tk.Button(task_window, text="Save Task", command=save_new_task).pack(pady=10)

    # 할 일 완료로 표시 함수
    def complete_task(self):
        selected = self.task_listbox.curselection()  # 선택된 항목 인덱스 가져오기
        if selected:
            task = self.tasks[selected[0]]  # 선택된 할 일 가져오기
            task.mark_completed()  # 완료로 표시
            self.points += 10  # 포인트 추가

            while self.points >= self.points_threshold:  # 레벨업 조건 확인
                self.points -= self.points_threshold  # 포인트 차감
                self.level += 1  # 레벨 증가
                messagebox.showinfo("Level Up!", f"Congratulations! You've reached Level {self.level}.")  # 레벨업 메시지

            save_tasks(self.tasks)  # 데이터 저장
            self.refresh_task_list()  # 갱신
            messagebox.showinfo("Task Completed", f"Task '{task.title}' marked as completed!\n10 points awarded!")  # 완료 메시지
        else:
            messagebox.showwarning("Selection Error", "Please select a task to mark as completed.")  # 선택되지 않은 경우 경고

    # 할 일 삭제 함수
    def delete_task(self):
        selected = self.task_listbox.curselection()  # 선택된 항목 인덱스 가져오기
        if selected:
            task = self.tasks.pop(selected[0])  # 선택된 할 일 제거
            save_tasks(self.tasks)  # 데이터 저장
            self.refresh_task_list()  # 갱신
            messagebox.showinfo("Task Deleted", f"Task '{task.title}' has been deleted.")  # 삭제 메시지
       
    # 검색 기능 추가 함수
    def search_task(self):
        query = simpledialog.askstring("Search Task", "Enter task to search:")  # 검색어 입력 받기
        if query:  # 입력이 있으면
            for idx, task in enumerate(self.tasks):  # 모든 작업 탐색
                if query.lower() in task.title.lower():  # 제목에 검색어가 포함되어 있으면
                    self.task_listbox.selection_set(idx)  # 해당 작업 선택
                    self.task_listbox.activate(idx)  # 선택 활성화
                    break
            else:
                messagebox.showinfo("Not Found", "No matching task found.")  # 검색 결과 없을 때 메시지 표시


# 메인 함수
if __name__ == "__main__":
    root = tk.Tk()  # Tkinter 루트 창 생성
    app = ToDoApp(root)  # ToDoApp 인스턴스 생성
    root.mainloop()  # Tkinter 이벤트 루프 실행

