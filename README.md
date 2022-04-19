Examples

```python
import json
from os import environ

from env_logging_config import create_config

environ['TEST_LOGGING_FORMATTERS.json.()'] = 'my.custom.new_formatter'

defaults = {
    'formatters': {
        'json': {'()': 'my.custom.formatter'}
    }
}

if __name__ == '__main__':
    print(
        json.dumps(
            create_config(
                'TEST_LOGGING_',
                defaults=defaults
            )
        )
    )
```
