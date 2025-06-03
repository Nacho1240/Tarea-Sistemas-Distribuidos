{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  buildInputs = [
    pkgs.python312
    pkgs.python312Packages.pymongo
    pkgs.pig
  ];

  shellHook = ''
    python main.py
  '';
}

