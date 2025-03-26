import sys

from a3.aegis_main import Aegis


def main() -> None:
    aegis = Aegis()

    try:
        print("Aegis  : Initializing.")
        if not aegis.read_command_line(sys.argv[1:]):
            print(
                "Aegis  : Unable to initialize.",
                file=sys.stderr,
            )
            sys.exit(1)

        print("Aegis  : Starting Up.")
        if not aegis.start_up():
            print(
                "Aegis  : Unable to start up.",
                file=sys.stderr,
            )
            sys.exit(1)

        if not aegis.build_world():
            print(
                "Aegis  : Error building world.",
                file=sys.stderr,
            )
            sys.exit(1)

        print("Aegis  : Waiting for agents.")
        _ = sys.stdout.flush()

        aegis.connect_all_agents()
        aegis.run_state()

    except Exception as e:
        print(f"Exception: {e}", file=sys.stderr)
        sys.exit(1)
    finally:
        print("Aegis  : Done.")
        aegis.shutdown()


if __name__ == "__main__":
    main()
