# Project Name

## Introduction

This template is for creating a new project. Please replace this section with your project's introduction.

## Usage

Inside of a python environment, you can import the requirements and run the following commands to start the project.

```bash
pip install -r requirements.txt
python run.py
```

If you prefer to use docker, you can use the docker image.
```bash
docker build -t myproject --target RUN .
docker run myproject
```

## Testing
To test the library, you can use the `run_tests.py` script. It is highly recommended to use the docker image to keep your system isolated from integration tests.

Using docker, you can run the following commands to run the tests.
```bash
docker build -t tests --target TEST .
docker run tests
```

You may still run the tests on your system, but it is recommended to use the docker image.
```bash
pip install pytest coverage
python run_tests.py
```

## License

This project is licensed under the MIT license.

## Contribution

This project is open source. Feel free to contribute to the project by making a pull request, creating an issue ticket, or sending an email to [Johnny Irvin](mailto:irvinjohnathan@gmail.com).