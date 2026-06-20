import os

from pyexcel_io.readers.csv_in_file import FileReader


def test_file_reader_with_plus_plus_in_dir(tmp_path):
    """Ensure directories containing '+' are handled when loading multi-CSV."""
    dir_with_plus = tmp_path / "x++"
    dir_with_plus.mkdir()
    csv_file = dir_with_plus / "x__x__0.csv"
    csv_file.write_text("col1,col2\n1,2\n")

    # Provide the base name (without index) to trigger multi-file handling
    fr = FileReader(str(dir_with_plus / "x.csv"), "csv")

    assert len(fr.content_array) == 1
    sheet = fr.content_array[0]
    assert sheet.name == "x"
    # Raw path should match the file we created
    assert os.path.normpath(sheet.raw) == os.path.normpath(str(csv_file))
