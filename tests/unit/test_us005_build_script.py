"""Unit tests for US-005: Nuitka build script."""


def test_get_nuitka_args_includes_standalone() -> None:
    from build import get_nuitka_args

    assert "--standalone" in get_nuitka_args()


def test_get_nuitka_args_includes_pyside6_plugin() -> None:
    from build import get_nuitka_args

    assert "--enable-plugin=pyside6" in get_nuitka_args()


def test_get_nuitka_args_output_dir_points_to_dist() -> None:
    from build import get_nuitka_args

    assert any("--output-dir" in arg and "dist" in arg for arg in get_nuitka_args())


def test_get_nuitka_args_includes_entry_point() -> None:
    from build import get_nuitka_args

    assert any("main.py" in arg for arg in get_nuitka_args())


def test_get_nuitka_args_suppresses_console_on_windows() -> None:
    import sys

    from build import get_nuitka_args

    if sys.platform == "win32":
        assert "--windows-disable-console" in get_nuitka_args()
