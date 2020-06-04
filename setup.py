import cx_Freeze

executables = [cx_Freeze.Executable("client.py")]

cx_Freeze.setup(
    name="SmashRPS",
    options={"build_exe": {"packages":[
        "pygame"
        ],
                           "include_files":[
                               "p.png",
                               "r.png",
                               "s.png",
                               "crown.png"
                            ]}},
    executables = executables

    )