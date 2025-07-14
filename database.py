import aiosqlite
from datetime import datetime, timedelta



async def create_table():
    async with aiosqlite.connect("Tasks.db") as db:
        await db.execute("CREATE TABLE IF NOT EXISTS tasks(" \
        "id INTEGER PRIMARY KEY AUTOINCREMENT," \
        "user_id INTEGER," \
        "task TEXT," \
        "discription TEXT," \
        "deadline_str DATETIME," \
        "status TEXT DEFAULT 'active')")
        await db.commit()



async def select_task(index: int):
    async with aiosqlite.connect("Tasks.db") as db:
        await db.execute("SELECT id FROM tasks WHERE id = ?", (index))
        await db.commit()



async def add_tasks(task: str, discription: str, deadline_str: str, user_id: int, status: str = "active"):
    deadline = datetime.strptime(deadline_str, "%Y-%m-%d %H:%M")
    async with aiosqlite.connect("Tasks.db") as db:
        await db.execute("INSERT INTO tasks (user_id, task, discription, deadline_str, status) VALUES(?, ?, ?, ?, ?)", (user_id, task, discription, deadline, status))
        await db.commit()



async def get_user_id():
    async with aiosqlite.connect("Tasks.db") as db:
        await db.execute("SELECT user_id FROM tasks")
        await db.commit()



async def get_upcoming_deadlines(hourse_before: int = 24):
    """Get tasks that have a deadline within `hours_before` hours"""
    now = datetime.now()
    datetime_threshold = now + timedelta(hours=hourse_before)

    async with aiosqlite.connect("Tasks.db") as db:
        cursor = await db.execute("SELECT id, task, deadline_str FROM tasks" \
        "WHERE deadline_str BETWEEN ? AND ?  AND status = 'active",
        (now, datetime_threshold)
        )
        return cursor.fetchall()



async def mark_task_as_done(task_id: int):
    async with aiosqlite.connect("Tasks.db") as db:
        await db.execute("UPDATE tasks SET status = 'completed' WHERE id = ?",
                          (task_id,))
        await db.commit()



async def get_user_task(user_id: int, task_id: int):
    async with aiosqlite.connect("Tasks.db") as db:
        params = (int(user_id), int(task_id))
        cursor = await db.execute(
            "SELECT id, task as name FROM tasks "
            "WHERE id = ? AND user_id = ? AND status = 'active'", params
                                  )
        await cursor.fetchone()



async def get_all_information():
    try:
        async with aiosqlite.connect("Tasks.db") as db:
            cursor = await db.execute("SELECT id, task, discription, deadline_str, status FROM tasks")
            tasks = await cursor.fetchall()

            if not tasks:
                return "В базе нет данеы"

            result = []
            for task in tasks:
                task_id, name, discription, deadline, status = task
                task_info = (
                    f"ID: {task_id or 'нет данных'}\n"
                    f"NAME: {name or 'нет данных'}\n"
                    f"DISCRIPTION: {discription or 'нет данных'}\n"
                    f"DEADLINE: {deadline or 'нет данных'}\n"
                    f"STATUS: {status or 'нет данных'}\n"
            )
            result.append(task_info)
           
        return "\n\n".join(result)
    except aiosqlite.Error as e:
        return print(f"Ошибка базы данных {e}")
    except Exception as e:
        print(f"Ошибка базы данных {e}")