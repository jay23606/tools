from pathlib import Path
from types import SimpleNamespace

import pytest

from nf_core.modules.lint.module_tests import _check_stub_gzip_syntax


@pytest.mark.parametrize("command", ["echo | gzip > ${prefix}.txt.gz", 'echo "" | gzip > ${prefix}.txt.gz'])
def test_stub_gzip_syntax_accepts_empty_echo(tmp_path: Path, command: str):
    main_nf = tmp_path / "main.nf"
    main_nf.write_text(f'''process test {{
    stub:
    """
    {command}
    """
}}''')
    module = SimpleNamespace(main_nf=main_nf, failed=[], passed=[])

    _check_stub_gzip_syntax(module)

    assert not module.failed
    assert any(result[1] == "test_stub_gzip_syntax" for result in module.passed)


@pytest.mark.parametrize("command", ['echo "data" | gzip > ${prefix}.txt.gz', "touch ${prefix}.txt.gz"])
def test_stub_gzip_syntax_rejects_non_gzip_or_nonempty_output(tmp_path: Path, command: str):
    main_nf = tmp_path / "main.nf"
    main_nf.write_text(f'''process test {{
    stub:
    """
    {command}
    """
}}''')
    module = SimpleNamespace(main_nf=main_nf, failed=[], passed=[])

    _check_stub_gzip_syntax(module)

    assert any(result[1] == "test_stub_gzip_syntax" for result in module.failed)
