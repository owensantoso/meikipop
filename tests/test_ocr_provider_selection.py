"""Offline tests of the actual OCR module; no config files, OCR engines or network.

Only import boundaries for the config singleton, abstract type and remote
package are substituted. OcrProcessor construction/switching are real code.
"""
import importlib.util
from pathlib import Path
from types import ModuleType, SimpleNamespace
import sys
import threading
import unittest
from unittest.mock import patch

SOURCE = Path(__file__).resolve().parents[1] / "src/meikipop/ocr/ocr.py"


class ProviderSelectionTests(unittest.TestCase):
    def setUp(self):
        self.config = SimpleNamespace(
            ocr_provider="Selected local", auto_scan_mode=False,
            saves=0,
        )
        def save():
            self.config.saves += 1
        self.config.save = save
        config_module = ModuleType("meikipop.config.config")
        config_module.config = self.config
        interface = ModuleType("meikipop.ocr.interface")
        interface.OcrProvider = type("OcrProvider", (), {})
        self.constructions = []
        self.local = self.provider("Selected local")
        self.remote = self.provider("Google Lens (remote)")
        remote_module = ModuleType("meikipop.ocr.providers.glensv2")
        remote_module.GoogleLensOcrV2 = self.remote
        # Include the legacy import so these regressions can run unchanged
        # against the old source and demonstrate the unwanted fallback.
        imports = {
            "meikipop.config.config": config_module,
            "meikipop.ocr.interface": interface,
            "meikipop.ocr.providers.glensv2": remote_module,
        }
        self.imports = patch.dict(sys.modules, imports)
        self.imports.start()
        self.addCleanup(self.imports.stop)
        spec = importlib.util.spec_from_file_location("ocr_selection_under_test", SOURCE)
        self.module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.module)
        self.processor = self.module.OcrProcessor
        self.triggered = []
        self.shared = SimpleNamespace(
            hit_scan_queue=SimpleNamespace(put=lambda value: self.triggered.append(value)),
            screenshot_trigger_event=threading.Event(),
        )
        self.screen = SimpleNamespace(force_screenshot_trigger=lambda: self.triggered.append("capture"))

    def provider(self, name, failure=None):
        calls = self.constructions
        class FakeProvider:
            NAME = name
            def __init__(self):
                calls.append(name)
                if failure:
                    raise failure
        return FakeProvider

    def construct(self, available):
        with patch.object(self.processor, "_discover_providers", return_value=available):
            return self.processor(self.shared, self.screen)

    def test_missing_local_never_constructs_remote(self):
        with self.assertLogs(self.module.logger, level="CRITICAL") as logs:
            with self.assertRaises(SystemExit) as stopped:
                self.construct({self.remote.NAME: self.remote})
        self.assertEqual(stopped.exception.code, 1)
        self.assertEqual(self.constructions, [])
        self.assertEqual(self.config.ocr_provider, "Selected local")
        self.assertEqual(self.config.saves, 0)
        self.assertIn("Selected local", " ".join(logs.output))

    def test_unknown_selection_does_not_pick_first_available(self):
        self.config.ocr_provider = "Unavailable selection"
        with self.assertRaises(SystemExit):
            self.construct({self.local.NAME: self.local})
        self.assertEqual(self.constructions, [])
        self.assertEqual(self.config.ocr_provider, "Unavailable selection")

    def test_failed_local_never_constructs_remote(self):
        failing = self.provider("Selected local", RuntimeError("synthetic initialization failure"))
        with self.assertRaises(SystemExit) as stopped:
            self.construct({failing.NAME: failing, self.remote.NAME: self.remote})
        self.assertEqual(stopped.exception.code, 1)
        self.assertEqual(self.constructions, ["Selected local"])
        self.assertEqual(self.config.ocr_provider, "Selected local")
        self.assertEqual(self.config.saves, 0)

    def test_selected_local_is_used_even_if_remote_is_first(self):
        processor = self.construct({self.remote.NAME: self.remote, self.local.NAME: self.local})
        self.assertEqual(processor.ocr_backend.NAME, "Selected local")
        self.assertEqual(self.constructions, ["Selected local"])
        self.assertEqual(self.config.saves, 0)

    def test_explicit_remote_is_still_allowed(self):
        self.config.ocr_provider = self.remote.NAME
        processor = self.construct({self.local.NAME: self.local, self.remote.NAME: self.remote})
        self.assertEqual(processor.ocr_backend.NAME, self.remote.NAME)
        self.assertEqual(self.constructions, [self.remote.NAME])
        self.assertEqual(self.config.saves, 0)

    def test_failed_explicit_remote_does_not_substitute_local(self):
        self.config.ocr_provider = self.remote.NAME
        failed = self.provider(self.remote.NAME, RuntimeError("synthetic remote initialization failure"))
        with self.assertRaises(SystemExit):
            self.construct({self.local.NAME: self.local, failed.NAME: failed})
        self.assertEqual(self.constructions, [self.remote.NAME])
        self.assertEqual(self.config.ocr_provider, self.remote.NAME)

    def test_explicit_manual_switch_still_saves_and_triggers_capture(self):
        processor = self.construct({self.local.NAME: self.local, self.remote.NAME: self.remote})
        self.config.auto_scan_mode = True
        processor.switch_provider(self.remote.NAME)
        self.assertEqual(self.constructions, [self.local.NAME, self.remote.NAME])
        self.assertEqual(self.config.ocr_provider, self.remote.NAME)
        self.assertEqual(self.config.saves, 1)
        self.assertEqual(self.triggered, [None, "capture"])
        self.assertTrue(self.shared.screenshot_trigger_event.is_set())

    def test_failed_manual_switch_keeps_previous_selected_provider(self):
        failed = self.provider(self.remote.NAME, RuntimeError("synthetic switch failure"))
        processor = self.construct({self.local.NAME: self.local, failed.NAME: failed})
        previous = processor.ocr_backend
        processor.switch_provider(failed.NAME)
        self.assertIs(processor.ocr_backend, previous)
        self.assertEqual(self.config.ocr_provider, self.local.NAME)
        self.assertEqual(self.triggered, [])

    def test_no_providers_preserves_existing_startup_failure(self):
        with self.assertRaises(SystemExit) as stopped:
            self.construct({})
        self.assertEqual(stopped.exception.code, 1)
        self.assertEqual(self.constructions, [])

    def test_successful_startup_does_not_start_the_worker(self):
        with patch.object(threading.Thread, "start") as start:
            self.construct({self.local.NAME: self.local})
        start.assert_not_called()


if __name__ == "__main__":
    unittest.main()
