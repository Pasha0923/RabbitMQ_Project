from mytasks import add

if __name__ == '__main__':
    result = add.delay(1, 1)
    print(result.id)

# ВАЖНО 1
# Broker (Redis DB 0) — хранит очередь задач до их выполнения.
# Backend (Redis DB 1) — хранит результаты уже выполненных задач.

# ВАЖНО 1
# celery -A mytasks worker -P solo -l info
# Это самый распространенный способ работы с Celery на Windows.

# ВАЖНО 1
# taskkill /F /IM python.exe
# Это завершит все процессы Python.


# Способ 1. Через Python (самый простой)
# Сценарий 1. Посмотреть сообщение (задачу), которое лежит в очереди

# Worker НЕ должен быть запущен.

# Порядок действий:

# 1. Запускаешь Redis
# docker start redis
# 2. НЕ запускаешь
# celery -A mytasks worker --loglevel=info
# 3. Запускаешь
# python app.py

# В этот момент задача попадает в очередь Redis.

# Как посмотреть содержимое Redis?
# Через redis-cli (самый простой)

# Теперь заходишь в Redis: в терминале:
# docker exec -it redis redis-cli   
# По умолчанию ты попадешь в базу 0, которая у тебя является брокером.

# 3.1 
# Проверяешь ключи:
# KEYS *
# 3.2 
# или лучше (для больших БД рекомендуется именно так):
# SCAN 0

# Если задача еще не обработана воркером, ты можешь увидеть список:
# 4. Смотришь
# LRANGE celery 0 -1
# Ты увидишь сериализованное сообщение, очень похожее на JSON из учебника (хотя внутри часть полей, например body, будет закодирована в Base64).


# 1. Как красиво вывести результат задачи из Redis (DB 1)?
# Сначала выйди из redis-cli терминла (команда quit)
# 2. В обычном терминале  терминале выполни команду:
# Можно одной командой прочитать сообщение из Redis и красиво вывести его:
# python -c "import redis, json; r=redis.Redis(host='localhost', port=6379, db=0, decode_responses=True); print(json.dumps(json.loads(r.lindex('celery',0)), indent=4, ensure_ascii=False))"


# Сценарий 2. Посмотреть результат выполнения задачи
# Здесь worker уже должен работать.

# Последовательность такая:
# Шаг 1
# Запускаешь Redis.
# docker start redis

# Шаг 2
# Запускаешь worker
# celery -A mytasks worker --loglevel=info

# Шаг 3
# В другом терминале
# python app.py
# Worker выполняет
# add(1, 1)
# и получает результат 2

# Шаг 3.1
# Celery сохраняет этот результат в Backend.
# У тебя Backend указан:
# BACKEND_URL = "redis://localhost:6379/1" , То есть сохраняется результат в базу Redis №1.

# # Теперь заходишь в Redis: в терминале:
# docker exec -it redis redis-cli   
# # docker exec -it redis redis-cli ping

# SELECT 1
# Проверяешь ключи:

# KEYS *
# Например увидишь

# celery-task-meta-ac7cf951-3e7f-40e0-9934-7fa972943181


# И читаешь его

# GET celery-task-meta-ac7cf951-3e7f-40e0-9934-7fa972943181

# Там будет JSON примерно такого вида:

# {
#     "status": "SUCCESS",
#     "result": 2,
#     "traceback": null,
#     "children": [],
#     "date_done": "...",
#     "task_id": "98d133e0-5347-4b67-a397-e6aaa699e0ab"
# }

# 1. Как красиво вывести результат задачи из Redis (DB 1)?
# Сначала выйди из redis-cli терминла (команда quit)
# 2. В обычном терминале  терминале выполни команду:
# python -c "import redis, json; r=redis.Redis(host='localhost', port=6379, db=1, decode_responses=True); data=r.get('celery-task-meta-ac7cf951-3e7f-40e0-9934-7fa972943181'); print(json.dumps(json.loads(data), indent=4, ensure_ascii=False))"