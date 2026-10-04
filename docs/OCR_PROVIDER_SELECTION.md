# OCR provider selection at startup

Startup uses exactly the provider named by `ocr_provider` in the `[Settings]`
section of `config.ini`. It does not substitute Google Lens or the first discovered
provider when the selected one is unavailable or its constructor fails. This
keeps a missing local backend from silently changing where screen images are sent.
An explicitly selected remote provider remains supported.

When initialization fails, startup logs the selected name and exits with code 1.
Restore that provider's dependencies, or deliberately change `ocr_provider` in the
application's platform-specific `config.ini` to an available provider and restart.
The failed startup does not save or replace the configured selection. Because it
stops before the tray is created, the tray cannot repair that startup failure.
After successful startup, explicit selection through the OCR Provider tray menu
continues to save the choice and request a new scan as before.

This change covers unavailable providers and constructors that raise. A provider
whose constructor catches its own failure and returns an unusable instance needs
separate health reporting; this selection guard does not detect that case.

## Offline verification

From the repository root, run:

```sh
python -m unittest discover -s tests -p 'test_ocr_provider_selection.py' -v
```

The tests import the actual OCR module, substituting only its configuration
singleton, provider type and fake provider classes. They exercise processor
construction and manual switches without reading user configuration, running OCR,
capturing screens, downloading models, using Qt or making network requests.

Frozen packages still explicitly include each provider through the existing
platform `.spec` files. No provider package or stable `NAME` changed here. Actual
packaged-app startup, tray behavior and physical capture remain manual checks.
The later native macOS bridge is a separate implementation and is not validated by
these Python-reference tests.
