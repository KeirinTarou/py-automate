import sys
import importlib.util
from pathlib import Path

def get_base_dir() -> Path:
    """
    実行ファイルのディレクトリのパスを解決する
    
    - `.py`から実行: __file__の場所
    - `.exe`から実行: .exeのあるディレクトリ
    :return: 実行ファイルのディレクトリのパスを表すPathオブジェクト
    :rtype: Path
    """
    # .exe実行時 -> "_MEIPASS"あり
    if hasattr(sys, "_MEIPASS"):
        # .exeのあるディレクトリのパスを返す
        return Path(sys.argv[0]).resolve().parent
    # .py実行時 -> .pyのあるディレクトリのパスを返す
    else:
        return Path(__file__).resolve().parent

def run_script(script_path: Path, script_args: list[str]):
    """ Python スクリプトを別モジュールとして読み込み、引数を渡して実行する。
 
    :param script_path: 実行したいスクリプトのパス
    :type script_path: Path
    :param script_args: スクリプトに渡す引数のリスト\n
        - モジュール内では`ARGS`として参照可
    :type script_args: list[str]

    Usage: \n
        - run_script(Path("example.py"), ["--mode", "test"]):
            - `example.py`内で`ARGS`に`["--mode", "test"]`が格納される
    """
    
    # 読み込んだスクリプトのファイルベース名を元に一時的なモジュール名を付与
    #   - foo.py: -> custom_script_foo
    unique_name = f"custom_script_{script_path.stem}"
    # 一時モジュールの情報を詰め込んだ構造体（spec）を作成する
    #   - この構造体の情報をもとにPythonがモジュールをロードする
    spec = importlib.util.spec_from_file_location(unique_name, script_path)
    # specを元にモジュールを作成する
    #   これにより、読み込んだスクリプトをモジュールとして実行できる
    module = importlib.util.module_from_spec(spec)
    # スクリプトに渡す引数をmodule側で受け取れるようにする
    module.ARGS = script_args
    # スクリプトの内容をmoduleに流し込む
    spec.loader.exec_module(module)

if __name__ == "__main__":
    # `py-automate.exe`に続く引数が最低1つは必要
    #   -> なければ終了コード`1`で終了
    if len(sys.argv) < 2:
        print("Usage: py-automate.exe <scriptfile.py> [args...]")
        sys.exit(1)

    # 実行形式（.py / .exe）に応じてスクリプトフォルダのパスを取得
    base_dir = get_base_dir()
    scripts_dir = base_dir / "scripts"

    # `scripts`フォルダをPythonのimportパスに闘魂注入
    #   - スクリプトファイルの親フォルダを解決
    #   - importパスに闘魂注入
    if str(scripts_dir) not in sys.path:
        sys.path.insert(0, str(scripts_dir))

    script_file = scripts_dir / sys.argv[1]

    if not script_file.exists():
        # 1つ目のコマンドライン引数が存在しないファイル
        #   -> 終了コード`1`で終了
        print(f"Script file not found: {script_file}")
        sys.exit(1)

    # 2番目以降の引数をスクリプトへ渡す
    args = sys.argv[2:]
    run_script(script_file, args)
