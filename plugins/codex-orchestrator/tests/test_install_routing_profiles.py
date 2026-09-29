import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest


PLUGIN = Path(__file__).resolve().parents[1]
HOOKS = json.loads((PLUGIN / 'hooks/hooks.json').read_text())['hooks']
HOOK = HOOKS['SessionStart'][0]['hooks'][0]
PROMPT_HOOK = HOOKS['UserPromptSubmit'][0]['hooks'][0]


class PromptReminderHookTests(unittest.TestCase):
    def test_prompt_hook_filters_child_and_invalid_input(self):
        with tempfile.TemporaryDirectory(prefix='codex orchestrator prompt ') as temporary:
            home = Path(temporary)
            env = {**os.environ, 'PLUGIN_ROOT': str(PLUGIN)}
            if os.name == 'nt':
                env['PSEXECUTIONPOLICYPREFERENCE'] = 'Restricted'
            command = PROMPT_HOOK['commandWindows' if os.name == 'nt' else 'command']
            command = command.replace('${PLUGIN_ROOT}', str(PLUGIN))
            parent = {'hook_event_name': 'UserPromptSubmit',
                      'prompt': 'agent_id in text', 'metadata': {'agent_type': 'nested'}}
            cases = [
                (parent, True),
                ({**parent, 'agent_id': 'child-1'}, False),
                ({**parent, 'agent_type': 'default'}, False),
                ({**parent, 'agent_id': 'child-1', 'agent_type': 'default'}, False),
                ({**parent, 'agent_id': None}, False),
                ({**parent, 'agent_id': ''}, False),
                ({**parent, 'agent_id': False}, False),
                ({**parent, 'agent_type': False}, False),
                ({**parent, 'agent_type': None}, False),
                ({**parent, 'agent_type': ''}, False),
                ({**parent, 'agent_id': None, 'agent_type': ''}, False),
                ('', False),
                ('{', False),
                (None, False),
                (False, False),
                ([], False),
                ([parent], False),
                ({'prompt': 'hello'}, False),
                ({'HOOK_EVENT_NAME': 'UserPromptSubmit'}, False),
                ({**parent, 'hook_event_name': 'SessionStart'}, False),
                ({**parent, 'hook_event_name': ['UserPromptSubmit']}, False),
                ({**parent, 'hook_event_name': True}, False),
                ({**parent, 'hook_event_name': {'name': 'UserPromptSubmit'}}, False),
                ({**parent, 'hook_event_name': 'userpromptsubmit'}, False),
            ]
            reminder = (PLUGIN / 'hooks/prompt-reminder.txt').read_text()
            for payload, should_emit in cases:
                with self.subTest(payload=payload):
                    input_text = payload if isinstance(payload, str) else json.dumps(payload)
                    result = subprocess.run(command, shell=True, cwd=home, env=env,
                                            input=input_text, capture_output=True,
                                            text=True, timeout=10)
                    self.assertEqual(result.returncode, 0, result.stderr)
                    self.assertEqual(result.stderr, '')
                    # PowerShell adds a transport newline after Get-Content -Raw output.
                    if should_emit:
                        self.assertEqual(result.stdout.rstrip('\r\n'), reminder.rstrip('\r\n'))
                    else:
                        self.assertEqual(result.stdout, '')


class InstallRoutingProfilesTests(unittest.TestCase):
    def test_hook_installs_missing_profiles_and_preserves_existing_files(self):
        with tempfile.TemporaryDirectory(prefix='codex orchestrator profiles ') as temporary:
            home = Path(temporary)
            # Run the packaged hook from an unrelated working directory.
            env = {**os.environ, 'CODEX_HOME': str(home), 'PLUGIN_ROOT': str(PLUGIN)}
            if os.name == 'nt':
                # Exercise Windows' Restricted policy, not the CI runner's permissive default.
                env['PSEXECUTIONPOLICYPREFERENCE'] = 'Restricted'
                powershell = ['powershell.exe', '-NoProfile', '-NonInteractive']
                script = home / 'blocked.ps1'
                script.write_text('exit 0')
                blocked = subprocess.run(powershell + ['-File', str(script)], env=env,
                                         capture_output=True, text=True)
                self.assertNotEqual(blocked.returncode, 0, 'Restricted must reject .ps1 files')
                self.assertIn('UnauthorizedAccess', blocked.stderr)
            command = HOOK['commandWindows' if os.name == 'nt' else 'command']
            command = command.replace('${PLUGIN_ROOT}', str(PLUGIN))
            catalog = home / 'subagent-router'

            def run_hook():
                result = subprocess.run(command, shell=True, cwd=home, env=env,
                                        capture_output=True, text=True, timeout=10)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertEqual(result.stdout, '')

            run_hook()
            sources = list((PLUGIN / 'routing').glob('codex-orchestrator-*.json'))
            self.assertEqual(len(sources), 3)
            for source in sources:
                self.assertEqual((catalog / source.name).read_bytes(), source.read_bytes())

            customized = catalog / 'codex-orchestrator-routine.json'
            customized.write_text('{"model": "my-custom-model"}')
            other = catalog / 'other-plugin.json'
            other.write_text('{"model": "another-plugin-model"}')
            before = {p.name: p.read_bytes() for p in catalog.iterdir()}
            missing = catalog / 'codex-orchestrator-complex.json'
            missing.unlink()
            run_hook()
            run_hook()
            self.assertEqual({p.name: p.read_bytes() for p in catalog.iterdir()}, before)


if __name__ == '__main__':
    unittest.main()
