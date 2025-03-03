import threading
from unittest.mock import patch

import pytest

from command_line_assistant.utils import renderers


def test_create_error_renderer(capsys: pytest.CaptureFixture[str]):
    renderer = renderers.create_error_renderer()
    renderer.render("errored out")

    captured = capsys.readouterr()
    assert "\x1b[31m🙁 errored out\x1b[0m\n" in captured.err


def test_create_spinner_renderer(capsys, mock_stream):
    with patch("command_line_assistant.rendering.stream.StdoutStream", mock_stream):
        spinner = renderers.create_spinner_renderer(message="Loading...", decorators=[])
        spinner.start()
        assert isinstance(spinner._spinner_thread, threading.Thread)
        assert spinner._spinner_thread.is_alive()

        spinner.stop()
        assert not spinner._spinner_thread.is_alive()
        assert spinner._done.is_set()

        captured = capsys.readouterr().out
        assert "Loading..." in captured


def test_create_text_renderer(capsys: pytest.CaptureFixture[str]):
    renderer = renderers.create_text_renderer()
    renderer.render("errored out")

    captured = capsys.readouterr()
    print(captured)
    assert "rrored out\n" in captured.out


@pytest.mark.parametrize(
    ("size", "expected"),
    (
        (248, "248.00 B"),
        (2048, "2.00 KB"),
        (2000048, "1.91 MB"),
        (2000000048, "1.86 GB"),
        (2000000000408, "1.82 TB"),
        (2000000000000408, "1.78 PB"),
    ),
)
def test_human_readable_size(size, expected):
    assert renderers.human_readable_size(size) == expected
