{
  description = "An experiment with LSAT";

  inputs = {
    flake-parts.url = "github:hercules-ci/flake-parts";
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";


    scipopt-nix = {
      url = "github:Lichthagel/scipopt-nix";
      inputs.nixpkgs.follows = "nixpkgs";
    };
  };

  outputs = inputs@{ flake-parts, ... }:
    flake-parts.lib.mkFlake { inherit inputs; } {
      systems = [ "x86_64-linux" "aarch64-linux" "aarch64-darwin" "x86_64-darwin" ];

      perSystem = { config, self', inputs', pkgs, system, ... }: {
        devShells.default = pkgs.mkShell {
          buildInputs = [
            (pkgs.python3.withPackages (p : [
              p.numpy
              p.rich
              p.ortools
              p.mypy
              p.parsy
              p.fire
              # p.pyscipopt
            ]))
            pkgs.black
            pkgs.mypy
          ];
        };
      };
    };
}
