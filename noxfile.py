import nox
import shutil


source_files = (
    "elastic_workplace_search/",
    "tests/",
    "noxfile.py",
    "setup.py",
)


@nox.session()
def blacken(session):
    session.install("black")
    session.run("black", *source_files)

    lint(session)


@nox.session()
def lint(session):
    session.install("black", "flake8", "twine", "wheel")

    session.run("black", "--check", *source_files)
    session.run("flake8", "--select=E,W,F", *source_files)

    shutil.rmtree("dist/", ignore_errors=True)
    session.run("python", "setup.py", "sdist", "bdist_wheel")
    session.run("twine", "check", "dist/*")


@nox.session(python=["2.7", "3.5", "3.6", "3.7", "3.8"])
def test(session):
    session.install(".")
    session.install("-r", "dev-requirements.txt")

    session.run("pytest", "tests/")
