# Logging

Markprint uses standard library logging by default and can optionally integrate with `ultilog`.

```toml
[tool.markprint.logging]
enabled = true
backend = "ultilog"
preset = "dev"
level = "INFO"
```
