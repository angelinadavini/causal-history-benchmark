from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class TaskSpec:
    name: str
    relation_values: tuple[str, str]
    output_values: tuple[str, str]
    description: str


SAME_DIFFERENT = TaskSpec(
    name="same_different",
    relation_values=("SAME", "DIFFERENT"),
    output_values=("0", "1"),
    description="The same binary relation is learned from examples or stated directly.",
)

DAX_WUG = TaskSpec(
    name="dax_wug",
    relation_values=("DAX", "WUG"),
    output_values=("X", "Y"),
    description="An arbitrary DAX/WUG mapping is learned from examples or stated directly.",
)

TASKS = {task.name: task for task in (SAME_DIFFERENT, DAX_WUG)}
