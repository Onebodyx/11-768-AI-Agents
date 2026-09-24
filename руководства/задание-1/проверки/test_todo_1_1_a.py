r"""Сценарии проверки TODO 1.1.a: активная история и чистый build_prompt().

Запуск всех сценариев из корня assignment-1 в Windows PowerShell:

    uv run pytest -p no:cacheprovider '..\руководства\задание-1\проверки\test_todo_1_1_a.py' -v --tb=short

Один сценарий отбирается по номеру, например: -k 07

Сценарии не обращаются к модели, Docker и сети и ничего не записывают на диск.
"""

from __future__ import annotations

import inspect
from copy import deepcopy

import pytest

from assignment.agent.base import Agent

# Поля, которые конструктор Agent создаёт до выполнения TODO 1.1.a.
ATTRIBUTES_BEFORE_TODO = {
    "env",
    "model",
    "client",
    "logs_save_path",
    "step_limit",
    "auto_stop_environment",
    "compact_threshold_tokens",
    "compaction_keep_recent_steps",
    "compaction_max_tokens",
    "system_prompt",
    "task_prompt",
    "api_prompts",
    "api_responses",
    "compaction_events",
    "tools",
    "finished",
    "steps_taken",
    "skills_path",
    "skills",
}
DOMAIN_TOOL_NAMES = (
    "execute",
    "send_message",
    "invoke_skill",
    "play_move",
    "simulate_move",
    "run_python",
)

SYSTEM_TEXT = "СИСТЕМНЫЕ-УКАЗАНИЯ-МАРКЕР"
TASK_TEXT = "ИСХОДНАЯ-ЗАДАЧА-МАРКЕР"
JOURNAL_TEXT = "ЖУРНАЛ-МАРКЕР-НЕ-ДОЛЖЕН-ПОПАСТЬ-В-ЗАПРОС"

START = [
    {"role": "system", "content": SYSTEM_TEXT},
    {"role": "user", "content": TASK_TEXT},
]
STEP_1 = [
    {
        "role": "assistant",
        "content": "Выполню два вызова.",
        "tool_calls": [
            {
                "id": "call_A",
                "type": "function",
                "function": {"name": "tool_a", "arguments": '{"x": 1}'},
            },
            {
                "id": "call_B",
                "type": "function",
                "function": {"name": "tool_b", "arguments": '{"y": 2}'},
            },
        ],
    },
    {"role": "tool", "tool_call_id": "call_A", "content": "результат A"},
    {"role": "tool", "tool_call_id": "call_B", "content": "результат B"},
]
STEP_2 = [
    {
        "role": "assistant",
        "content": "Теперь третий вызов.",
        "tool_calls": [
            {
                "id": "call_C",
                "type": "function",
                "function": {"name": "tool_c", "arguments": "{}"},
            },
        ],
    },
    {"role": "tool", "tool_call_id": "call_C", "content": "результат C"},
]


class FakeEnvironment:
    cwd = "/testbed"
    system, release, version, machine = "Linux", "6.1.0-check", "#1 SMP", "x86_64"

    def execute(self, command, **kwargs):
        raise AssertionError("build_prompt() не должен исполнять команды")


@pytest.fixture
def agent(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "check-key")
    monkeypatch.setenv("OPENAI_BASE_URL", "http://127.0.0.1:0/v1")
    created = Agent(FakeEnvironment(), model="check-model", auto_stop_environment=False)
    created.system_prompt = SYSTEM_TEXT
    created.task_prompt = TASK_TEXT
    return created


def build(agent: Agent) -> list:
    try:
        return agent.build_prompt()
    except NotImplementedError:
        pytest.fail(
            "build_prompt() вызывает NotImplementedError: TODO 1.1.a ещё не выполнен",
            pytrace=False,
        )


def history(agent: Agent) -> list:
    new_fields = sorted(set(vars(agent)) - ATTRIBUTES_BEFORE_TODO)
    list_fields = [name for name in new_fields if isinstance(getattr(agent, name), list)]
    if len(list_fields) != 1:
        pytest.fail(
            "в конструкторе Agent должно появиться ровно одно новое поле-список "
            f"для активной истории; новые поля: {new_fields}, из них списков: {list_fields}",
            pytrace=False,
        )
    return getattr(agent, list_fields[0])


def state(agent: Agent) -> dict:
    return deepcopy({k: v for k, v in vars(agent).items() if k not in {"client", "env"}})


def test_01_возвращает_список_без_NotImplementedError(agent):
    result = build(agent)
    assert isinstance(result, list), f"ожидался список сообщений, получено {type(result).__name__}"
    assert all(isinstance(m, dict) and "role" in m for m in result), (
        "каждое сообщение должно быть словарём с полем role"
    )


def test_02_первый_запрос_ровно_system_и_user(agent):
    assert build(agent) == START, (
        "первый запрос должен состоять ровно из system с system_prompt "
        "и user с task_prompt"
    )


def test_03_повторный_вызов_ничего_не_меняет(agent):
    before = state(agent)
    first = build(agent)
    second = build(agent)
    assert second == first, "два вызова подряд без новых действий дали разные запросы"
    assert state(agent) == before, "вызов build_prompt() изменил поля агента"


def test_04_каждый_вызов_возвращает_новые_объекты(agent):
    first = build(agent)
    second = build(agent)
    assert second is not first, "два вызова вернули один и тот же список"
    assert all(a is not b for a, b in zip(first, second)), (
        "два вызова вернули одни и те же объекты сообщений"
    )


def test_05_порча_результата_не_влияет_на_следующий_вызов(agent):
    spoiled = build(agent)
    spoiled.append({"role": "user", "content": "лишнее"})
    spoiled[0]["content"] = "ИСПОРЧЕНО"
    spoiled[1]["content"] = "ИСПОРЧЕНО"
    assert build(agent) == START, "изменение возвращённого результата изменило следующий запрос"


def test_06_новая_активная_история_пуста(agent):
    assert history(agent) == [], "сразу после создания агента активная история должна быть пустой"


def test_07_шаг_с_двумя_вызовами_попадает_в_запрос_по_порядку(agent):
    history(agent).extend(deepcopy(STEP_1))
    assert build(agent) == START + STEP_1, (
        "после шага запрос должен быть: system, user, assistant, tool A, tool B"
    )


def test_08_два_шага_без_повторов(agent):
    stored = history(agent)
    stored.extend(deepcopy(STEP_1 + STEP_2))
    build(agent)
    result = build(agent)
    assert result == START + STEP_1 + STEP_2, (
        "после двух шагов каждое сообщение должно входить в запрос ровно один раз и по порядку"
    )
    assert len(stored) == len(STEP_1 + STEP_2), (
        f"после вызовов build_prompt() в истории {len(stored)} сообщений вместо {len(STEP_1 + STEP_2)}"
    )


def test_09_глубокая_копия_защищает_tool_calls(agent):
    stored = history(agent)
    stored.extend(deepcopy(STEP_1))
    snapshot = deepcopy(stored)
    result = build(agent)
    result[2]["tool_calls"][0]["function"]["arguments"] = '{"x": "ИСПОРЧЕНО"}'
    result[2]["tool_calls"].append({"id": "call_Z"})
    result[3]["content"] = "ИСПОРЧЕНО"
    assert stored == snapshot, (
        "изменение вложенных tool_calls в результате изменило активную историю: "
        "копия неглубокая"
    )


def test_10_журналы_не_попадают_в_запрос(agent):
    agent.api_prompts.append([{"role": "user", "content": JOURNAL_TEXT}])
    agent.api_responses.append({"choices": [{"message": {"content": JOURNAL_TEXT}}]})
    agent.compaction_events.append({"summary": JOURNAL_TEXT})
    assert JOURNAL_TEXT not in repr(build(agent)), (
        "содержимое api_prompts, api_responses или compaction_events попало в запрос"
    )


def test_11_нет_имён_предметных_инструментов():
    source = inspect.getsource(Agent.build_prompt)
    found = [name for name in DOMAIN_TOOL_NAMES if f'"{name}"' in source or f"'{name}'" in source]
    assert not found, f"общий build_prompt() упоминает предметные инструменты: {found}"
