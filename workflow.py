"""Lesson-specific workflow. Read this file before the execution adapter."""
from __future__ import annotations
import asyncio
import json
from pathlib import Path
from runtime import atomic_json, contained_path, in_process_tool

async def run(agent, data):
    from runtime import TransientError
    adaptations = []
    selected = data['primary']
    try:
        result = await agent.ask('primary', 'Complete the assigned task.', data['task'], 'The primary specialist prepared the summary.')
    except TransientError:
        selected = data['backup']
        adaptations.append({'from': data['primary'], 'to': selected, 'reason': 'observed transient failure'})
        result = await agent.ask('backup', 'Complete this reassigned task. Disclose that it is a fallback.', data['task'], 'Fallback summary from the generalist; review the policy details.')
    return {'selected': selected, 'adaptations': adaptations, 'result': result, 'max_reconfigurations': 1}
