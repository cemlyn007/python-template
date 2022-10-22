import pathlib
import zipfile

import build

from project import hello_world


def test_print_hello_world(capsys) -> None:
    hello_world.print_hello_world()

    captured = capsys.readouterr()
    assert captured.out == 'Hello World!\n'


def test_build(tmp_path) -> None:
    root = pathlib.Path('.')
    builder = build.ProjectBuilder(root)
    artifact_path = builder.build('wheel', tmp_path)
    assert artifact_path.endswith('.whl')
    assert zipfile.is_zipfile(artifact_path)

    want = [str(path.relative_to(root)) for path in root.glob('project/*.py')]

    with zipfile.ZipFile(artifact_path) as f:
        assert len(f.filelist) > 0
        got = [path.filename for path in f.filelist]
    got = [filename for filename in got if '.dist' not in filename]

    assert sorted(got) == sorted(want)
