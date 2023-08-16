with import <nixpkgs> {};

stdenv.mkDerivation {
    name = "django-actistream";
    buildInputs = [
        black
        isort
        python310
        python310Packages.django
        python310Packages.flake8
        python310Packages.pycodestyle
        python310Packages.python-lsp-server
        python310Packages.tox
        python310Packages.twine
    ];
}
