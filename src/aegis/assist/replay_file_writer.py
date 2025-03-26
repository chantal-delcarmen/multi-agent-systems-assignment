import os
from datetime import datetime


class ReplayFileWriter:
    replay_file = None

    @staticmethod
    def open_replay_file(filename: str, world_filename: str) -> bool:
        try:
            if ReplayFileWriter.replay_file is not None:
                ReplayFileWriter.close_replay_file()
            ReplayFileWriter.replay_file = open(filename, "w")

            if not os.path.exists(world_filename):
                print(f"Cannot find world file {world_filename}")
                return False

            with open(world_filename, "r") as world_file:
                world_file_content = world_file.read()
                _ = ReplayFileWriter.replay_file.write(f"{len(world_file_content)}\n")
                _ = ReplayFileWriter.replay_file.write(world_file_content + "\n")
                _ = ReplayFileWriter.replay_file.write(
                    f"System Run date: {datetime.now()}\n"
                )
                ReplayFileWriter.replay_file.flush()

        except FileNotFoundError:
            print(f"Cannot find/open replay file {filename}")
            return False
        except Exception as ex:
            print(f"Error writing to {filename}: {str(ex)}")
            return False
        return True

    @staticmethod
    def close_replay_file() -> None:
        if ReplayFileWriter.replay_file is not None:
            ReplayFileWriter.replay_file.close()

    @staticmethod
    def write_string(string: str) -> None:
        if ReplayFileWriter.replay_file is not None:
            _ = ReplayFileWriter.replay_file.write(string)
            ReplayFileWriter.replay_file.flush()

    @classmethod
    def __del__(cls) -> None:
        cls.close_replay_file()
